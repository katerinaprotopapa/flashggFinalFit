# Overlay stat-only mu_ttH scans (k_lambda = 1): C1 binning ttH categories vs STXS ttH categories, Run 3 2022-2024 (lumi_scale = 1).
# Also the Run 2 STXS ttH categories alone (137 fb-1, ttH xs at 13 TeV) in the same style
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
gname = "profile1D.mu_ttH_kl1.statonly.asimov"

c1   = ("#hat{C}_{1} binning", os.path.join(ffdir, "Combine/aug26/runFits_C1reco_2224_muttH_kl1", gname + ".root"), ROOT.kRed + 1, 1)
stxs = ("STXS Run 3", os.path.join(base, "runFits_ttHCats_Only_muttH_kl1_STXS", gname + ".root"), ROOT.kBlue + 1, 1)
run2dir = os.path.abspath(os.path.join(base, "..", "..", "Run2", "runFits_Run2_ttHCats_muttH_run2"))
stxs2 = ("STXS Run 2", os.path.join(run2dir, "Plots", "profile1D_statonly_mu_ttH_norm_Run2_ttHCats.root"), ROOT.kBlack, 1)
# Same Run 2 card with the ttH xs scaled to 13.6 TeV (like-for-like with Run 3)
run2dir_13p6 = os.path.abspath(os.path.join(base, "..", "..", "Run2", "runFits_Run2_ttHCats_muttH_run2_13p6TeV"))
stxs2_13p6 = ("STXS Run 2", os.path.join(run2dir_13p6, "Plots", "profile1D_statonly_mu_ttH_norm_Run2_ttHCats.root"), ROOT.kBlack, 1)

# (output name, relative to this dir or absolute; scans; top-right label)
plots = [
    ("profile1D_statonly_muttH_STXS_vs_C1", [c1, stxs], "Stat-only, #kappa_{#lambda} = 1, 172 fb#kern[-0.55]{^{-1}} (2022-2024), 13.6 TeV"),
    (os.path.join(run2dir, "profile1D.mu_ttH.statonly.asimov"), [stxs2], "Run 2, 137 fb#kern[-0.55]{^{-1}} (13 TeV)"),
    (os.path.join(run2dir_13p6, "profile1D.mu_ttH.statonly.asimov"), [stxs2_13p6], "Run 2, 137 fb#kern[-0.55]{^{-1}}, ttH at 13.6 TeV"),
]

# The scan graph saved by plot1DScan.py (CollectFits names it with a "Plots/" prefix, which TFile::Get reads as a
# directory, so take it from the key list)
def load_graph(path):
    f = ROOT.TFile.Open(path)
    g = f.GetListOfKeys()[0].ReadObj()
    return f, g

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

ymax = 3.

# 3 significant figures, keeping trailing zeros (1.0 -> "1.00")
def sf3(x):
    return format(x, "#.3g")

def make_plot(outname, scans, header):
    graphs = []
    keep = []
    for label, path, col, style in scans:
        if not os.path.exists(path):
            raise SystemExit("Missing %s: %s" % (label, path))
        f, g = load_graph(path)
        g = g.Clone(label)
        g.SetLineColor(col); g.SetLineWidth(3); g.SetLineStyle(style)
        graphs.append((label, col, g))
        keep.append(f)

    # x range: wherever any scan is below ymax, with a small margin
    xs_in = [g.GetX()[i] for _, _, g in graphs for i in range(g.GetN()) if g.GetY()[i] <= ymax]
    pad = 0.1 * (max(xs_in) - min(xs_in))
    xlo, xhi = max(0., min(xs_in) - pad), max(xs_in) + pad

    c = ROOT.TCanvas("c_" + os.path.basename(outname), "c", 700, 600)
    c.SetLeftMargin(0.115); c.SetBottomMargin(0.115); c.SetRightMargin(0.025); c.SetTopMargin(0.06)
    frame = ROOT.TH1F("frame_" + os.path.basename(outname), "", 100, xlo, xhi)
    frame.SetMinimum(0); frame.SetMaximum(ymax)
    frame.GetXaxis().SetTitle("#mu_{ttH}")
    frame.GetYaxis().SetTitle("-2 #Delta ln L")
    frame.GetXaxis().SetTitleSize(0.05); frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.045); frame.GetYaxis().SetLabelSize(0.045)
    frame.GetYaxis().SetTitleOffset(1.1); frame.GetXaxis().SetTitleOffset(0.95)
    frame.Draw()

    line = ROOT.TLine(xlo, 1, xhi, 1); line.SetLineStyle(2); line.SetLineColor(ROOT.kGray + 2); line.Draw()

    # Legend at top centre (between the parabola arms): one row per scan, label followed by its mu_ttH value.
    # The text is drawn with TLatex (TLegend adds a gap before the super/subscripts)
    nrows = len(graphs)
    lx1, lx2, ly2 = 0.33, 0.79, 0.925
    ly1 = ly2 - 0.075 * nrows
    leg = ROOT.TLegend(lx1, ly1, lx2, ly2)
    leg.SetBorderSize(0); leg.SetFillStyle(0); leg.SetTextSize(0.037); leg.SetMargin(0.16)
    vals = []
    for label, col, g in graphs:
        g.Draw("L SAME")
        xmin, lo, hi = crossings(g)
        txt = "#mu_{ttH}: %s" % sf3(xmin)
        if lo is not None and hi is not None:
            txt += "^{+%s}_{-%s}" % (sf3(hi - xmin), sf3(xmin - lo))
        print(outname, label, xmin, lo, hi)
        leg.AddEntry(g, " ", "l")
        vals.append((label, txt))
        for xc in (lo, hi):
            if xc is not None:
                v = ROOT.TLine(xc, 0, xc, 1); v.SetLineColor(col); v.SetLineStyle(3); v.Draw(); keep.append(v)
    leg.Draw()

    vlat = ROOT.TLatex(); vlat.SetNDC(); vlat.SetTextFont(42); vlat.SetTextSize(0.037); vlat.SetTextAlign(12)
    rowh = (ly2 - ly1) / nrows
    for i, (label, txt) in enumerate(vals):
        y = ly2 - (i + 0.5) * rowh
        vlat.DrawLatex(lx1 + leg.GetMargin() * (lx2 - lx1), y, label)
        vlat.DrawLatex(lx1 + 0.255, y, txt)

    lat = ROOT.TLatex(); lat.SetNDC()
    lat.SetTextFont(62); lat.SetTextSize(0.06); lat.DrawLatex(0.14, 0.87, "CMS")
    lat.SetTextFont(52); lat.SetTextSize(0.045); lat.DrawLatex(0.14, 0.82, "Internal")
    lat.SetTextFont(42); lat.SetTextSize(0.037); lat.SetTextAlign(31)
    lat.DrawLatex(0.975, 0.95, header)

    c.RedrawAxis()
    out = os.path.join(base, outname)
    for ext in ("png", "pdf"):
        c.SaveAs("%s.%s" % (out, ext))

for outname, scans, header in plots:
    make_plot(outname, scans, header)
