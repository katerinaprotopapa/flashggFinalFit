import ROOT
import os
import pickle
import pandas as pd

# Base directory of the Workspaces (for all eras)
root_dir = "/vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/RooWorkspaces_6Feb2026/signal"
#!/usr/bin/env python3

eras_lumi = {
    "preEE": 8.00,
    "postEE": 26.70,
}
xs_procs = { # XS values for mH=125.38GeV: https://gitlab.cern.ch/jlangfor/stxs-run3-recommendations/-/blob/master/data/SM_Higgs_XS_13p6TeV.xlsx?ref_type=heads
    "ggH": 51.96,
    "VBF": 4.067,
    "WH": 1.442,
    "ZH": 0.944, # 0.936, # since adding ggZH in
    "ttH": 0.564,
}
# xs_procs = { # 'plot_weight' was calculated for xs values at mH=125GeV instead of 125.38GeV
#     "ggH": 52.23,
#     "VBF": 4.078,
#     "WH": 1.442,
#     "ZH": 0.944, # adding ggZH in
#     "ttH": 0.57,
# }
# print("WH: ", 0.38268657 + 0.18495666 + 0.5992074900000001 + 0.28960362)
# print("ZH: ", 0.0953093586 + 0.1887 + 0.6598804899999999 + 0.006838 + 0.01351 + 0.04776)
# print("WH: ", 0.59328485+0.37886577+0.2867411412+0.1831100256)
# print("ZH: ", 0.560266754+0.087945636+0.16028+0.094170117+0.014781978+0.02694)
# exit()
br = 0.002277
categories = {
    1: "hadr_C1_LT_10", 
    2: "hadr_C1_10_29", 
    3: "hadr_C1_29_48", 
    4: "hadr_C1_48_71", 
    5: "hadr_C1_GT_71",
    6: "lept_C1_LT_10", 
    7: "lept_C1_10_29", 
    8: "lept_C1_29_48", 
    9: "lept_C1_48_71", 
    10: "lept_C1_GT_71"
}
total_yields = {era: {proc: {cat: 0.0 for cat in categories.values()} for proc in xs_procs} for era in eras_lumi.keys()}

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
        yields = df.groupby(pred_label)["plot_weight"].sum()
        # yields = df.groupby(pred_label)["weight"].sum() # just weights

        for i, cat in categories.items():
            total_yields_exp[era][proc][cat] = yields.get(i, 0.0)
# print(total_yields_exp)

# --- Printing: RooWorkSpaces VS Parquet files ---
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


# --- Printing: "plot_weight" is as expected check in Parquet files ---
# Preprocessing - full MC df
path_df_preprocess = "/vols/cms/evp18/trilinear_higgs/run3hggstxs/src/run3hggstxs/preprocessing/saves/channels/ttH_classifier_df_preprocess_2022_channels.pkl"
with open(path_df_preprocess, "rb") as f:
        df_preprocess = pickle.load(f)
# print("df_preprocess: ", df_preprocess)

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
