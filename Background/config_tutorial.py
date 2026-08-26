# Config file: options for signal fitting

backgroundScriptCfg = {
  
  # Setup
  'inputWS':"/eos/user/p/pkrueper/STXS3_2025/src/run3hggstxs/classification/multiclassifier_extended_eval17marchon30may_176_finalfits/data/root/Data/ws/allData_data.root", # location of 'allData.root' file
  'cats':'auto', # auto: automatically inferred from input ws
  'catOffset':0, # add offset to category numbers (useful for categories from different allData.root files)  
  'ext':'STXS0', # extension to add to output directory
  'year':'combined', # Use combined when merging all years in category (for plots)

  # Job submission options
  'batch':'condor', # [condor,SGE,IC,local]
  'queue':'espresso' # for condor e.g. microcentury
  
}
