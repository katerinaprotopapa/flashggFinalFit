# Config file: options for signal fitting in kl analysis: C1reco - 2024

_year = '2024'

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
  'scalesCorr':'', # correlated across years
  'scalesGlobal':'', # affect all processes equally, correlated across years
  'smears':'Smearing2G_IJazZ', # separate nuisance per year

  # Job submission options
  'batch':'condor', # ['condor','SGE','IC','local']
  'queue':'espresso',
  # 'max_runtime': 3600,

}
