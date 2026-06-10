"""
NOTE!!! Ignore "plot_weight" of ZH samples for now (it was calculated using the XS of NLO ggZH samples instead of the highest order theoretical calculation XS value)
"""

import ROOT
import os
import pickle
import pandas as pd

# Base directory of the Workspaces (for all eras)
root_dir = "/vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/RooWorkspaces/C1_reco/signal"
#!/usr/bin/env python3

eras_lumi = {
    "preEE": 7.99,
    "postEE": 26.68,
    "preBPix": 17.96,
    "postBPix": 9.68,
    "2024": 109.95
}
xs_procs = { # XS values for mH=125.38GeV: https://gitlab.cern.ch/jlangfor/stxs-run3-recommendations/-/blob/master/data/SM_Higgs_XS_13p6TeV.xlsx?ref_type=heads
    "ggH": 51.96,
    "VBF": 4.067,
    "WH": 1.442,
    "ZH": 0.944, # 0.936, # since adding ggZH in
    "ttH": 0.564,
}
br = 0.002277
categories = {
    1: "hadr_C1_LT_20",
    2: "hadr_C1_20_40",
    3: "hadr_C1_40_60",
    4: "hadr_C1_60_80",
    5: "hadr_C1_GT_80",
    6: "lept_C1_LT_15",
    7: "lept_C1_15_30",
    8: "lept_C1_30_45",
    9: "lept_C1_45_60",
    10: "lept_C1_60_75",
    11: "lept_C1_GT_75"
}
total_yields = {era: {proc: {cat: 0.0 for cat in categories.values()} for proc in xs_procs} for era in eras_lumi.keys()}

### 1) ###
# --- Printing: "plot_weight" is as expected check in Parquet files ---
# # Preprocessing - full MC df
# path_df_preprocess = "/vols/cms/evp18/trilinear_higgs/run3hggstxs/src/run3hggstxs/preprocessing/saves/df_preprocess_22_23_24_MC.pkl"
# with open(path_df_preprocess, "rb") as f:
#         df_preprocess = pickle.load(f)
# # print("df_preprocess: ", df_preprocess)

# Parquet files
syst = "nominal"
pred_label = "pred_C1_reco"
total_yields_exp = {era: {proc: {cat: 0.0 for cat in categories.values()} for proc in xs_procs} for era in eras_lumi.keys()}
parquet_dir = "/vols/cms/evp18/trilinear_higgs/run3hggstxs/src/run3hggstxs/final_fits/MC/"
for era, lumi in eras_lumi.items():
    for proc, xs in xs_procs.items():
        parquet_path = os.path.join(parquet_dir, era, proc, syst, f"{proc}_{era}_{syst}.parquet")
        if not os.path.exists(parquet_path):
            print(f"Parquet file not found: {parquet_path}")
            continue
        df = pd.read_parquet(parquet_path)
        df["plot_weight_check"] = xs*1000 * br * lumi * df["weight"]
        print(df[["era", "sample_name", "weight", "plot_weight", "plot_weight_check"]])

### 2) ###
# --- RooWorkSpaces ---
for era, lumi in eras_lumi.items():
    for proc, xs in xs_procs.items():
        file_path = os.path.join(root_dir, era, f"output_{proc}_M125_pythia8_{proc}.root")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        f = ROOT.TFile.Open(file_path)
        if not f or f.IsZombie():
            print(f"Failed to open {file_path}")
            continue
        dir = f.Get("DiphotonTree") # get the TDirectory
        if not dir:
            print(f"No DiphotonTree in {file_path}")
            continue
        ws = dir.Get("cms_hgg_13TeV") # get the RooWorkspace
        if not ws:
            print(f"No RooWorkspace cms_hgg_13TeV in {file_path}")
            continue
        
        for i, cat in categories.items():
            cat_dataset = ws.data(f"{proc}_{era}_hgg_125_13TeV_{cat}")
            sum_w = cat_dataset.sumEntries()
            # finding the Number of Events for each era x proc x cat
            # print(f"Era {era} - proc {proc} - cat {cat}")
            # print("xs: ", xs)
            # print("br: ", br)
            # print("lumi: ", lumi)
            # print("sum_w: ", sum_w)

            # ToDo: I will have to add the new XS for WH and ZH here
            total_yields[era][proc][cat] = xs*1000 * br * lumi * sum_w # since xs is in pb and lumi in fb^-1 
            # total_yields[era][proc][cat] = sum_w # just weights
# print(total_yields)

# --- Parquet files from Preprocessing ---
syst = "nominal"
pred_label = "pred_C1_reco"
total_yields_exp = {era: {proc: {cat: 0.0 for cat in categories.values()} for proc in xs_procs} for era in eras_lumi.keys()}
parquet_dir = "/vols/cms/evp18/trilinear_higgs/run3hggstxs/src/run3hggstxs/final_fits/MC/"
for era, lumi in eras_lumi.items():
    for proc, xs in xs_procs.items():
        parquet_path = os.path.join(parquet_dir, era, proc, syst, f"{proc}_{era}_{syst}.parquet")
        if not os.path.exists(parquet_path):
            print(f"Parquet file not found: {parquet_path}")
            continue

        df = pd.read_parquet(parquet_path, columns=[pred_label, "weight", "plot_weight"])
        yields = df.groupby(pred_label)["plot_weight"].sum() # NOTE: comparing with plot_weight
        # yields = df.groupby(pred_label)["weight"].sum() # just weights

        for i, cat in categories.items():
            total_yields_exp[era][proc][cat] = yields.get(i, 0.0)
# print(total_yields_exp)

# --- Printing: RooWorkSpaces VS Parquet files ---
# This is actually calculated yields VS plot_weight column in Parquet files (exp)
# I have verified that weights from parquet transfer fine in trees2ws
for era in eras_lumi.keys():
    print(f"\n{'='*150}")
    print(f"Era: {era}")
    print(f"{'='*150}")
    
    # header
    header = f"{'Category':<20} |"
    for proc in xs_procs.keys():
        header += f" {proc:^22} |"
    print(header)
    
    # sub-header
    sub_header = f"{'':<20} |"
    for _ in xs_procs:
        sub_header += f" {'RooWs':>4} {'Parquet':>8} {'Ratio':>7} |"
    print(sub_header)
    print("-" * 150)

    # cats
    unique_cats = list(dict.fromkeys(categories.values()))
    for cat in unique_cats:
        row = f"{cat:<22} |"
        for proc in xs_procs.keys():
            val_ws = total_yields[era][proc][cat] 
            val_exp = total_yields_exp[era][proc][cat]
            ratio = val_ws / val_exp if val_exp > 0 else 0.0
            row += f" {val_ws:7.5f} {val_exp:7.5f} {ratio:6.3f} |"
        print(row)
print(f"\n{'='*150}")
