import ROOT
import json
import numpy as np

# Definitions
num_points = 100
categories_json = "/vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Trees2WS/config_categories_kl.json"

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptTitle(0) # hiding the default box title for a cleaner look

# Workspace
f = ROOT.TFile.Open("Datacard_kl_k_lambda.root")
w = f.Get("w")

# k_lambda - my POI
kl = w.var("k_lambda")
kl_min, kl_max = kl.getMin(), kl.getMax()

# categories
with open(categories_json, 'r') as f_in:
    categories_dict = json.load(f_in)
categories = list(categories_dict["cat_dict"].values())

colors = [
    ROOT.kAzure+7,   # Bright Blue
    ROOT.kOrange+7,  # Deep Orange
    ROOT.kSpring+9,  # Strong Green
    ROOT.kRed+1,     # Rich Red
    ROOT.kViolet-3,  # Purple
    ROOT.kTeal-1,    # Dark Cyan
    ROOT.kPink+1,    # Dark Pink
    ROOT.kYellow+2,  # Mustard/Gold
    ROOT.kGray+3,    # Deep Charcoal
    ROOT.kOrange-3   # Vibrant Sunset 
]
# scans
def get_scan(func_prefix, cats):
    scan = {}
    for i, cat in enumerate(cats):
        g = ROOT.TGraph()
        color = colors[i % len(colors)]
        g.SetLineColor(color)
        g.SetLineWidth(2)
        scan[cat] = g
    for i in range(num_points):
        val = kl_min + i * (kl_max - kl_min) / (num_points - 1)
        kl.setVal(val)
        for cat in cats:
            if func_prefix == "XSscal":
                fname = f"{func_prefix}_{cat}"
            elif func_prefix == "BRscal":
                fname = f"{func_prefix}_hgg" # only for Hgg so far
            elif func_prefix == "XSBRscal":
                fname = f"{func_prefix}_{cat}_hgg"
            func = w.function(fname)
            if func:
                scan[cat].SetPoint(i, val, func.getVal())
    return scan
xs_graphs = get_scan("XSscal", categories)
br_graphs = get_scan("BRscal", ["hgg"])
xsbr_graphs = get_scan("XSBRscal", categories)

# Plotting
c = ROOT.TCanvas("c", "mu_vs_kl", 1500, 500)
c.SetLeftMargin(0.12)   # Same left margin for all pads
c.SetRightMargin(0.05)  # Keep a small right margin for all pads
c.SetTopMargin(0.05)    # Small margin at the top for all pads
c.SetBottomMargin(0.12) # Small margin at the bottom for all pads
c.Divide(3, 1, 0, 0)

# style
def style_axis(item, xtitle, ytitle, size=0.05):
    item.GetXaxis().SetTitle(xtitle)
    item.GetYaxis().SetTitle(ytitle)
    item.GetXaxis().SetTitleSize(size)
    item.GetYaxis().SetTitleSize(size)
    item.GetXaxis().SetLabelSize(size)
    item.GetYaxis().SetLabelSize(size)
    item.GetXaxis().SetTitleOffset(1.5)
    item.GetYaxis().SetTitleOffset(1.5)

# SM reference lines
# mu=1
line_h = ROOT.TLine(kl_min, 1, kl_max, 1)
line_h.SetLineStyle(3)
line_h.SetLineColor(ROOT.kGray+2)
# kl=1
line_v = ROOT.TLine(1, 0, 1, 1.2)
line_v.SetLineStyle(3)
line_v.SetLineColor(ROOT.kGray+2)

# Left: XS
p1 = c.cd(1)
ROOT.gPad.SetLeftMargin(0.15)
# p1.SetLeftMargin(0.15)   # Keep this for the Y-axis title
# p1.SetRightMargin(0.1)  # Reduce gap to Pad 2
ROOT.gPad.SetLeftMargin(0.17)   # Consistent left margin for pad 1
ROOT.gPad.SetRightMargin(0.09)  # Consistent right margin for pad 1
ROOT.gPad.SetBottomMargin(0.15) # Bottom margin
ROOT.gPad.SetTopMargin(0.05)    # Top margin
mg_xs = ROOT.TMultiGraph()
leg_xs = ROOT.TLegend(0.7, 0.69, 0.95, 1.0)
leg_xs.SetTextSize(0.03)
leg_xs.SetFillColor(ROOT.kWhite)
leg_xs.SetFillStyle(1001) # 1001 is the code for "solid fill"
leg_xs.SetBorderSize(1)

for cat, g in xs_graphs.items():
    mg_xs.Add(g, "L")
    leg_xs.AddEntry(g, cat, "L")

mg_xs.Draw("A")
mg_xs.SetMinimum(-0.6)
mg_xs.SetMaximum(1.6)
style_axis(mg_xs, "#kappa_{#lambda}", "#mu_{#sigma}")
line_h.Draw()
line_v.DrawLine(1, ROOT.gPad.GetUymin(), 1, ROOT.gPad.GetUymax())
leg_xs.Draw()

# Middle: BR
p2 = c.cd(2)
# p2.SetLeftMargin(0.15)   # Reduced from 0.22 since it's now closer to Pad 1
# p2.SetRightMargin(0.1)  # Reduce gap to Pad 3
ROOT.gPad.SetLeftMargin(0.15)   # Consistent left margin for pad 1
ROOT.gPad.SetRightMargin(0.08)  # Consistent right margin for pad 1
ROOT.gPad.SetBottomMargin(0.15) # Bottom margin
ROOT.gPad.SetTopMargin(0.05)    # Top margin
br_g = br_graphs["hgg"]
br_g.SetLineColor(ROOT.kBlack)
br_g.Draw("AL")
style_axis(br_g, "#kappa_{#lambda}", "#mu_{BR}")

ROOT.gPad.Update()
leg_br = ROOT.TLegend(0.2, 0.8, 0.4, 0.9)
leg_br.SetTextSize(0.045)
leg_br.SetBorderSize(0)
leg_br.AddEntry(br_g, "H #rightarrow #gamma#gamma", "L")
line_h.Draw()
line_v.DrawLine(1, ROOT.gPad.GetUymin(), 1, ROOT.gPad.GetUymax())
leg_br.Draw()

# Right: XS * BR
p3 = c.cd(3)
# p3.SetLeftMargin(0.15)   # Reduced gap from Pad 2
# p3.SetRightMargin(0.1)  # Small margin at the far right edge
ROOT.gPad.SetLeftMargin(0.14)   # Consistent left margin for pad 1
ROOT.gPad.SetRightMargin(0.08)  # Consistent right margin for pad 1
ROOT.gPad.SetBottomMargin(0.15) # Bottom margin
ROOT.gPad.SetTopMargin(0.05)    # Top margin
mg_xsbr = ROOT.TMultiGraph()
leg_xsbr = ROOT.TLegend(0.7, 0.69, 0.95, 1.0)
leg_xsbr.SetTextSize(0.03)
leg_xsbr.SetFillColor(ROOT.kWhite)
leg_xsbr.SetFillStyle(1001) # 1001 is the code for "solid fill"
leg_xsbr.SetBorderSize(1)

for cat_hgg in categories:
    g = xsbr_graphs[cat_hgg]
    mg_xsbr.Add(g, "L")
    # Use original cat name for legend
    leg_xsbr.AddEntry(g, cat_hgg.replace("_hgg",""), "L")

mg_xsbr.Draw("A")
mg_xsbr.SetMinimum(-0.6)
mg_xsbr.SetMaximum(1.6)
style_axis(mg_xsbr, "#kappa_{#lambda}", "#mu_{#sigma #times BR}")
line_h.Draw()
line_v.DrawLine(1, ROOT.gPad.GetUymin(), 1, ROOT.gPad.GetUymax())
leg_xsbr.Draw()

c.SaveAs("mu_vs_kl.png")
c.SaveAs("mu_vs_kl.pdf")
print("Done! Saved to mu_vs_kl.png")