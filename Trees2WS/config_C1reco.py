# Input config file for running trees2ws

trees2wsCfg = {

  # Name of RooDirectory storing input tree
  'inputTreeDir':'DiphotonTree',

  # Variables to be added to dataframe: use wildcard * for common strings
  'mainVars':["CMS_hgg_mass","weight","dZ","C1_gen",
              "weight_AlphaSDown", "weight_AlphaSUp", "weight_ElectronIdLooseSFDown", "weight_ElectronIdLooseSFUp", "weight_ElectronIdRecoSFDown", "weight_ElectronIdRecoSFUp", "weight_ElectronVetoSFDown", "weight_ElectronVetoSFUp", "weight_NUM_TightPFIso_DEN_MediumIDDown", "weight_NUM_TightPFIso_DEN_MediumIDUp", "weight_PS_FSRDown", "weight_PS_FSRUp", "weight_PS_ISRDown", "weight_PS_ISRUp", "weight_PileupDown", "weight_PileupUp", "weight_PreselSFDown", "weight_PreselSFUp", "weight_Tau_IDDown", "weight_Tau_IDUp", "weight_TriggerSFDown", "weight_TriggerSFUp"
            ], # Var for the nominal RooDataSets
  'dataVars':["CMS_hgg_mass","weight"], # Vars to be added for data
  'stxsVar':'',
  'systematicsVars':["CMS_hgg_mass","weight"], # Variables to add to sytematic RooDataHists
  'theoryWeightContainers':{},

  # List of systematics: use string YEAR for year-dependent systematics
  'systematics':[],

  # Analysis categories: python list of cats or use 'auto' to extract from input tree
  'cats':'auto',

  'catVar': 'pred_C1_reco',
  'binning': 'C1_reco'

}
