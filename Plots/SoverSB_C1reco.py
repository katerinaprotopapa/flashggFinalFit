"""
Compute S/(S+B) in the +-1 sigma_eff window around the peak (mH=125GeV) for each analysis category
breakdown by Higgs production mode
"""

import re
import csv
import ROOT

ROOT.gROOT.SetBatch(True)

from plottingTools import getEffSigma # smallest window containing 68.3% of the distribution
from commonObjects import lumiMap, lumiScaleFactor # real per-era luminosity (fb^-1) + pb->fb unit conversion factor

MASS = 125.0
SQRTS = "13p6TeV"
PDF_NBINS = 3200

CAT_NAMES = [
    "hadr_C1_LT_10",
    "hadr_C1_10_21",
    "hadr_C1_21_30",
    "hadr_C1_30_36",
    "hadr_C1_36_42",
    "hadr_C1_42_63",
    "hadr_C1_GT_63",
    "lept_C1_LT_15",
    "lept_C1_15_30",
    "lept_C1_30_43",
    "lept_C1_43_63",
    "lept_C1_63_70",
    "lept_C1_GT_70"
]
CATEGORIES = [
    dict(
        cat=cat,
        sig_file=f"../Signal/outdir_packaged_C1reco/CMS-HGG_sigfit_packaged_C1reco_{cat}.root",
        sig_ws="wsig_13p6TeV",
        bkg_file=f"../Background/outdir_kl_C1reco/CMS-HGG_multipdf_{cat}.root",
        bkg_ws="multipdf",
    )
    for cat in CAT_NAMES
]

# era tags that appear in the naming
ERA_TAGS = ["preEE", "postEE", "preBPix", "postBPix", "2024"]

PROCESS_GROUP = {
    "GG2H": "ggH",
    "VBF": "VBF",
    "TTH": "ttH",
    "ZH2HLL": "ZH", "ZH2HQQ": "ZH", "ZH2HNUNU": "ZH", "ZH": "ZH",
    "WPLUSH2HQQ": "WH", "WPLUSH2HLNU": "WH", "WPLUSH": "WH",
    "WMINUSH2HQQ": "WH", "WMINUSH2HLNU": "WH", "WMINUSH": "WH",
}
PROD_MODE_COLUMNS = ["ggH", "VBF", "WH", "ZH", "ttH"]

rows = []
for cfg in CATEGORIES:
    cat = cfg["cat"]
    print("=" * 100)
    print("Category:", cat)

    # open workspaces
    # background
    print("[open] background file:", cfg["bkg_file"])
    fbkg = ROOT.TFile.Open(cfg["bkg_file"])
    wbkg = fbkg.Get(cfg["bkg_ws"])

    xvar_bkg = wbkg.var("CMS_hgg_mass")
    xvar_bkg.SetTitle("m_{#gamma#gamma}")
    xvar_bkg.setUnit("GeV")
    xvar_bkg_argset = ROOT.RooArgSet(xvar_bkg)

    # signal
    print("[open] signal file:", cfg["sig_file"])
    fsig = ROOT.TFile.Open(cfg["sig_file"])
    wsig = fsig.Get(cfg["sig_ws"])

    xvar = wsig.var("CMS_hgg_mass")
    xvar.SetTitle("m_{#gamma#gamma}")
    xvar.setUnit("GeV")
    xvar_argset = ROOT.RooArgSet(xvar)
    wsig.var("MH").setVal(MASS)

    # find every signal pdf (for each process, era)
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
            print("  !! WARNING: no PROCESS_GROUP entry for raw process '%s' (from '%s') -- treating as its own group." % (proc, pdf.GetName()))
            group = proc
        # print("  [match] pdf='%s'  ->  proc='%s' era='%s' group='%s'" % (pdf.GetName(), proc, era, group))
        components.append({"proc": proc, "era": era, "proc_era": proc_era, "group": group, "pdf": pdf})

    if not components:
        raise RuntimeError("No signal components found for category %s -- check naming assumptions (SQRTS='%s')" % (cat, SQRTS))
    print("[signal components] Found %d signal (process, era) components" % len(components))

    # sum of pdfs for each category (procs, eras)
    total_list = ROOT.RooArgList()
    component_yields = {}
    component_hcomps = {}
    h_S = None 
    for c in components:
        total_list.add(c["pdf"])

        norm_var_name = f"hggpdfsmrel_{c['proc_era']}_{cat}_{SQRTS}_normThisLumi"
        norm_var = wsig.function(norm_var_name)
        if norm_var:  
            if c["era"] not in lumiMap:
                raise RuntimeError("No lumiMap entry for era '%s' (component '%s') -- "
                                    "check ERA_TAGS / lumiMap are in sync" % (c["era"], c["pdf"].GetName()))
            wsig.var("IntLumi").setVal(lumiScaleFactor * lumiMap[c["era"]])
            val = norm_var.getVal()
            component_yields[c["pdf"].GetName()] = val
            # print("  [yield] era='%-8s' IntLumi=%.3f (=%.3f fb^-1) -> %-60s = %.6f" % (c["era"], lumiScaleFactor * lumiMap[c["era"]], lumiMap[c["era"]], c["pdf"].GetName(), val))

            h_comp = c["pdf"].createHistogram(f"h_comp_{c['pdf'].GetName()}", xvar, ROOT.RooFit.Binning(PDF_NBINS))
            if h_comp.Integral() > 0:
                h_comp.Scale(val / h_comp.Integral())
            
            component_hcomps[c["pdf"].GetName()] = h_comp

            if h_S is None:
                h_S = h_comp.Clone(f"h_S_{cat}")
            else:
                h_S.Add(h_comp)

    S_tot = sum(component_yields.values())
    # print("[sig_total_pdf] S_tot (summed individual component yields) = %.4f" % S_tot)
    # print("[sig_total_pdf] built combined histogram '%s' with integral=%.4f" % (h_S.GetName(), h_S.Integral()))

    effSigma = getEffSigma(h_S)
    print("[effSigma] = %.4f GeV" % effSigma)
    # range
    rangeName = "effSigma_%s" % cat
    xvar.setRange(rangeName, MASS - effSigma, MASS + effSigma) # signal
    xvar_bkg.setRange(rangeName, MASS - effSigma, MASS + effSigma) # background

    bin_low = h_S.FindBin(MASS - effSigma)
    bin_high = h_S.FindBin(MASS + effSigma)
    S_eff = h_S.Integral(bin_low, bin_high)
    sig_frac_in_window = S_eff / S_tot if S_tot > 0 else 0.0
    print("S_eff = %.4f, S_tot = %.4f, window_frac %.4f" % (S_eff, S_tot, sig_frac_in_window))

    # per production mode: summing component_yields
    print("[groups] grouping component yields by production mode:")
    window_group_yields = {}
    for group in set(c["group"] for c in components):
        members = [c for c in components if c["group"] == group]
        member_names = [c["pdf"].GetName() for c in members]
        group_s_eff = sum(component_hcomps[c["pdf"].GetName()].Integral(bin_low, bin_high) for c in members)
        window_group_yields[group] = group_s_eff
        print("['%s'] pdfs: %d, window yield = %.4f  (fraction of S_eff = %.4f)" % (group, len(members), group_s_eff, group_s_eff / S_eff if S_eff > 0 else 0.0))

    # background
    bkgshape_name = "CMS_hgg_%s_%s_bkgshape" % (cat, SQRTS)
    print("[background] looking up RooMultiPdf '%s'" % bkgshape_name)
    multipdf = wbkg.pdf(bkgshape_name)
    if multipdf is None:
        raise RuntimeError("Could not find RooMultiPdf '%s' in workspace" % bkgshape_name)
    bpdf = multipdf.getCurrentPdf()

    bnorm = wbkg.var("%s_norm" % bkgshape_name)
    B_tot = bnorm.getVal()
    # pdfindex_cat = wbkg.cat("pdfindex_%s_%s" % (cat, SQRTS))
    # print("[background] current envelope member = '%s', B_tot=%s" % (bpdf.GetName(), B_tot))

    h_B = bpdf.createHistogram(f"h_B_{cat}", xvar_bkg, ROOT.RooFit.Binning(PDF_NBINS))
    if h_B.Integral() > 0:
        h_B.Scale(B_tot / h_B.Integral()) # since h_B is created as a pdf (integral=1)
    b_bin_low = h_B.FindBin(MASS - effSigma)
    b_bin_high = h_B.FindBin(MASS + effSigma)
    B_eff = h_B.Integral(b_bin_low, b_bin_high)
    bkg_frac_in_window = B_eff / B_tot if B_tot > 0 else 0.0
    print("B_eff = %.4f, B_tot = %s, window_frac %.4f" % (B_eff, B_tot, bkg_frac_in_window))

    # S / (S+B)
    SoverSplusB = S_eff / (S_eff + B_eff) if (S_eff + B_eff) > 0 else 0.0
    print("[S/(S+B)] S_eff=%.4f, B_eff=%.4f -> S/(S+B) = %.4f" % (S_eff, B_eff, SoverSplusB))

    ratio_col_name = "S/(S+B)"
    row = {
        "cat": cat, 
        "sigma_eff": round(effSigma, 4),
    }
    for g in PROD_MODE_COLUMNS:
        group_yield = window_group_yields.get(g, 0.0)
        frac = group_yield / S_eff if S_eff > 0 else 0.0
        row["frac_%s" % g] = f"{frac * 100:.2f}%"

    for g in set(window_group_yields) - set(PROD_MODE_COLUMNS):
        group_yield = window_group_yields[g]
        frac = group_yield / S_eff if S_eff > 0 else 0.0
        row["frac_%s" % g] = f"{frac * 100:.2f}%"
    row["S_eff"] = round(S_eff, 4)
    row["B_eff"] = int(round(B_eff))
    row[ratio_col_name] = round(SoverSplusB, 4)
    rows.append(row)

# ---- print + save ----
header = ["cat", "sigma_eff"] + ["frac_%s" % g for g in PROD_MODE_COLUMNS] + ["S_eff", "B_eff", "S/(S+B)"]
extra_cols = sorted(set(k for r in rows for k in r) - set(header))
header += extra_cols

print()
print("=" * 130)
print("SUMMARY TABLE")
print("".join(f"{h:>15}" for h in header))
for r in rows:
    line = ""
    for h in header:
        val = r.get(h, 0.0)
        if isinstance(val, str):
            line += f"{val:>15}"
        elif isinstance(val, int):
            line += f"{val:15d}"
        else:
            line += f"{val:15.4f}"
    print(line)

outname = "SoverSplusB_C1reco.csv"
with open(outname, "w", newline="") as fout:
    writer = csv.DictWriter(fout, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)
print("\nSaved: %s" % outname)



# # STXS comparison:
# SQRTS = "13TeV"
# CAT_NAMES = [
#     "RECO_ttH_PTH_0_120",
#     "RECO_ttH_PTH_GT120"
# ]
# CATEGORIES = [
#     dict(
#         cat=cat,
#         sig_file=f"../comparison_stxs/Mar26/Models_IA/signal/CMS-HGG_sigfit_packaged_{cat}.root",
#         sig_ws="wsig_13TeV",
#         bkg_file=f"../comparison_stxs/Mar26/Models_IA/background/CMS-HGG_multipdf_{cat}.root",
#         bkg_ws="multipdf",
#     )
#     for cat in CAT_NAMES
# ]
# ERA_TAGS = ["preEE", "postEE", "preBPix", "postBPix"]
# PROD_MODES = [
#     ("ggZH", ("GG2HQQ", "GG2HLL", "GG2HNUNU")),
#     ("ggH",  ("GG2H", "GGH")),
#     ("bbH",  ("BBH",)),
#     ("VBF",  ("VBF",)),
#     ("tH",   ("THQ", "THW")),
#     ("ttH",  ("TTH",)),
#     ("ZH",   ("ZH2H",)),
#     ("WH",   ("WPLUSH", "WMINUSH", "WH2H")),
# ]
# PROD_MODE_COLUMNS = ["ggH", "VBF", "WH", "ZH", "ttH", "ggZH", "tH", "bbH"]
# def get_process_group(proc):
#     proc_upper = proc.upper()
#     for group, prefixes in PROD_MODES:
#         if proc_upper.startswith(prefixes):
#             return group
#     print("  !! WARNING: no mapping entry for raw process '%s' -- treating as its own group." % proc)
#     return proc

# group = get_process_group(proc)

# outname = "SoverSplusB_C1reco_STXScomparison.csv" 