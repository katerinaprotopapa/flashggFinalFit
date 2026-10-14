# Overlay stat-only kappa_lambda scans: C1 binning ttH categories vs STXS ttH categories (Run 3, and Run 2 scaled to 300/fb)
import ROOT
import os
from functools import partial
import CombineHarvester.CombineTools.plotting as plot

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

base = os.path.dirname(os.path.abspath(__file__))
ffdir = os.path.abspath(os.path.join(base, "..", "..", ".."))
run2dir = os.path.abspath(os.path.join(base, "..", "..", "Run2"))

c1   = ("#scale[1.3]{#hat{ }}#kern[-0.8]{C}_{1} binning", os.path.join(ffdir, "Combine/aug26/runFits_C1reco_lumi300_kl_C1reco/profile1D.statonly.tutorial.root"), ROOT.kRed + 1, 1)
stxs3 = ("STXS Run 3", os.path.join(base, "runFits_ttHCats_Only_kl_STXScomparison/profile1D.statonly.tutorial.root"), ROOT.kBlue + 1, 1)
stxs2 = ("STXS Run 2", os.path.join(run2dir, "runFits_Run2_ttHCats_kl_STXScomparison_Run2/profile1D.statonly.tutorial.root"), ROOT.kGreen + 2, 1)

plots = [
    ("profile1D_statonly_STXS_vs_C1", [c1, stxs3]),
    ("profile1D_statonly_STXS_Run3_Run2_vs_C1", [c1, stxs3, stxs2]),
]

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

xlo, xhi, ymax = -20, 50, 3.

def make_plot(outname, scans):
    missing = [s for s in scans if not os.path.exists(s[1])]
    if missing:
        for s in missing: print("Skipping %s: %s not found (%s)" % (outname, s[0], s[1]))
        return

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

    line = ROOT.TLine(xlo, 1, xhi, 1); line.SetLineStyle(2); line.SetLineColor(ROOT.kGray + 2); line.Draw()

    # Legend at top right: one row per scan, label followed by its kappa_lambda value.
    # The text is drawn with TLatex (TLegend adds a gap before the super/subscripts)
    nrows = len(scans)
    lx1, lx2, ly2 = 0.50, 0.96, 0.925
    ly1 = ly2 - 0.075 * nrows
    leg = ROOT.TLegend(lx1, ly1, lx2, ly2)
    leg.SetBorderSize(0); leg.SetFillStyle(0); leg.SetTextSize(0.037); leg.SetMargin(0.16)
    vals = []
    keep = [frame, line]
    for label, path, col, style in scans:
        f = ROOT.TFile.Open(path)
        g = f.Get("profile1D.statonly.tutorial").Clone(label)
        g.SetLineColor(col); g.SetLineWidth(3); g.SetLineStyle(style)
        g.Draw("L SAME")
        xmin, lo, hi = crossings(g)
        txt = "#kappa_{#lambda}: %.2f" % xmin
        if lo is not None and hi is not None:
            txt += "^{+%.2f}_{-%.2f}" % (hi - xmin, xmin - lo)
        print(outname, label, xmin, lo, hi)
        leg.AddEntry(g, " ", "l")
        vals.append((label, txt))
        for xc in (lo, hi):
            if xc is not None:
                v = ROOT.TLine(xc, 0, xc, 1); v.SetLineColor(col); v.SetLineStyle(3); v.Draw(); keep.append(v)
        keep += [f, g]
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
    lat.SetTextFont(42); lat.SetTextSize(0.037); lat.SetTextAlign(31); lat.DrawLatex(0.975, 0.95, "Stat-only, 300 fb#kern[-0.55]{^{-1}}")

    c.RedrawAxis()
    out = os.path.join(base, outname)
    for ext in ("png", "pdf"):
        c.SaveAs("%s.%s" % (out, ext))

for outname, scans in plots:
    make_plot(outname, scans)
