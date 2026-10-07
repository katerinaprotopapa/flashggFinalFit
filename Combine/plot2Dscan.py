import ROOT
from scipy.interpolate import RegularGridInterpolator
import numpy as np

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

file_name = "incl.root" # found in runFits_C1reco_muttH_klambda dir

# Luminosity label: card lumi (2022-2025, sum of lumiMap in tools/commonObjects.py) times the lumi_scale used in the fit
card_lumi = 282.64 # fb^-1
lumi_scale = 1.0 # must match --setParameters lumi_scale in inputs_tutorial_profile2D_syst.json
f = ROOT.TFile(file_name)
t = f.Get("limit")

# Number of bins in plot
n_bins = 45

# quantileExpected == -1 rows are the per-job best-fit snapshot (one duplicate
# per split condor job, all echoing the same combine-determined minimum) - pull
# the true bestfit coordinates from here rather than from the grid
# interpolation below, then exclude them so the grid reshape stays clean
bf_kl, bf_mu = None, None
x, y, deltaNLL = [], [], []
for ev in t:
    if ev.quantileExpected == -1:
        if bf_kl is None:
            bf_kl, bf_mu = getattr(ev, "k_lambda"), getattr(ev, "mu_ttH")
        continue
    x.append(getattr(ev, "k_lambda"))
    y.append(getattr(ev, "mu_ttH"))
    deltaNLL.append(getattr(ev, "deltaNLL"))
assert bf_kl is not None, "no quantileExpected == -1 bestfit row found in tree"

# Plot only out to the actual extent of the scanned grid - the combine grid
# (with --alignEdges) can fall a bit short of the --setParameterRanges bounds,
# and plotting past the last scanned point leaves a gap with no interpolated
# data, which the "fill empty bins with 999" step below then paints in as a
# solid, misleadingly bright band at the edge of the z-axis palette.
x_range = [min(x), max(x)]
y_range = [min(y), max(y)]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Do interpolation
# The scanned points already sit on a regular (k_lambda, mu_ttH) grid, so
# interpolate on that grid directly (RegularGridInterpolator, tensor-product
# bilinear) rather than re-triangulating them as scattered points
# (scipy.griddata): Delaunay-triangulation-based interpolation of a rotated,
# narrow likelihood valley creates spurious kinks/creases in the contours that
# aren't present in the underlying scan, because the triangulation picks an
# arbitrary diagonal through each grid cell. Higher-order grid methods
# (cubic/pchip) avoid that too, but scipy's implementation is too slow to
# evaluate over the ~1M-point plotting mesh below.
kl_vals = np.array(sorted(set(x)))
mu_vals = np.array(sorted(set(y)))
kl_index = {v: i for i, v in enumerate(kl_vals)}
mu_index = {v: i for i, v in enumerate(mu_vals)}
z_grid = np.full((len(kl_vals), len(mu_vals)), np.nan)
for xi, yi, zi in zip(x, y, deltaNLL):
    z_grid[kl_index[xi], mu_index[yi]] = zi
assert not np.isnan(z_grid).any(), "missing point(s) in the (k_lambda, mu_ttH) scan grid"

interp = RegularGridInterpolator((kl_vals, mu_vals), z_grid, method="linear", bounds_error=False, fill_value=np.nan)

# Define histogram and fill each bin directly from the interpolator, evaluated
# once at the bin center. A TProfile2D filled from a dense mesh of
# interpolated points and averaged down to display resolution was considered
# instead: averaging the (convex, curved-near-the-minimum) -2*deltaNLL surface
# over a bin's area isn't exactly equal to its value at the bin center, and
# evaluating directly at the center avoids that bias as well as the cost of
# generating and averaging a ~1M-point mesh.
h2D = ROOT.TH2D("h", "h", n_bins, x_range[0], x_range[1], n_bins, y_range[0], y_range[1])

for ibin in range(1, h2D.GetNbinsX() + 1):
    for jbin in range(1, h2D.GetNbinsY() + 1):
        xc = h2D.GetXaxis().GetBinCenter(ibin)
        yc = h2D.GetYaxis().GetBinCenter(jbin)
        v = interp(np.array([[xc, yc]]))[0]
        # Factor of 2 comes from 2*NLL. Bin centers outside the scanned grid's
        # convex hull (shouldn't occur here since x_range/y_range are set to
        # that exact hull, but kept as a defensive fallback) come back NaN
        # from interp - mark those excluded (999) rather than leaving the
        # TH2D default of 0, which would be misread as the best-fit minimum.
        h2D.SetBinContent(ibin, jbin, 999 if np.isnan(v) else 2 * v)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Set up canvas
canv = ROOT.TCanvas("canv", "canv", 600, 600)
canv.SetTickx()
canv.SetTicky()
canv.SetLeftMargin(0.115)
canv.SetRightMargin(0.16)
canv.SetBottomMargin(0.115)
# Extract binwidth
xw = (x_range[1] - x_range[0]) / n_bins
yw = (y_range[1] - y_range[0]) / n_bins

# Set histogram properties
h2D.SetContour(999)
h2D.SetTitle("")
h2D.GetXaxis().SetTitle(r"#kappa_{#lambda}")
h2D.GetXaxis().SetTitleSize(0.05)
h2D.GetXaxis().SetTitleOffset(0.9)
h2D.GetXaxis().SetRangeUser(x_range[0], x_range[1] - xw)

h2D.GetYaxis().SetTitle(r"#mu_{ttH} #scale[0.8]{(norm)}")
h2D.GetYaxis().SetTitleSize(0.05)
h2D.GetYaxis().SetTitleOffset(0.9)
h2D.GetYaxis().SetRangeUser(y_range[0], y_range[1] - yw)

h2D.GetZaxis().SetTitle("-2 #Delta ln L")
h2D.GetZaxis().SetTitleSize(0.05)
h2D.GetZaxis().SetTitleOffset(0.9)

h2D.SetMaximum(50)

# Make confidence interval contours
c68, c95 = h2D.Clone(), h2D.Clone()
c68.SetContour(2)
c68.SetContourLevel(1, 2.3)
c68.SetLineWidth(3)
c68.SetLineColor(ROOT.kBlack)
c95.SetContour(2)
c95.SetContourLevel(1, 5.99)
c95.SetLineWidth(3)
c95.SetLineStyle(2)
c95.SetLineColor(ROOT.kBlack)

# Draw histogram and contours
h2D.Draw("COLZ")

# Draw lines for SM point
vline = ROOT.TLine(1, y_range[0], 1, y_range[1] - yw)
vline.SetLineColorAlpha(ROOT.kGray, 0.5)
vline.Draw("Same")
hline = ROOT.TLine(x_range[0], 1, x_range[1] - xw, 1)
hline.SetLineColorAlpha(ROOT.kGray, 0.5)
hline.Draw("Same")

# Draw contours
c68.Draw("cont3same")
c95.Draw("cont3same")

# Make best fit and sm points
gSM = ROOT.TGraph()
gSM.SetPoint(0, 1, 1)
gSM.SetMarkerStyle(33)
gSM.SetMarkerSize(3)
gSM.SetMarkerColor(ROOT.kRed)
gSM.Draw("P")

gBF = ROOT.TGraph()
gBF.SetPoint(0, bf_kl, bf_mu)
gBF.SetMarkerStyle(34)
gBF.SetMarkerSize(2)
gBF.SetMarkerColor(ROOT.kBlack)
gBF.Draw("P")


# Add legend
leg = ROOT.TLegend(0.67, 0.15, 0.87, 0.35)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.AddEntry(gBF, "Best fit", "P")
leg.AddEntry(c68, "1#sigma CL", "L")
leg.AddEntry(c95, "2#sigma CL", "L")
leg.AddEntry(gSM, "SM", "P")
leg.Draw()

lat = ROOT.TLatex(); lat.SetNDC(); lat.SetTextFont(42); lat.SetTextSize(0.037); lat.SetTextAlign(31)
lat.DrawLatex(1 - canv.GetRightMargin(), 1 - canv.GetTopMargin() + 0.015, "%.1f fb#kern[-0.55]{^{-1}} (13.6 TeV)" % (card_lumi * lumi_scale))

canv.Update()
canv.SaveAs("scan2D_k_lambda_vs_mu_ttH.png")
