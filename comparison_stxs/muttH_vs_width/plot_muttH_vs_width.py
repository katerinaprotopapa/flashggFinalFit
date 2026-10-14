# Stat-only mu_ttH +1 sigma and -1 sigma (k_lambda = 1) vs global signal width scale CMS_hgg_sigma_scale, 2022-2024
# aug26 C1 binning setup scaled to 138 fb-1, compared with Run 2. Reads the hadded scans made by CollectFits.py
# (modes muttH_vs_width, muttH_vs_width_extra and muttH_run2_13p6TeV)
import ROOT
import os
import re
import glob

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

base = os.path.dirname(os.path.abspath(__file__))
cdir = os.path.join(base, "..", "..", "Combine")

# Yield-weighted ttH sigma_eff over all categories (sigma_eff.py): Run 3 C1 nominal 1.825 GeV, Run 2 STXS 1.650 GeV
seff_run3, seff_run2 = 1.825, 1.650
run2_x = seff_run2 / seff_run3

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

# Collect every 138 fb-1 width point from both run dirs (final home here, or still in Combine)
res = {}
for mode in ("muttH_vs_width", "muttH_vs_width_extra"):
    rd = "runFits_C1reco_2224_sigscale_%s" % mode
    for d in (os.path.join(base, rd), os.path.join(cdir, rd)):
        if os.path.isdir(d):
            for fn in glob.glob(os.path.join(d, "profile1D_statonlyS*_mu_ttH.root")):
                m = re.search(r"statonlyS(\d)p(\d)_mu_ttH\.root$", fn)  # skips the S1p0lumi172 validation scan
                if m:
                    dn, up = sigma_band(fn)
                    res[float("%s.%s" % m.groups())] = {"up": up, "dn": dn}
            break
scales = sorted(res)
for s in scales:
    print("s = %.1f: +%.3f -%.3f" % (s, res[s]["up"], res[s]["dn"]))

# Run 2: same stat-only scan (k_lambda = 1) on the Run 2 ttH-categories card at its own 137.2 fb-1, ttH xs at 13.6 TeV
# (mode muttH_run2_13p6TeV, POI mu_ttH_norm)
rd2 = "runFits_Run2_ttHCats_muttH_run2_13p6TeV"
for d in (os.path.join(base, "..", "Run2", rd2), os.path.join(cdir, rd2)):
    if os.path.isdir(d):
        dn, up = sigma_band(os.path.join(d, "profile1D_statonly_mu_ttH_norm.root"), poi="mu_ttH_norm")
        break
run2 = {"up": up, "dn": dn}
print("Run 2: +%.3f -%.3f" % (up, dn))

# Width where the Run 3 curve reaches the Run 2 value (linear interpolation between measured points)
def match(side):
    for a, b in zip(scales, scales[1:]):
        ya, yb = res[a][side] - run2[side], res[b][side] - run2[side]
        if ya * yb <= 0 and ya != yb:
            return a + (b - a) * (-ya) / (yb - ya)
    return None

xlo, xhi, ylo, yhi = 0.1, 1.75, 0.4, 1.9

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
    sm = match(side)
    print("%s: Run 3 reaches Run 2 (%.2f) at width %s" % (side, run2[side], "%.2f" % sm if sm else "-- (outside scanned range)"))
    keep.append(g)

# Run 2: mu_ttH = 1 with its expected +-1 sigma, at its own sigma_eff
g2 = ROOT.TGraphAsymmErrors(1)
g2.SetPoint(0, run2_x, 1.)
g2.SetPointError(0, 0., 0., run2["dn"], run2["up"])
g2.SetMarkerStyle(34); g2.SetMarkerSize(1.8); g2.SetMarkerColor(ROOT.kGreen + 2)
g2.SetLineColor(ROOT.kGreen + 2); g2.SetLineWidth(3)
g2.Draw("P SAME")
keep.append(g2)

rows = [(band, "Run 3, #hat{C}_{1} binning", "f"), (g2, "Run 2, STXS binning", "pe")]
print("Run 2 point at width %.3f (sigma_eff %.3f / %.3f GeV)" % (run2_x, seff_run2, seff_run3))

# Legend (TLatex text: TLegend adds a gap before sub/superscripts)
lx1, lx2, ly2, rowh = 0.17, 0.55, 0.80, 0.055
leg = ROOT.TLegend(lx1, ly2 - rowh * len(rows), lx2, ly2)
leg.SetBorderSize(0); leg.SetFillStyle(0); leg.SetMargin(0.2)
for obj, lab, opt in rows:
    leg.AddEntry(obj, " ", opt)
leg.Draw()
tl = ROOT.TLatex(); tl.SetNDC(); tl.SetTextFont(42); tl.SetTextSize(0.035); tl.SetTextAlign(12)
for i, (obj, lab, opt) in enumerate(rows):
    tl.DrawLatex(lx1 + leg.GetMargin() * (lx2 - lx1) + 0.01, ly2 - (i + 0.5) * rowh, lab)

lat = ROOT.TLatex(); lat.SetNDC()
lat.SetTextFont(62); lat.SetTextSize(0.06); lat.DrawLatex(0.17, 0.86, "CMS")
lat.SetTextFont(52); lat.SetTextSize(0.045); lat.DrawLatex(0.30, 0.86, "Internal")
lat.SetTextFont(42); lat.SetTextSize(0.037); lat.SetTextAlign(31)
lat.DrawLatex(0.97, 0.95, "Stat-only, #kappa_{#lambda} = 1, 138 fb^{-1} (2022-2024 scaled), 13.6 TeV")

c.RedrawAxis()
for ext in ("png", "pdf"):
    c.SaveAs(os.path.join(base, "muttH_vs_width.%s" % ext))
