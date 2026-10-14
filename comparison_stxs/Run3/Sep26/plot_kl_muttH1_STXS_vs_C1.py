# Overlay stat-only kappa_lambda scans: C1 binning vs STXS ttH categories (Run 3) and Run 2 STXS (13.6 TeV ttH xs),
# all at the same luminosity. For each luminosity, two plots:
#   - mu_ttH fixed to 1 (normalisation + shape)    [CollectFits modes kl_muttH1, kl_muttH1_Run2 (+ _lumi300)]
#   - mu_ttH floating (shape only)                 [CollectFits modes kl_muttHfloat, kl_muttHfloat_Run2 (+ _lumi300)]
# 172 fb-1 = Run 3 2022-2024 (lumi_scale 1, Run 2: 172.26/138 = 1.248); 300 fb-1: lumi_scale 1.74, Run 2: 2.174
import ROOT
import os
from functools import partial
try:
    import CombineHarvester.CombineTools.plotting as plot  # cmsenv
except ImportError:
    import HiggsAnalysis.CombinedLimit.util.plotting as plot  # standalone flashggFinalFit env (as plot1DScan.py)

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

base = os.path.dirname(os.path.abspath(__file__))
ffdir = os.path.abspath(os.path.join(base, "..", "..", ".."))
cdir = os.path.join(ffdir, "Combine")
fixed_f = "profile1D_statonlyMuFixed_k_lambda.root"
float_f = "profile1D_statonlyMuFloat_k_lambda.root"

run2dir = os.path.abspath(os.path.join(base, "..", "..", "Run2"))

def first_existing(*paths):
    for p in paths:
        if os.path.exists(p): return p
    return paths[0]

# A scan in its final home (Sep26 for Run 3, comparison_stxs/Run2 for Run 2), or still in Combine right after
# RunFits/CollectFits
def scan(rundir, fname, home):
    return first_existing(os.path.join(home, rundir, fname), os.path.join(cdir, rundir, fname))

# (label, colour, fixed scan, floating scan) for a luminosity suffix ("" = 172 fb-1, "_lumi300" = 300 fb-1).
# The 300 fb-1 floating scans fall back to the earlier comparison runs (same workspaces and lumi_scale, mu_ttH free)
# when the kl_muttHfloat(_Run2)_lumi300 modes have not been run
def get_binnings(sfx):
    c1_flt = scan("runFits_C1reco_2224_kl_muttHfloat" + sfx, float_f, base)
    st_flt = scan("runFits_ttHCats_Only_kl_muttHfloat" + sfx, float_f, base)
    r2_flt = scan("runFits_Run2_ttHCats_kl_muttHfloat_Run2" + sfx, float_f, run2dir)
    if sfx == "_lumi300":
        c1_flt = first_existing(c1_flt, os.path.join(cdir, "aug26/runFits_C1reco_lumi300_kl_C1reco/statonly.root"))
        st_flt = first_existing(st_flt, os.path.join(base, "runFits_ttHCats_Only_kl_STXScomparison/statonly.root"))
        r2_flt = first_existing(r2_flt, os.path.join(run2dir, "runFits_Run2_ttHCats_kl_STXScomparison_Run2/statonly.root"))
    return [
        ("#hat{C}_{1} binning", ROOT.kRed + 1, scan("runFits_C1reco_2224_kl_muttH1" + sfx, fixed_f, base), c1_flt),
        ("STXS Run 3", ROOT.kBlue + 1, scan("runFits_ttHCats_Only_kl_muttH1" + sfx, fixed_f, base), st_flt),
        ("STXS Run 2", ROOT.kGreen + 2, scan("runFits_Run2_ttHCats_kl_muttH1_Run2" + sfx, fixed_f, run2dir), r2_flt),
    ]

# Hand-built subscript: TLatex's _{} leaves a gap after the mu
muttH = "#mu#lower[0.3]{#scale[0.7]{ttH}}"

# 2 deltaNLL vs k_lambda from the combine limit tree, shifted so the minimum is at 0
def scan_graph(path, name):
    f = ROOT.TFile.Open(path)
    pts = {}
    for e in f.Get("limit"):
        pts[round(e.k_lambda, 6)] = 2 * e.deltaNLL
    f.Close()
    xs = sorted(pts)
    ymin = min(pts.values())
    g = ROOT.TGraph(len(xs))
    g.SetName(name)
    for i, x in enumerate(xs):
        g.SetPoint(i, x, pts[x] - ymin)
    return g

# Same crossing method as plot1DScan.py (TSpline3 through the scan points + FindCrossingsWithSpline),
# so the quoted uncertainties match the single-scan plots
def crossings(g, level=1.0):
    n = g.GetN()
    xmin = g.GetX()[min(range(n), key=lambda i: g.GetY()[i])]
    spline = ROOT.TSpline3("spline3_" + g.GetName(), g)
    func_method = partial(lambda obj, x, params: obj.Eval(x[0]), spline)
    func = ROOT.TF1("splinefn_" + g.GetName(), func_method, g.GetX()[0], g.GetX()[n - 1], 1)
    func._method = func_method
    lo, hi = None, None
    for cr in plot.FindCrossingsWithSpline(g, func, level):
        if cr["lo"] <= xmin <= cr["hi"]:
            if cr["valid_lo"]: lo = cr["lo"]
            if cr["valid_hi"]: hi = cr["hi"]
    return xmin, lo, hi

def value_text(g):
    xmin, lo, hi = crossings(g)
    txt = "#kappa_{#lambda}: %.2f" % xmin
    if lo is not None and hi is not None:
        txt += "^{+%.2f}_{-%.2f}" % (hi - xmin, xmin - lo)
    else:
        # Interval not closed inside the scan range
        txt += "^{%s}_{%s}" % ("+%.2f" % (hi - xmin) if hi is not None else "> %g" % xhi,
                               "-%.2f" % (xmin - lo) if lo is not None else "< %g" % xlo)
    return txt, lo, hi

xlo, xhi, ymax = -20, 50, 3.

# which = "fixed" (mu_ttH = 1) or "float" (mu_ttH floating)
def make_plot(outname, which, sfx, lumitxt):
    binnings = get_binnings(sfx)
    c = ROOT.TCanvas("c_" + outname, "c", 700, 600)
    c.SetLeftMargin(0.115); c.SetBottomMargin(0.115); c.SetRightMargin(0.025); c.SetTopMargin(0.06)
    frame = ROOT.TH1F("frame_" + outname, "", 100, xlo, xhi)
    frame.SetMinimum(0); frame.SetMaximum(ymax)
    frame.GetXaxis().SetTitle("#kappa_{#lambda}")
    frame.GetYaxis().SetTitle("-2 #Delta ln L")
    frame.GetXaxis().SetTitleSize(0.05); frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.045); frame.GetYaxis().SetLabelSize(0.045)
    frame.GetYaxis().SetTitleOffset(1.1); frame.GetXaxis().SetTitleOffset(0.95)
    frame.Draw()
    keep = [frame]

    line = ROOT.TLine(xlo, 1, xhi, 1); line.SetLineStyle(2); line.SetLineColor(ROOT.kGray + 2); line.Draw()
    keep.append(line)

    # Rows: (legend sample, label, value text)
    rows = []
    for label, col, pfix, pflt in binnings:
        path = pfix if which == "fixed" else pflt
        if not os.path.exists(path):
            print("Skipping %s: %s not found" % (label, path))
            continue
        g = scan_graph(path, "g_%s_%d" % (outname, len(keep)))
        g.SetLineColor(col); g.SetLineWidth(3)
        g.Draw("L SAME")
        txt, lo, hi = value_text(g)
        print(outname, label, txt)
        for xc in (lo, hi):
            if xc is not None:
                v = ROOT.TLine(xc, 0, xc, 1); v.SetLineColor(col); v.SetLineStyle(3); v.Draw(); keep.append(v)
        rows.append((g, label, txt))
        keep.append(g)
    if not rows:
        print("Nothing to plot for %s" % outname)
        return

    # Legend at top centre (above the flat part of the scans). The text is TLatex (TLegend adds a gap before
    # the super/subscripts)
    rowh = 0.075
    lx1, lx2, ly2 = 0.33, 0.79, 0.925
    ly1 = ly2 - rowh * len(rows)
    leg = ROOT.TLegend(lx1, ly1, lx2, ly2)
    leg.SetBorderSize(0); leg.SetFillStyle(0); leg.SetMargin(0.16)
    for s, lab, txt in rows:
        leg.AddEntry(s, " ", "l")
    leg.Draw()
    keep.append(leg)
    vlat = ROOT.TLatex(); vlat.SetNDC(); vlat.SetTextFont(42); vlat.SetTextSize(0.037); vlat.SetTextAlign(12)
    for i, (s, lab, txt) in enumerate(rows):
        y = ly2 - (i + 0.5) * rowh
        vlat.DrawLatex(lx1 + leg.GetMargin() * (lx2 - lx1), y, lab)
        vlat.DrawLatex(lx1 + 0.255, y, txt)

    lat = ROOT.TLatex(); lat.SetNDC()
    lat.SetTextFont(62); lat.SetTextSize(0.06); lat.DrawLatex(0.14, 0.87, "CMS")
    lat.SetTextFont(52); lat.SetTextSize(0.045); lat.DrawLatex(0.14, 0.82, "Internal")
    lat.SetTextFont(42); lat.SetTextSize(0.037); lat.SetTextAlign(31)
    mutxt = "%s = 1" % muttH if which == "fixed" else "%s floating" % muttH
    lat.DrawLatex(0.975, 0.95, "Stat-only, %s, %s" % (mutxt, lumitxt))

    c.RedrawAxis()
    out = os.path.join(base, outname)
    for ext in ("png", "pdf"):
        c.SaveAs("%s.%s" % (out, ext))

for sfx, lumitxt in [("", "172 fb#kern[-0.55]{^{-1}} (2022-2024)"), ("_lumi300", "300 fb#kern[-0.55]{^{-1}} (2022-2024 rescaled)")]:
    make_plot("profile1D_statonly_kl_muttH1%s_STXS_vs_C1" % sfx, "fixed", sfx, lumitxt)
    make_plot("profile1D_statonly_kl_muttHfloat%s_STXS_vs_C1" % sfx, "float", sfx, lumitxt)
