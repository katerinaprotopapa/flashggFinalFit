import ROOT
from scipy.interpolate import RegularGridInterpolator
import numpy as np

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

file_name = "incl.root" # found in runFits_C1reco_lumi300_kl_C1reco dir
f = ROOT.TFile(file_name)
t = f.Get("limit")

# Number of points in interpolation
n_points = 1000

# Number of bins in plot
n_bins = 45

# quantileExpected == -1 rows are the per-job best-fit snapshot, not part of
# the scanned (k_lambda, mu_ttH) grid - exclude them so the grid reshape below is clean
x, y, deltaNLL = [], [], []
for ev in t:
    if ev.quantileExpected == -1:
        continue
    x.append(getattr(ev, "k_lambda"))
    y.append(getattr(ev, "mu_ttH"))
    deltaNLL.append(getattr(ev, "deltaNLL"))

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

# Set up grid, restricted to the convex hull of the actual scan (points outside
# get NaN from interp and are dropped below, same as the old griddata behaviour)
grid_x, grid_y = np.mgrid[x_range[0] : x_range[1] : n_points * 1j, y_range[0] : y_range[1] : n_points * 1j]
grid_vals = interp(np.stack([grid_x.ravel(), grid_y.ravel()], axis=-1)).reshape(grid_x.shape)

# Remove NANS
grid_x = grid_x[grid_vals == grid_vals]
grid_y = grid_y[grid_vals == grid_vals]
grid_vals = grid_vals[grid_vals == grid_vals]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define Profile2D histogram
h2D = ROOT.TProfile2D("h", "h", n_bins, x_range[0], x_range[1], n_bins, y_range[0], y_range[1])

for i in range(len(grid_vals)):
    # Factor of 2 comes from 2*NLL
    h2D.Fill(grid_x[i], grid_y[i], 2 * grid_vals[i])

# Loop over bins: if content = 0 then set 999
for ibin in range(1, h2D.GetNbinsX() + 1):
    for jbin in range(1, h2D.GetNbinsY() + 1):
        if h2D.GetBinContent(ibin, jbin) == 0:
            xc = h2D.GetXaxis().GetBinCenter(ibin)
            yc = h2D.GetYaxis().GetBinCenter(jbin)
            h2D.Fill(xc, yc, 999)

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
gBF.SetPoint(0, grid_x[np.argmin(grid_vals)], grid_y[np.argmin(grid_vals)])
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

canv.Update()
canv.SaveAs("scan2D_k_lambda_vs_mu_ttH_lumi300.png")
