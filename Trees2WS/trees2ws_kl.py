import os, sys, re
from optparse import OptionParser
from collections import OrderedDict as od
from importlib import import_module
import json
import ROOT
import pandas as pd
import numpy as np

from commonTools import *
from commonObjects import *
from tools.STXS_tools import *

import pyarrow.parquet as pq
import glob
import random

def get_options():
    parser = OptionParser()
    parser.add_option('--inputConfig', dest='inputConfig', default="", help='Input config file')
    parser.add_option('--inputTreeFile',dest='inputTreeFile', default="/vols/cms/evp18/trilinear_higgs/run3hggstxs/src/run3hggstxs/final_fits/MC/preEE/ggH/nominal", help='Input tree file')
    parser.add_option('--inputMass', dest='inputMass', default="125", help='Higgs mass')
    parser.add_option('--productionMode', dest='productionMode', default="ggH", help='Production mode')
    parser.add_option('--decayExt', dest='decayExt', default='', help='Decay extension')
    parser.add_option('--year', dest='year', default="2022", help='Year')
    parser.add_option('--doNNLOPS', dest='doNNLOPS', default=False, action="store_true", help='Add NNLOPS weight')
    parser.add_option('--doSystematics', dest='doSystematics', default=False, action="store_true", help='Add systematics')
    parser.add_option('--catVar', dest='catVar', default="pred_C1_reco", help='Column name for categorization')
    parser.add_option('--categorisationConfig',default='config_categories_kl.json')
    parser.add_option('-v',default=False,action="store_true")
    return parser.parse_args()

def leave():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~ SCRIPT END ~~~~~~~~~~~~~~~~~~~~~~~~~")
    exit(0)

# Parser Arguments
(opt, args) = get_options()
proc=opt.inputTreeFile.split('/')[-2]
print("proc: ", proc)

# Input Config (e.g. config_tutorial_kl.py)
if opt.inputConfig == '' or not os.path.exists(opt.inputConfig):
    print(f"[ERROR] Config file {opt.inputConfig} not found.")
    leave()
_cfg = import_module(re.sub(".py$", "", opt.inputConfig)).trees2wsCfg
inputTreeDir     = _cfg['inputTreeDir'].rstrip('/')
mainVars         = _cfg['mainVars']
stxsVar          = _cfg['stxsVar']
systematicsVars  = _cfg['systematicsVars']
theoryWeightContainers = _cfg['theoryWeightContainers']
systematics      = _cfg['systematics']
cats             = _cfg['cats']
# If STXS var is not defined, disable splitting
if not stxsVar:
    opt.doSTXSSplitting = False
    stxsVar = 'nosplit'
    print("[INFO] STXS variable not defined. Disabling STXS splitting.")

# Read in parquet files (should only really be 1)
def parquet_readin(dirpath):
    # take only nominal, non-systematic files
    files = [
        f for f in glob.glob(f"{dirpath}/*.parquet")
        if "Up" not in f and "Down" not in f and "ws_" not in f
    ]
    if not files: # if no files are found, the function returns an empty DataFrame
        return pd.DataFrame()
    if len(files) != 1:
        print(f"[INFO] There is not only one parquet file for MC {opt.year} {opt.productionMode} nominal! Check again if this as you expect!")

    dfs = []
    for f in files:
        pf = pq.ParquetFile(f)
        for batch in pf.iter_batches(batch_size=20000): # iter_batches lets you stop early
            df = batch.to_pandas()
            dfs.append(df)

    return pd.concat(dfs)

merged = parquet_readin(opt.inputTreeFile)
print('Nominal merged: ', merged)

# Auto-detect categories from .parquet files in inputTreeFile directory
if cats == 'auto':
    if not os.path.isdir(opt.inputTreeFile):
        print(f"[ERROR] Input directory '{opt.inputTreeFile}' does not exist.")
        leave()
    with open(opt.categorisationConfig, "r") as f:
        cat_dict = json.load(f)
    cats = [cat_dict['cat_dict'][str(cat)] for cat in merged[opt.catVar].unique() if cat!=0]
    if not cats:
        print(f"[ERROR] No categories are detected in '{opt.inputTreeFile}' parquet file")
        leave()
    else:
        print(f"[INFO] Detected categories: {cats}")
cats=list(cat_dict['cat_dict'].values()) # All categories are included

merged['cat'] = merged[opt.catVar].map(str).map(cat_dict['cat_dict'])
merged['type'] = 'nominal'

data = merged.copy()

# Ensure STXS var
if stxsVar not in data.columns:
    data[stxsVar] = 'nosplit'

# Systematic - add HEM for 2018
if opt.year == '2018':
    systematics.append("JetHEM")
# Theory Weights
modesToSkipTheoryWeights = ['bbh', 'thq', 'thw']
theoryWeightColumns = {
    ts: [f"{ts[:-1]}_{i}" for i in range(n)] for ts, n in theoryWeightContainers.items()
}

# ----- RooWorkspace Helpers -----
def add_vars_to_workspace(ws, df, stxsVar):
    intLumi = ROOT.RooRealVar("intLumi", "intLumi", 1000., 0., 999999999.) # initializing intLumi to 1000 CHECK AGAIN
    intLumi.setConstant(True)
    getattr(ws, 'import')(intLumi)

    rvars = od()
    for col in df.columns:
        if col in ['cat', 'type', stxsVar, '']: continue
        if col == "CMS_hgg_mass":
            rvar = ROOT.RooRealVar(col, col, 125., 100., 180.)
            rvar.setBins(160)
        elif col == "dZ":
            rvar = ROOT.RooRealVar(col, col, 0., -20., 20.)
            rvar.setBins(40)
        elif col == "weight":
            rvar = ROOT.RooRealVar(col, col, 0.)
        else:
            rvar = ROOT.RooRealVar(col, col, 1., -999999, 999999)
            rvar.setBins(1)
        getattr(ws, 'import')(rvar, ROOT.RooFit.Silence())
        rvars[col] = rvar
    return list(rvars.keys())

def make_argset(ws, var_names):
    aset = ROOT.RooArgSet()
    for name in var_names:
        aset.add(ws.var(name))
    return aset

# ----- RooWorkspace Creation -----
for stxsId in data[stxsVar].unique():
    df = data[data[stxsVar] == stxsId]
    if stxsVar == 'nosplit':
        stxsBin = opt.productionMode
        print("stxsBin: ", stxsBin)
    else:
        stxsBin = flashggSTXSDict.get(int(stxsId), f"unknownSTXS_{stxsId}")
        if opt.productionMode == "wh":
            stxsBin = stxsBin.replace("QQ2HQQ", "WH2HQQ")
        elif opt.productionMode == "zh":
            stxsBin = stxsBin.replace("QQ2HQQ", "ZH2HQQ")
        elif opt.productionMode == "ggzh":
            if opt.decayExt == "_ZToQQ":
                stxsBin = stxsBin.replace("GG2H", "GG2HQQ")
            elif opt.decayExt == "_ZToNuNu":
                stxsBin = stxsBin.replace("GG2HLL", "GG2HNUNU")
        elif opt.productionMode == "thq":
            stxsBin = stxsBin.replace("TH", "THQ")
        elif opt.productionMode == "thw":
            stxsBin = stxsBin.replace("TH", "THW")

    output_dir = f"{opt.inputTreeFile}/ws_{stxsBin}"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"output_{stxsBin}_M{opt.inputMass}_pythia8_{stxsBin}.root")
    print(f"[INFO] Creating workspace: {output_file}")

    fout = ROOT.TFile(output_file, "RECREATE")

    foutdir = fout.mkdir(inputTreeDir)
    foutdir.cd()  # IMPORTANT: switch to the input directory

    ws = ROOT.RooWorkspace("cms_hgg_13TeV", "cms_hgg_13TeV")

    if 'mass' in df.columns:
        df = df.rename(columns={'mass': 'CMS_hgg_mass'})
    df_reduced = df[mainVars]
    var_names = add_vars_to_workspace(ws, df_reduced, stxsVar)

    for cat in cats:
        df_cat = df[df['cat'] == cat]

        aset = make_argset(ws, var_names)  # full list (workspace needs everything)
        cat_renamed=cat#'_'.join(cat.split('_')[:-1])
        dset_name = f"{opt.productionMode}_{opt.year}_hgg_{opt.inputMass}_13TeV_{cat_renamed}"
        dset = ROOT.RooDataSet(dset_name, dset_name, aset, ROOT.RooFit.WeightVar("weight"))

        # # Only try to convert numeric columns
        # numeric_var_names = [v for v in var_names if v in df_cat.columns and pd.api.types.is_numeric_dtype(df_cat[v])]
        # df_cat.loc[:, numeric_var_names] = df_cat[numeric_var_names].astype('float64')
        # df_cat = df_cat.dropna(subset=numeric_var_names)
        # df_cat = df_cat.dropna(subset=var_names)
        if opt.v:
            print(f"[INFO] Category {cat} has {len(df_cat)} entries after cleaning.")
        # for row in df_cat[numeric_var_names].itertuples(index=False, name=None):
        #     for name, val in zip(numeric_var_names, row):
        #         var = aset.find(name)
        #         if var:  # safeguard
        #             var.setVal(float(val))
        #     dset.add(aset, aset.find("weight").getVal())

        for row in df_cat.itertuples(index=False):
            for name in var_names:
                val = getattr(row, name)
                var = aset.find(name)
                if var:
                    var.setVal(val)
            dset.add(aset, aset.find("weight").getVal())
        getattr(ws, 'import')(dset)
    
    if opt.doSystematics:
        def parquet_readin_syst(dirpath, syst, direction):
            # Example matches: ...PileupUp.parquet, ...JERDown.parquet
            files = [
                f for f in glob.glob(f"{dirpath}/*.parquet")
                if syst in f and direction in f and "ws_" not in f
            ]
            if not files:
                return pd.DataFrame()
            
            df_syst = []
            for f in files:
                try:
                    table = pq.read_table(f)
                    df_syst.append(table.to_pandas())
                except Exception as e:
                    print(f"[ERROR] Could not read {f}: {e}")
                    return pd.DataFrame()

        for cat in cats:
            catcopy=cat
            for syst in systematics:
                for direction in ['Down',"Up"]:
                    syst_name = f"{syst}{direction}"
                
                    merged_sys = parquet_readin_syst(opt.inputTreeFile, syst, direction)
                    merged_sys['cat'] = merged_sys[opt.catVar].map(str).map(cat_dict['cat_dict'])
                    merged_sys = merged_sys[merged_sys['cat'] == cat]
                    sdf = merged_sys

                    if sdf.empty:
                       if opt.v:
                        print(f"[WARNING] Empty systematic parquet:")
                        # continue                      
                    if 'mass' in sdf.columns:
                        sdf = sdf.rename(columns={'mass': 'CMS_hgg_mass'})

                    # If splitting: ensure STXS var
                    if stxsVar not in sdf.columns:
                        sdf[stxsVar] = stxsId

                    # Clean and ensure needed vars
                    systematicsVarsDropWeight = [v for v in systematicsVars if v != 'weight']
                    for v in systematicsVarsDropWeight:
                        if v not in sdf.columns:
                            print(f"[ERROR] Missing var {v} in syst file")
                            break
                    sdf = sdf.dropna(subset=systematicsVarsDropWeight + ['weight'])

                    aset = make_argset(ws, systematicsVarsDropWeight)
                    hist_name = f"{opt.productionMode}_{opt.year}_hgg_{opt.inputMass}_13TeV_{catcopy}_{syst_name}01sigma"
                    # print(f"[DEBUG] Importing histogram: {hist_name}")
                    hist = ROOT.RooDataHist(hist_name, hist_name, aset)

                    for row, weight in zip(sdf[systematicsVarsDropWeight].to_numpy(), sdf["weight"].to_numpy()):
                        for i, val in enumerate(row):
                            aset[i].setVal(float(val))
                        hist.add(aset, weight)

                    getattr(ws, 'import')(hist)
                    if opt.v:
                        print(f"[INFO] Imported systematics hist: {hist_name}")
    if opt.v:
        print(ws)
        ws.Print('v')
    ws.Write()
    fout.Close()

print("~~~~~~~~~~~~~~~~~~~~~~~~~ ALL WORKSPACES DONE ~~~~~~~~~~~~~~~~~~~~~~~~~")
print(' WARNING: In this setup, parquet files had background (pred=0). This got dropped when making RooWS!')

debug= False
if debug:
    for i in merged.cat.unique():
        proc=opt.inputTreeFile.split('/')[-3]
        n=f'{proc}_preEE_hgg_125_13TeV_{i}'
        print(f'{i} and {merged[merged.cat==i].weight.sum()} vs root: {ws.data(n).Print()}')
        print('\n')