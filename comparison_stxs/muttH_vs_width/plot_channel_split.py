# Stat-only expected mu_ttH 1 sigma intervals (k_lambda = 1, 172 fb-1, ttH at 13.6 TeV) for hadronic-only, leptonic-only
# and all categories: Run 2 STXS, Run 3 STXS and Run 3 C1 binning. Reads the scan points from the inputs_channel_split.json
# runs (run dirs in their final homes or still in Combine); the Run 3 all-category scans are the existing 172 fb-1 ones
import ROOT
import os
import glob

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

base = os.path.dirname(os.path.abspath(__file__))
cs = os.path.abspath(os.path.join(base, ".."))
cdir = os.path.abspath(os.path.join(cs, "..", "Combine"))

def find(rundir, homes):
    for h in homes + [cdir]:
        if os.path.isdir(os.path.join(h, rundir)): return os.path.join(h, rundir)
    raise SystemExit("Missing run dir %s" % rundir)

# 2 deltaNLL scan from the POINTS files (or the hadded file), +-1 sigma by linear interpolation of the crossings
def band(pattern, poi):
    pts = {}
    for fn in glob.glob(pattern):
        f = ROOT.TFile.Open(fn)
        for e in f.Get("limit"):
            pts[round(getattr(e, poi), 6)] = 2 * e.deltaNLL
        f.Close()
    xs = sorted(pts); ys = [pts[x] for x in xs]; m = min(ys); ys = [y - m for y in ys]; i0 = ys.index(0.)
    def cross(rng):
        for a in rng:
            b = a + 1
            if (ys[a] - 1) * (ys[b] - 1) <= 0 and ys[a] != ys[b]:
                return xs[a] + (1 - ys[a]) * (xs[b] - xs[a]) / (ys[b] - ys[a])
    lo, hi = cross(range(i0 - 1, -1, -1)), cross(range(i0, len(xs) - 1))
    return hi - xs[i0], xs[i0] - lo

r2 = find("runFits_Run2_ttHCats_muttH_channels_Run2", [os.path.join(cs, "Run2")])
s3 = find("runFits_ttHCats_Only_muttH_channels_STXS3", [os.path.join(cs, "Run3", "Sep26")])
c1 = find("runFits_C1reco_2224_sigscale_muttH_channels_C1", [base])
pts = lambda d, tag, poi: os.path.join(d, "higgsCombine_profile1D_statonly%s_%s.POINTS.*.root" % (tag, poi))

# (label, colour, {block: (up, dn)})
analyses = [
    ("Run 2, STXS binning", ROOT.kGreen + 2, {
        "had": band(pts(r2, "Had", "mu_ttH_norm"), "mu_ttH_norm"),
        "lep": band(pts(r2, "Lep", "mu_ttH_norm"), "mu_ttH_norm"),
        "all": band(pts(r2, "All", "mu_ttH_norm"), "mu_ttH_norm")}),
    ("Run 3, STXS binning", ROOT.kBlue + 1, {
        "had": band(pts(s3, "Had", "mu_ttH"), "mu_ttH"),
        "lep": band(pts(s3, "Lep", "mu_ttH"), "mu_ttH"),
        "all": band(os.path.join(cs, "Run3", "Sep26", "runFits_ttHCats_Only_muttH_kl1_STXS",
                                 "higgsCombine_profile1D_statonly_mu_ttH.POINTS.*.root"), "mu_ttH")}),
    ("Run 3, #hat{C}_{1} binning", ROOT.kRed + 1, {
        "had": band(pts(c1, "Had", "mu_ttH"), "mu_ttH"),
        "lep": band(pts(c1, "Lep", "mu_ttH"), "mu_ttH"),
        "all": band(os.path.join(cdir, "aug26", "runFits_C1reco_2224_muttH_kl1",
                                 "higgsCombine_profile1D_statonly_mu_ttH.POINTS.*.root"), "mu_ttH")}),
]
blocks = [("had", "Hadronic only"), ("lep", "Leptonic only"), ("all", "All categories")]
for lab, _, r in analyses:
    print(lab.replace("#hat{C}_{1}", "C1"), {k: "+%.3f/-%.3f" % v for k, v in r.items()})

# Hand-built subscript: TLatex's _{} leaves a gap after the mu
muttH = "#mu#lower[0.3]{#scale[0.7]{ttH}}"

# y layout: blocks top to bottom, three rows per block
ystep, gap = 1.0, 0.9
ypos, ycentre, y = {}, {}, 0.
for bk, _ in blocks:
    rows = []
    for i in range(len(analyses)):
        y -= ystep; ypos[(bk, i)] = y; rows.append(y)
    ycentre[bk] = sum(rows) / len(rows)
    y -= gap
ylo, yhi = y + gap - 0.8, 0.2 + 2.6

xlo, xhi = 0.35, 1.95
c = ROOT.TCanvas("c", "c", 800, 650)
c.SetLeftMargin(0.2); c.SetBottomMargin(0.11); c.SetRightMargin(0.03); c.SetTopMargin(0.06)
frame = ROOT.TH1F("frame", "", 100, xlo, xhi)
frame.SetMinimum(ylo); frame.SetMaximum(yhi)
frame.GetXaxis().SetTitle("Expected %s" % muttH)
frame.GetXaxis().SetTitleSize(0.048); frame.GetXaxis().SetLabelSize(0.042); frame.GetXaxis().SetTitleOffset(1.0)
frame.GetYaxis().SetLabelSize(0); frame.GetYaxis().SetTickLength(0)
frame.Draw("AXIS")  # AXIS: the empty histogram would draw a line at y = 0
keep = [frame]

one = ROOT.TLine(1, ylo, 1, ypos[(blocks[0][0], 0)] + 0.6); one.SetLineStyle(2); one.SetLineColor(ROOT.kGray + 2); one.Draw()
keep.append(one)

# Light separators between blocks
for bk, _ in blocks[1:]:
    ys = ypos[(bk, 0)] + 0.5 * (ystep + gap)
    l = ROOT.TLine(xlo, ys, xhi, ys); l.SetLineColor(ROOT.kGray); l.SetLineStyle(3); l.Draw(); keep.append(l)

txt = ROOT.TLatex(); txt.SetTextFont(42)
for i, (lab, col, r) in enumerate(analyses):
    g = ROOT.TGraphAsymmErrors()
    for bk, _ in blocks:
        up, dn = r[bk]
        n = g.GetN(); g.SetPoint(n, 1., ypos[(bk, i)]); g.SetPointError(n, dn, up, 0, 0)
        txt.SetTextSize(0.027); txt.SetTextColor(col); txt.SetTextAlign(12)
        txt.DrawLatex(1. + up + 0.03, ypos[(bk, i)], "+%.3f / #minus%.3f" % (up, dn))
    g.SetLineColor(col); g.SetLineWidth(4); g.SetMarkerColor(col); g.SetMarkerStyle(20); g.SetMarkerSize(1.2)
    g.Draw("PZ SAME"); keep.append(g)
    analyses[i] = (lab, col, r, g)

# Block labels in the left margin
bl = ROOT.TLatex(); bl.SetTextFont(42); bl.SetTextSize(0.04); bl.SetTextAlign(32)
for bk, name in blocks:
    bl.DrawLatex(xlo - 0.03, ycentre[bk], name)

# Legend (TLatex text: TLegend adds a gap before sub/superscripts)
lx1, lx2, ly2, rowh = 0.22, 0.6, 0.915, 0.045
leg = ROOT.TLegend(lx1, ly2 - rowh * len(analyses), lx2, ly2)
leg.SetBorderSize(0); leg.SetFillStyle(0); leg.SetMargin(0.12)
for lab, col, r, g in analyses:
    leg.AddEntry(g, " ", "lp")
leg.Draw(); keep.append(leg)
tl = ROOT.TLatex(); tl.SetNDC(); tl.SetTextFont(42); tl.SetTextSize(0.034); tl.SetTextAlign(12)
for k, (lab, col, r, g) in enumerate(analyses):
    tl.DrawLatex(lx1 + leg.GetMargin() * (lx2 - lx1) + 0.01, ly2 - (k + 0.5) * rowh, lab)

lat = ROOT.TLatex(); lat.SetNDC()
lat.SetTextFont(62); lat.SetTextSize(0.055); lat.DrawLatex(0.71, 0.87, "CMS")
lat.SetTextFont(52); lat.SetTextSize(0.042); lat.DrawLatex(0.71, 0.825, "Internal")
lat.SetTextFont(42); lat.SetTextSize(0.034); lat.SetTextAlign(31)
lat.DrawLatex(0.97, 0.95, "Stat-only, #kappa_{#lambda} = 1, 172 fb^{-1} (2022-2024), ttH at 13.6 TeV")

c.RedrawAxis()
for ext in ("png", "pdf"):
    c.SaveAs(os.path.join(base, "channel_split_muttH.%s" % ext))
