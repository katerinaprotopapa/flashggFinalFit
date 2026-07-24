# Config file: options for signal fitting in kl analysis: C1reco - preBPix

_year = 'preBPix'

signalScriptCfg = {
  
  # Setup
  'inputWSDir':'/vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/RooWorkspaces/C1_reco/signal/%s'%_year,
  'procs':'auto', # if auto: inferred automatically from filenames
  'cats':'auto', # if auto: inferred automatically from (0) workspace
  'ext':'kl_C1reco_%s'%_year,
  'analysis':'kl_C1reco', # To specify which replacement dataset mapping (defined in ./python/replacementMap.py)
  'year':'%s'%_year, # Use 'combined' if merging all years: not recommended
  'massPoints':'125',

  #Photon shape systematics  
  'scales':'', # separate nuisance per year
  'scalesCorr':'', # correlated across years
  'scalesGlobal':'', # affect all processes equally, correlated across years
  'smears':'', # separate nuisance per year

  # Job submission options
  'batch':'condor', # ['condor','SGE','IC','local']
  'queue':'espresso',
  'max_runtime': 3600,

}
