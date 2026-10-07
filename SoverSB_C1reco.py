"""
Compute S/(S+B) in the +-1 sigma_eff window around the peak (mH=125GeV) for each analysis category
breakdown by Higgs production mode
"""

import re
import csv
import ROOT

from Plots.plottingTools

ROOT.gROOT.SetBatch(True)


def getEffSigma(_h):
    # sigma_eff: smallest window containing 68.3% of the distribution
    nbins, binw, xmin = _h.GetXaxis().GetNbins(), _h.GetXaxis().GetBinWidth(1), _h.GetXaxis().GetXmin()
    mu, rms, total = _h.GetMean(), _h.GetRMS(), _h.Integral()
    nWindow = int(rms / binw) if (rms / binw) < 0.1 * nbins else int(0.1 * nbins)
    rlim = 0.683 * total
    wmin, iscanmin = 9999999, -999
    for iscan in range(-1 * nWindow, nWindow + 1):
        i_centre = int((mu - xmin) / binw + 1 + iscan)
        x_centre = (i_centre - 0.5) * binw + xmin
        x_up, x_down = x_centre, x_centre
        i_up, i_down = i_centre, i_centre
        y = _h.GetBinContent(i_centre)
        r = y
        reachedLimit = False
        for j in range(1, nbins):
            if reachedLimit:
                continue
            if (i_up < nbins) & (not reachedLimit):
                i_up += 1
                x_up += binw
                y = _h.GetBinContent(i_up)
                r += y
                if r > rlim:
                    reachedLimit = True
            else:
                print(" --> Reach nBins in effSigma calc: %s. Returning 0 for effSigma" % _h.GetName())
                return 0
            if reachedLimit:
                continue
            if (i_down > 1) & (not reachedLimit):
                i_down -= 1
                x_down -= binw
                y = _h.GetBinContent(i_down)
                r += y
                if r > rlim:
                    reachedLimit = True
            else:
                print(" --> Reach 0 in effSigma calc: %s. Returning 0 for effSigma" % _h.GetName())
                return 0
        if reachedLimit:
            wscan = x_up - x_down
            if wscan < wmin:
                wmin = wscan
                iscanmin = iscan
    return 0.5 * wmin

MASS = 125.0
SQRTS = "13p6TeV"
PDF_NBINS = 3200

# One (category, signal_file, background_file) tuple per category.
# ASSUMPTION: file paths guessed from your original docstring -- fix these
# to your real directory layout, and extend with the rest of your categories.
CATEGORIES = [
    dict(
        cat="hadr_C1_10_21",
        sig_file=f"Signal/outdir_packaged_C1reco/CMS-HGG_sigfit_packaged_C1reco_{cat}.root",
        sig_ws="wsig_13p6TeV",
        bkg_file=f"Background/outdir_kl_C1reco/CMS-HGG_multipdf_{cat}.root",
        bkg_ws="multipdf",
    ),
]

# Era tags that can appear appended to a raw process token.
# ASSUMPTION: complete list of eras used across all your categories.
ERA_TAGS = ["preEE", "postEE", "preBPix", "postBPix", "2024"]

# Map raw process tokens (after stripping the era suffix) to a Higgs
# production-mode column. ASSUMPTION: this is the grouping you want.
PROCESS_GROUP = {
    "GG2H": "ggH",
    "VBF": "VBF",
    "TTH": "ttH",
    "ZH2HLL": "ZH", "ZH2HQQ": "ZH", "ZH2HNUNU": "ZH", "ZH": "ZH",
    "WPLUSH2HQQ": "WH", "WPLUSH2HLNU": "WH", "WPLUSH": "WH",
    "WMINUSH2HQQ": "WH", "WMINUSH2HLNU": "WH", "WMINUSH": "WH",
}
PROD_MODE_COLUMNS = ["ggH", "VBF", "ZH", "WH", "ttH"]

rows = []

for cfg in CATEGORIES:
    cat = cfg["cat"]
    print("=" * 100)
    print("Category:", cat)

    # ---- open workspaces ----
    fsig = ROOT.TFile.Open(cfg["sig_file"])
    wsig = fsig.Get(cfg["sig_ws"])
    fbkg = ROOT.TFile.Open(cfg["bkg_file"])
    wbkg = fbkg.Get(cfg["bkg_ws"])

    xvar = wsig.var("CMS_hgg_mass")
    xvar.SetTitle("m_{#gamma#gamma}")
    xvar.setUnit("GeV")
    xvar_argset = ROOT.RooArgSet(xvar)
    wsig.var("MH").setVal(MASS)

    # Background lives in a separate workspace/file with its own
    # CMS_hgg_mass instance -- keep a second handle for it.
    xvar_bkg = wbkg.var("CMS_hgg_mass")
    xvar_bkg.SetTitle("m_{#gamma#gamma}")
    xvar_bkg.setUnit("GeV")
    xvar_bkg_argset = ROOT.RooArgSet(xvar_bkg)

    # ---- find every extended, lumi-scaled per-(process,era) signal pdf ----
    pattern = re.compile(
        r"^extendhggpdfsmrel_(?P<proc_era>.+)_%s_%sThisLumi$" % (re.escape(cat), re.escape(SQRTS))
    )
    components = []  # list of dicts: proc, era, group, pdf (RooExtendPdf)
    for pdf in wsig.allPdfs():
        m = pattern.match(pdf.GetName())
        if not m:
            continue
        proc_era = m.group("proc_era")
        proc, era = proc_era, None
        for e in ERA_TAGS:
            if proc_era.endswith("_" + e):
                proc, era = proc_era[: -len(e) - 1], e
                break
        group = PROCESS_GROUP.get(proc)
        if group is None:
            print("  !! WARNING: no PROCESS_GROUP entry for raw process '%s' "
                  "(from '%s') -- treating as its own group." % (proc, pdf.GetName()))
            group = proc
        components.append({"proc": proc, "era": era, "group": group, "pdf": pdf})

    if not components:
        raise RuntimeError("No signal components found for category %s -- check "
                            "naming assumptions (SQRTS='%s')" % (cat, SQRTS))
    print("  Found %d signal (process, era) components" % len(components))

    # ---- combined total signal pdf = RooAddPdf of ALL extended components.
    # Being a sum of extended pdfs, it is itself extended: its
    # expectedEvents() is the fit-computed total signal yield (not a
    # histogram sum), and its density is already yield-weighted internally,
    # so createHistogram() gives the correct total-signal shape directly. ----
    total_list = ROOT.RooArgList()
    for c in components:
        total_list.add(c["pdf"])
    sig_total_pdf = ROOT.RooAddPdf("sigAdd_total_%s" % cat, "total signal pdf", total_list)

    S_tot = sig_total_pdf.expectedEvents(xvar_argset)
    h_S = sig_total_pdf.createHistogram("h_S_%s" % cat, xvar, ROOT.RooFit.Binning(PDF_NBINS))
    effSigma = getEffSigma(h_S)

    rangeName = "effSigma_%s" % cat
    xvar.setRange(rangeName, MASS - effSigma, MASS + effSigma)
    xvar_bkg.setRange(rangeName, MASS - effSigma, MASS + effSigma)

    # S_eff = integral of the combined signal fit over the window, times its
    # fit-computed total yield.
    S_eff = sig_total_pdf.createIntegral(xvar_argset, xvar_argset, rangeName).getVal() * S_tot

    # ---- same components, grouped by production mode -- only the total
    # yield per group is needed now (for the fraction-of-total column) ----
    group_yields = {}
    for group in set(c["group"] for c in components):
        glist = ROOT.RooArgList()
        for c in components:
            if c["group"] == group:
                glist.add(c["pdf"])
        gpdf = ROOT.RooAddPdf("sigAdd_%s_%s" % (group, cat), "signal pdf for %s" % group, glist)
        group_yields[group] = gpdf.expectedEvents(xvar_argset)

    # ---- background: envelope member currently selected by pdfindex.
    # Yield is the fitted RooRealVar '<bkgshape>_norm', used as-is -- no
    # lumi rescale (confirmed: not needed here), even though the workspace
    # also carries an 'IntLumi' var. ----
    bkgshape_name = "CMS_hgg_%s_%s_bkgshape" % (cat, SQRTS)
    multipdf = wbkg.pdf(bkgshape_name)
    if multipdf is None:
        raise RuntimeError("Could not find RooMultiPdf '%s' in workspace" % bkgshape_name)
    bpdf = multipdf.getCurrentPdf()

    bnorm = wbkg.var("%s_norm" % bkgshape_name)
    B_tot = bnorm.getVal()

    pdfindex_cat = wbkg.cat("pdfindex_%s_%s" % (cat, SQRTS))
    print("  Background: current envelope member = '%s' (pdfindex=%s), B_tot=%.3f"
          % (bpdf.GetName(), pdfindex_cat.getIndex() if pdfindex_cat else "?", B_tot))

    B_eff = bpdf.createIntegral(xvar_bkg_argset, xvar_bkg_argset, rangeName).getVal() * B_tot

    SoverSplusB = S_eff / (S_eff + B_eff)

    row = {"cat": cat, "S_tot": S_tot, "S_eff": S_eff, "SoverSplusB": SoverSplusB}
    for g in PROD_MODE_COLUMNS:
        row["frac_%s" % g] = group_yields.get(g, 0.0) / S_tot
    # flag any groups that showed up but weren't in PROD_MODE_COLUMNS
    for g in set(group_yields) - set(PROD_MODE_COLUMNS):
        row["frac_%s" % g] = group_yields[g] / S_tot

    rows.append(row)

# ---- print + save ----
header = ["cat", "S_tot"] + ["frac_%s" % g for g in PROD_MODE_COLUMNS] + ["S_eff", "SoverSplusB"]
header += sorted(set(k for r in rows for k in r) - set(header))

print()
print(("{:<16}" + "{:>12}" * (len(header) - 1)).format(*header))
for r in rows:
    print(("{:<16}" + "{:>12.4f}" * (len(header) - 1)).format(
        *[r["cat"]] + [r.get(f, 0.0) for f in header[1:]]))

outname = "SoverSplusB_C1reco_fromFits.csv"
with open(outname, "w", newline="") as fout:
    writer = csv.DictWriter(fout, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)
print("\nSaved: %s" % outname)