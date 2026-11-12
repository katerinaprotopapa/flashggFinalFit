# Stat-only mu_ttH +1 sigma and -1 sigma (k_lambda = 1) vs global signal width scale CMS_hgg_sigma_scale, 2022-2024
# aug26 C1 binning at 172 fb-1, compared with Run 2 STXS scaled to 172 fb-1 with the ttH xs at 13 TeV and at 13.6 TeV.
# Reads the hadded scans made by CollectFits.py (modes muttH_vs_width_172fb and muttH_run2_172fb).
# The previous 138 fb-1 version is plot_muttH_vs_width_alternative.py.
import ROOT
import os
import re
import glob

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

base = os.path.dirname(os.path.abspath(__file__))
cdir = os.path.join(base, "..", "..", "Combine")

# Yield-weighted sigma_eff over all categories (sigma_eff.py), MH = 125 GeV. ttH only: Run 3 C1 1.825 GeV, Run 2 STXS
# 1.650 GeV. All Higgs processes: Run 3 1.870 GeV, Run 2 1.645 GeV. Run 2 is the same at 13 and 13.6 TeV (ttH xs) to
# better than 0.001 GeV in both definitions
seff_run3, seff_run2 = 1.825, 1.650
seff_run3_all, seff_run2_all = 1.870, 1.645
run2_x = seff_run2 / seff_run3
run2_x_all = seff_run2_all / seff_run3_all

# Hand-built subscript: TLatex's _{} leaves a gap after the mu
muttH = "#mu#lower[0.3]{#scale[0.7]{ttH}}"

# +-1 sigma from 2 deltaNLL = 1 crossings (linear interpolation between scan points)
def sigma_band(path, poi="mu_ttH"):
    f = ROOT.TFile.Open(path)
    pts = {}
    for e in f.Get("limit"):
        pts[round(getattr(e, poi), 6)] = 2 * e.deltaNLL
    f.Close()
    xs = sorted(pts)
    ys = [pts[x] for x in xs]
    m = min(ys)
    ys = [y - m for y in ys]
    i0 = ys.index(0.)
    def cross(rng):
        for a in rng:
            b = a + 1
            if (ys[a] - 1) * (ys[b] - 1) <= 0 and ys[a] != ys[b]:
                return xs[a] + (1 - ys[a]) * (xs[b] - xs[a]) / (ys[b] - ys[a])
        return None
    lo, hi = cross(range(i0 - 1, -1, -1)), cross(range(i0, len(xs) - 1))
    return xs[i0] - lo, hi - xs[i0]

def find(rundir, homes):
    for h in homes + [cdir]:
        if os.path.isdir(os.path.join(h, rundir)):
            return os.path.join(h, rundir)
    raise SystemExit("Missing run dir %s" % rundir)

# Run 3 C1 width points at 172 fb-1
rd3 = find("runFits_C1reco_2224_sigscale_muttH_vs_width_172fb", [base])
res = {}
for fn in glob.glob(os.path.join(rd3, "profile1D_statonlyS*_mu_ttH.root")):
    m = re.search(r"statonlyS(\d)p(\d)_mu_ttH\.root$", fn)
    if m:
        dn, up = sigma_band(fn)
        res[float("%s.%s" % m.groups())] = {"up": up, "dn": dn}
scales = sorted(res)
for s in scales:
    print("s = %.1f: +%.3f -%.3f" % (s, res[s]["up"], res[s]["dn"]))

# Run 2 STXS at 172 fb-1 (lumi_scale 1.256), POI mu_ttH_norm: ttH xs at 13 TeV and at 13.6 TeV
rd2 = find("runFits_Run2_ttHCats_muttH_run2_172fb", [os.path.join(base, "..", "Run2")])
run2 = {}
for e in ("13TeV", "13p6TeV"):
    dn, up = sigma_band(os.path.join(rd2, "profile1D_statonly%s_mu_ttH_norm.root" % e), poi="mu_ttH_norm")
    run2[e] = {"up": up, "dn": dn}
    print("Run 2 (%s): +%.3f -%.3f" % (e, up, dn))

# Width where the Run 3 curve reaches the Run 2 (13.6 TeV) value (linear interpolation between measured points)
def match(side, ref):
    for a, b in zip(scales, scales[1:]):
        ya, yb = res[a][side] - ref[side], res[b][side] - ref[side]
        if ya * yb <= 0 and ya != yb:
            return a + (b - a) * (-ya) / (yb - ya)
    return None

xlo, xhi, ylo, yhi = 0.1, 1.75, 0.4, 1.9  # same axes as plot_muttH_vs_width_alternative.py

for side in ("up", "dn"):
    for e in ("13p6TeV", "13TeV"):
        sm = match(side, run2[e])
        print("%s: Run 3 reaches Run 2 %s (%.3f) at width %s" % (side, e, run2[e][side], "%.2f" % sm if sm else "-- (outside scanned range)"))

# Run 2 points at both definitions of the width position (Run 2 / Run 3 sigma_eff ratio): ttH only (filled markers)
# and all Higgs (open markers)
def draw(outname):
    print("Run 2 points at width %.3f (ttH sigma_eff) and %.3f (all Higgs)" % (run2_x, run2_x_all))

    c = ROOT.TCanvas("c", "c", 700, 600)
    c.SetLeftMargin(0.13); c.SetBottomMargin(0.12); c.SetRightMargin(0.03); c.SetTopMargin(0.06)
    c.SetTicks(1, 1)
    frame = ROOT.TH1F("frame", "", 100, xlo, xhi)
    frame.SetMinimum(ylo); frame.SetMaximum(yhi)
    frame.GetXaxis().SetTitle("Signal width scaling")
    frame.GetYaxis().SetTitle("Expected %s" % muttH)
    frame.GetXaxis().SetTitleSize(0.048); frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.045); frame.GetYaxis().SetLabelSize(0.045)
    frame.GetYaxis().SetTitleOffset(1.15); frame.GetXaxis().SetTitleOffset(1.1)
    frame.GetXaxis().SetNdivisions(508)
    frame.Draw()

    # Run 3: light red band between mu_ttH = 1 - (-1 sigma) and 1 + (+1 sigma) at each width
    band = ROOT.TGraph()
    for s in scales:
        band.SetPoint(band.GetN(), s, 1. + res[s]["up"])
    for s in reversed(scales):
        band.SetPoint(band.GetN(), s, 1. - res[s]["dn"])
    band.SetFillColor(ROOT.kRed - 10); band.SetLineWidth(0)
    band.Draw("F SAME")

    # Best fit (Asimov) at mu_ttH = 1
    l_one = ROOT.TLine(scales[0], 1, scales[-1], 1); l_one.SetLineColor(ROOT.kRed + 1); l_one.SetLineStyle(2); l_one.SetLineWidth(2); l_one.Draw()

    # Nominal width: black dashed guides from the axes to the Run 3 band edges at scaling 1
    guides = [ROOT.TLine(1, ylo, 1, 1. + res[1.0]["up"])]
    for v in (1. + res[1.0]["up"], 1. - res[1.0]["dn"]):
        guides.append(ROOT.TLine(xlo, v, 1, v))
    for l in guides:
        l.SetLineColor(ROOT.kBlack); l.SetLineStyle(2); l.SetLineWidth(2); l.Draw()

    keep = []
    lab_txt = ROOT.TLatex(); lab_txt.SetTextFont(42); lab_txt.SetTextSize(0.036); lab_txt.SetTextColor(ROOT.kRed + 1); lab_txt.SetTextAlign(12)
    for side, sign, lab in (("up", 1., "+1#sigma"), ("dn", -1., "-1#sigma")):
        g = ROOT.TGraph()
        for s in scales:
            g.SetPoint(g.GetN(), s, 1. + sign * res[s][side])
        g.SetLineColor(ROOT.kRed + 1); g.SetLineWidth(2)
        g.SetMarkerColor(ROOT.kRed + 1); g.SetMarkerStyle(20); g.SetMarkerSize(1.1)
        g.Draw("LP SAME")
        lab_txt.DrawLatex(scales[-1] + 0.03, 1. + sign * res[scales[-1]][side], lab)
        keep.append(g)

    # Run 2: mu_ttH = 1 with its expected +-1 sigma, both at Run 2's own sigma_eff (the ttH xs scaling does not change it);
    # the wider 13 TeV bar (blue) is drawn first and the 13.6 TeV one (green) on top, semi-transparent, so both stay visible
    def run2_point(r, marker, colour, alpha, x):
        g = ROOT.TGraphAsymmErrors(1)
        g.SetPoint(0, x, 1.)
        g.SetPointError(0, 0., 0., r["dn"], r["up"])
        g.SetMarkerStyle(marker); g.SetMarkerSize(1.8); g.SetMarkerColorAlpha(colour, alpha)
        g.SetLineColorAlpha(colour, alpha); g.SetLineWidth(3)
        g.Draw("P SAME")
        keep.append(g)
        return g
    # one colour per point; the 13.6 TeV bars (narrower, drawn on top) are semi-transparent so the 13 TeV ones show
    g2_13_all = run2_point(run2["13TeV"], 33, ROOT.kOrange + 1, 1., run2_x_all)
    g2_136_all = run2_point(run2["13p6TeV"], 34, ROOT.kViolet + 1, 0.5, run2_x_all)
    g2_13 = run2_point(run2["13TeV"], 33, ROOT.kAzure + 2, 1., run2_x)
    g2_136 = run2_point(run2["13p6TeV"], 34, ROOT.kGreen + 2, 0.5, run2_x)

    rows = [(band, "Run 3 #hat{C}_{1} binning", "f"),
            (g2_13, "Run 2 STXS at 13 TeV: ttH #sigma_{eff} ratio", "pe"),
            (g2_136, "Run 2 STXS with ttH at 13.6 TeV: ttH #sigma_{eff} ratio", "pe"),
            (g2_13_all, "Run 2 STXS at 13 TeV: all-Higgs #sigma_{eff} ratio", "pe"),
            (g2_136_all, "Run 2 STXS with ttH at 13.6 TeV: all-Higgs #sigma_{eff} ratio", "pe")]

    # Legend (TLatex text: TLegend adds a gap before sub/superscripts)
    lx1, lx2, ly2, rowh = 0.16, 0.6, 0.905, 0.046
    leg = ROOT.TLegend(lx1, ly2 - rowh * len(rows), lx2, ly2)
    leg.SetBorderSize(0); leg.SetFillStyle(0); leg.SetMargin(0.17)
    for obj, lab, opt in rows:
        leg.AddEntry(obj, " ", opt)
    leg.Draw()
    tl = ROOT.TLatex(); tl.SetNDC(); tl.SetTextFont(42); tl.SetTextSize(0.029); tl.SetTextAlign(12)
    for i, (obj, lab, opt) in enumerate(rows):
        tl.DrawLatex(lx1 + leg.GetMargin() * (lx2 - lx1) + 0.01, ly2 - (i + 0.5) * rowh, lab)

    note = ROOT.TLatex(); note.SetNDC(); note.SetTextFont(42); note.SetTextSize(0.029); note.SetTextColor(ROOT.kGray + 2)
    note.SetTextAlign(31)
    note.DrawLatex(0.95, 0.83, "Run 2 at 172 fb^{-1}")

    lat = ROOT.TLatex(); lat.SetNDC()
    lat.SetTextFont(62); lat.SetTextSize(0.06); lat.SetTextAlign(31); lat.DrawLatex(0.95, 0.875, "CMS #font[52]{#scale[0.75]{Internal}}")
    lat.SetTextFont(42); lat.SetTextSize(0.037); lat.SetTextAlign(31)
    lat.DrawLatex(0.97, 0.95, "Stat-only, #kappa_{#lambda} = 1, 2022-2024")

    c.RedrawAxis()
    for ext in ("png", "pdf"):
        c.SaveAs(os.path.join(base, "%s.%s" % (outname, ext)))


draw("muttH_vs_width")
