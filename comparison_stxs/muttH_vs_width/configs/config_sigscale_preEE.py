# Config file: signal fitting for the mu_ttH vs signal width study: C1reco - preEE
# Same as the aug26 (2022-2024) signal fits, plus CMS_hgg_sigma_scale (run signalFit with --modeOpts "... --addSigmaScale")

_year = 'preEE'

signalScriptCfg = {

  # Setup
  'inputWSDir':'/vols/cms/evp18/trilinear_higgs/run3hggstxs/src/run3hggstxs/final_fits_22_23_24_aug26/MC/nominal/%s'%_year,
  'procs':'auto', # if auto: inferred automatically from filenames
  'cats':'auto', # if auto: inferred automatically from (0) workspace
  'ext':'kl_C1reco_sigscale_%s'%_year,
  'analysis':'kl_C1reco', # To specify which replacement dataset mapping (defined in ./python/replacementMap.py)
  'year':'%s'%_year,
  'massPoints':'125',

  # Photon shape systematics (as in the aug26 fits)
  'scales':'ScaleEB2G_IJazZ,ScaleEE2G_IJazZ',
  'scalesCorr':'Material,FNUF',
  'scalesGlobal':'',
  'smears':'Smearing2G_IJazZ',

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
