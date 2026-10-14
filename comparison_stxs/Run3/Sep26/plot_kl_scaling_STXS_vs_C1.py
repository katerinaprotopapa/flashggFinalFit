# Yield scaling mu_ttH(kappa_lambda) = XS(kl) * BR_gg(kl) for the highest-C1 (most sensitive, solid) and
# lowest-C1 (least sensitive, dashed) categories of the C1 binning (reco categories) and the STXS binning
# (ttH gen processes), using the C1 JSONs from TrilinearCouplingModels.py
import ROOT
import os
import json

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLineStyleString(11, "40 25")  # long dashes for the least sensitive categories

base = os.path.dirname(os.path.abspath(__file__))
datadir = os.path.join(os.environ["CMSSW_BASE"], "src/HiggsAnalysis/CombinedLimit/data/trilinearHiggsModel")

def load(name):
    with open(os.path.join(datadir, name)) as f:
        d = json.load(f)
    return {k: v for k, v in d.items() if k.lower() != "background"}

dZH = -1.536e-3
C1_BR, cGTot = 0.49e-2, 2.5e-3

# Same expressions as TrilinearHiggsDifferential_ttH(_STXScomparison)
def mu(kl, c1):
    xs = (1 + kl * c1 + dZH) / ((1 - (kl * kl - 1) * dZH) * (1 + c1 + dZH))
    br = 1 + (kl - 1) * (C1_BR - cGTot) / (1 + (kl - 1) * cGTot)
    return xs * br

# Hand-built sub/superscripts: TLatex's _{} / ^{} leave a gap after the base letter
C1 = "#kern[0]{(C}#lower[0.3]{#scale[0.7]{1}}"  # includes the opening bracket, to avoid a gap after it
C1hat = "#scale[1.3]{#hat{ }}#kern[-0.8]{C}#lower[0.3]{#scale[0.7]{1}}"
pTH = "p#kern[-0.1]{#lower[0.3]{#scale[0.7]{T}}}#kern[-0.6]{#lower[-0.6]{#scale[0.7]{H}}}"
labels = {
    "lept_C1_GT_70": "leptonic, %s > 0.070" % C1hat, "hadr_C1_LT_10": "hadronic, %s < 0.010" % C1hat,
    "TTH_PTH_0_60": "%s 0-60 GeV" % pTH, "TTH_PTH_GT300": "%s > 300 GeV" % pTH,
}
c1lab = "%s binning" % C1hat

c1_cats = load("C1_gen_avg_cat_C1_reco.json")
stxs_cats = load("C1_gen_avg_cat_C1_reco_STXScomparison.json")
hi = lambda cats: max(cats.items(), key=lambda kv: kv[1])
lo = lambda cats: min(cats.items(), key=lambda kv: kv[1])

# (binning label, (category, C1), colour, line style)
curves = [
    (c1lab, hi(c1_cats), ROOT.kRed + 1, 1),
    (c1lab, lo(c1_cats), ROOT.kRed + 1, 11),
    ("STXS", hi(stxs_cats), ROOT.kBlue + 1, 1),
    ("STXS", lo(stxs_cats), ROOT.kBlue + 1, 11),
]

# Coarse enough sampling that the dash pattern is visible (ROOT restarts it on every segment)
xlo, xhi, npt = -15, 50, 131

graphs = []
for blab, (name, c1v), col, sty in curves:
    print(name, c1v)
    g = ROOT.TGraph(npt)
    for i in range(npt):
        kl = xlo + (xhi - xlo) * i / (npt - 1)
        g.SetPoint(i, kl, mu(kl, c1v))
    g.SetLineColor(col); g.SetLineStyle(sty); g.SetLineWidth(3 if sty == 1 else 2)
    graphs.append(("%s: %s %s = %.3f)" % (blab, labels.get(name, name), C1, c1v), g))

c = ROOT.TCanvas("c", "c", 750, 650)
c.SetLeftMargin(0.13); c.SetBottomMargin(0.115); c.SetRightMargin(0.025); c.SetTopMargin(0.06)
c.SetGridx(); c.SetGridy()
ytop = max(g.GetY()[i] for _, g in graphs for i in range(npt))
frame = ROOT.TH1F("frame", "", 100, xlo, xhi)
frame.SetMinimum(0); frame.SetMaximum(ytop * 1.5)
frame.GetXaxis().SetTitle("#kappa_{#lambda}")
frame.GetYaxis().SetTitle("#mu_{ttH}")
frame.GetXaxis().SetTitleSize(0.05); frame.GetYaxis().SetTitleSize(0.05)
frame.GetXaxis().SetLabelSize(0.045); frame.GetYaxis().SetLabelSize(0.045)
frame.GetYaxis().SetTitleOffset(1.2); frame.GetXaxis().SetTitleOffset(0.95)
frame.Draw()

one = ROOT.TLine(xlo, 1, xhi, 1); one.SetLineColor(ROOT.kGray + 2); one.SetLineStyle(3); one.Draw()

# The PNG backend restarts the dash pattern on every graph segment, so dashed curves are drawn as solid
# pieces cut by arc length in pad-fraction units (dash on/off lengths below)
dash_on, dash_off = 0.030, 0.018
ymin_f, ymax_f = frame.GetMinimum(), frame.GetMaximum()
def draw_dashed(g):
    pieces, cur, s, on = [], [], 0., True
    px = lambda x: (x - xlo) / (xhi - xlo)
    py = lambda y: (y - ymin_f) / (ymax_f - ymin_f) * 650. / 750.  # canvas aspect ratio
    xs = [g.GetX()[i] for i in range(g.GetN())]
    ys = [g.GetY()[i] for i in range(g.GetN())]
    # Subdivide finely so the cut points land accurately
    fx, fy = [], []
    for i in range(len(xs) - 1):
        for j in range(10):
            t = j / 10.
            fx.append(xs[i] + t * (xs[i + 1] - xs[i])); fy.append(ys[i] + t * (ys[i + 1] - ys[i]))
    fx.append(xs[-1]); fy.append(ys[-1])
    cur = [(fx[0], fy[0])]
    for i in range(1, len(fx)):
        s += ((px(fx[i]) - px(fx[i - 1])) ** 2 + (py(fy[i]) - py(fy[i - 1])) ** 2) ** 0.5
        if on: cur.append((fx[i], fy[i]))
        if s >= (dash_on if on else dash_off):
            if on: pieces.append(cur)
            on, s, cur = not on, 0., [(fx[i], fy[i])]
    if on and len(cur) > 1: pieces.append(cur)
    out = []
    for pc in pieces:
        p = ROOT.TGraph(len(pc))
        for k, (x, y) in enumerate(pc): p.SetPoint(k, x, y)
        p.SetLineColor(g.GetLineColor()); p.SetLineWidth(g.GetLineWidth()); p.Draw("L SAME")
        out.append(p)
    return out

keep = []
for _, g in graphs:
    if g.GetLineStyle() == 1:
        g.Draw("L SAME")
    else:
        keep += draw_dashed(g)

# Legend: TLegend only draws the line samples; the text is TLatex (TLegend adds a gap before sub/superscripts)
lx1, lx2, ly2, rowh = 0.30, 0.96, 0.925, 0.05
ly1 = ly2 - rowh * len(graphs)
leg = ROOT.TLegend(lx1, ly1, lx2, ly2)
leg.SetBorderSize(0); leg.SetFillStyle(0); leg.SetMargin(0.12)
for lab, g in graphs:
    leg.AddEntry(g, " ", "l")
leg.Draw()
tlat = ROOT.TLatex(); tlat.SetNDC(); tlat.SetTextFont(42); tlat.SetTextSize(0.032); tlat.SetTextAlign(12)
for i, (lab, g) in enumerate(graphs):
    tlat.DrawLatex(lx1 + leg.GetMargin() * (lx2 - lx1) + 0.01, ly2 - (i + 0.5) * rowh, lab)

lat = ROOT.TLatex(); lat.SetNDC()
lat.SetTextFont(62); lat.SetTextSize(0.06); lat.DrawLatex(0.16, 0.87, "CMS")
lat.SetTextFont(52); lat.SetTextSize(0.045); lat.DrawLatex(0.16, 0.82, "Internal")
lat.SetTextFont(42); lat.SetTextSize(0.037); lat.SetTextAlign(31)
lat.DrawLatex(0.975, 0.95, "13.6 TeV")

c.RedrawAxis()
out = os.path.join(base, "kl_scaling_STXS_vs_C1")
for ext in ("png", "pdf"):
    c.SaveAs("%s.%s" % (out, ext))
