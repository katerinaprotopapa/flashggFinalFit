# Config file: options for signal fitting in kl analysis: C1reco - preEE

_year = 'preEE'

signalScriptCfg = {
  
  # Setup
  'inputWSDir':'/vols/cms/evp18/trilinear_higgs/run3hggstxs/src/run3hggstxs/final_fits/MC/nominal/%s'%_year,
  'procs':'auto', # if auto: inferred automatically from filenames
  'cats':'auto', # if auto: inferred automatically from (0) workspace
  'ext':'kl_C1reco_%s'%_year,
  'analysis':'kl_C1reco', # To specify which replacement dataset mapping (defined in ./python/replacementMap.py)
  'year':'%s'%_year, # Use 'combined' if merging all years: not recommended
  'massPoints':'125',

  #Photon shape systematics
  'scales':'ScaleEB2G_IJazZ,ScaleEE2G_IJazZ', # separate nuisance per year
  'scalesCorr':'Material,FNUF', # correlated across years
  'scalesGlobal':'', # affect all processes equally, correlated across years
  'smears':'Smearing2G_IJazZ', # separate nuisance per year

  # Maps pred_C1_reco int (as string) to category name, matching Parquet2WS/config_kl.json
  'categories': {
    "0": "background",
    "1": "hadr_C1_LT_10",
    "2": "hadr_C1_10_21",
    "3": "hadr_C1_21_30",
    "4": "hadr_C1_30_36",
    "5": "hadr_C1_36_42",
    "6": "hadr_C1_42_63",
    "7": "hadr_C1_GT_63",
    "8": "lept_C1_LT_15",
    "9": "lept_C1_15_30",
    "10": "lept_C1_30_43",
    "11": "lept_C1_43_63",
    "12": "lept_C1_63_70",
    "13": "lept_C1_GT_70"
  },

  # Job submission options
  'batch':'condor', # ['condor','SGE','IC','local']
  'queue':'espresso',
  'max_runtime': 3600,

}
