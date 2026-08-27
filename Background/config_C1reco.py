# Config file: options for signal fitting

backgroundScriptCfg = {
  
  # Setup
  'inputWS':'/vols/cms/evp18/trilinear_higgs/run3hggstxs/src/run3hggstxs/final_fits/Data/merged/C1_reco/ws_data/allData_data.root', # location of 'allData.root' file
  'cats':'auto', # auto: automatically inferred from input ws
  'catOffset':0, # add offset to category numbers (useful for categories from different allData.root files)  
  'ext':'kl_C1reco', # extension to add to output directory
  'year':'combined', # Use combined when merging all years in category (for plots)

  # Job submission options
  'batch':'condor', # [condor,SGE,IC,local]
  'queue':'espresso', # for condor e.g. microcentury
  'max_runtime': 3600
  
}
