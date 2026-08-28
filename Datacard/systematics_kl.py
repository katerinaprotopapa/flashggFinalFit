### --- kl analysis --- ###
# Systematics

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# THEORETICAL SYSTEMATICS 

theory_systematics = [
                # Normalisation uncertainties: enter interpretations
                {'name':'BR_hgg','title':'BR_hgg','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':"0.98/1.021"},

                {'name':'QCDscale_ggH','title':'QCDscale_ggH','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_ggh.json'},
                {'name':'QCDscale_VBF','title':'QCDscale_VBF','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_qqh.json'},
                {'name':'QCDscale_WH','title':'QCDscale_WH','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_wh.json'},
                {'name':'QCDscale_ZH','title':'QCDscale_ZH','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_zh.json'},
                {'name':'QCDscale_ttH','title':'QCDscale_ttH','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_tth.json'},

                {'name':'pdf_Higgs_ggH','title':'pdf_Higgs_ggH','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_ggh.json'},
                {'name':'pdf_Higgs_VBF','title':'pdf_Higgs_VBF','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_qqh.json'},
                {'name':'pdf_Higgs_WH','title':'pdf_Higgs_WH','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_wh.json'},
                {'name':'pdf_Higgs_ZH','title':'pdf_Higgs_ZH','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_zh.json'},
                {'name':'pdf_Higgs_ttH','title':'pdf_Higgs_ttH','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_tth.json'},

                {'name':'alphaS_ggH','title':'alphaS_ggH','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_ggh.json'},
                {'name':'alphaS_VBF','title':'alphaS_VBF','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_qqh.json'},
                {'name':'alphaS_WH','title':'alphaS_WH','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_wh.json'},
                {'name':'alphaS_ZH','title':'alphaS_ZH','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_zh.json'},
                {'name':'alphaS_ttH','title':'alphaS_ttH','type':'constant','prior':'lnN','correlateAcrossYears':1,'value':'theory_uncertainties/thu_tth.json'},

                {'name':'weight_AlphaS','title':'CMS_hgg_AlphaS','type':'factory','prior':'lnN','correlateAcrossYears':1,'tiers':['shape']},
                {'name':'weight_PS_ISR','title':'CMS_hgg_PS_ISR','type':'factory','prior':'lnN','correlateAcrossYears':1,'tiers':['shape']},
                {'name':'weight_PS_FSR','title':'CMS_hgg_PS_FSR','type':'factory','prior':'lnN','correlateAcrossYears':1,'tiers':['shape']},
              ]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# EXPERIMENTAL SYSTEMATICS 

experimental_systematics = [
                {'name':'lumi_1','title':'lumi_1','type':'constant','prior':'lnN','correlateAcrossYears':-1,'value':{'preEE':'1.0138', 'postEE':'1.0138', 'preBPix':'1.0017', 'postBPix':'1.0017', '2024':'1.0020'}},
                {'name':'lumi_2','title':'lumi_2','type':'constant','prior':'lnN','correlateAcrossYears':-1,'value':{'preEE':'-', 'postEE':'-', 'preBPix':'1.0127', 'postBPix':'1.0127', '2024':'1.0068'}},
                {'name':'lumi_3','title':'lumi_3','type':'constant','prior':'lnN','correlateAcrossYears':-1,'value':{'preEE':'-', 'postEE':'-', 'preBPix':'-', 'postBPix':'-', '2024':'1.0144'}},

                {'name':'weight_Pileup','title':'CMS_hgg_PileupWeight','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'weight_TriggerSF','title':'CMS_hgg_TriggerWeight','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'weight_PreselSF','title':'CMS_hgg_PreselSF','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'weight_ElectronVetoSF','title':'CMS_hgg_ElectronVetoSF','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'weight_ElectronIdLooseSF','title':'CMS_hgg_ElectronIdLooseSF','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'weight_ElectronIdRecoSF','title':'CMS_hgg_ElectronIdRecoSF','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'weight_NUM_TightPFIso_DEN_MediumID','title':'CMS_hgg_MuonIsoSF','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'weight_Tau_ID','title':'CMS_hgg_TauIDSF','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'weight_bTagSF_sys_cferr1','title':'CMS_hgg_bTagSF_cferr1','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'weight_bTagSF_sys_cferr2','title':'CMS_hgg_bTagSF_cferr2','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'weight_bTagSF_sys_hf','title':'CMS_hgg_bTagSF_hf','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'weight_bTagSF_sys_hfstats1','title':'CMS_hgg_bTagSF_hfstats1','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'weight_bTagSF_sys_hfstats2','title':'CMS_hgg_bTagSF_hfstats2','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'weight_bTagSF_sys_jes','title':'CMS_hgg_bTagSF_jes','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'weight_bTagSF_sys_lf','title':'CMS_hgg_bTagSF_lf','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'weight_bTagSF_sys_lfstats1','title':'CMS_hgg_bTagSF_lfstats1','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'weight_bTagSF_sys_lfstats2','title':'CMS_hgg_bTagSF_lfstats2','type':'factory','prior':'lnN','correlateAcrossYears':1},

                {'name':'MET_unclusteredEnergy','title':'CMS_hgg_MET_Unclustered','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'Tau_EnergyScale','title':'CMS_scale_t','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'energyErrShift','title':'CMS_hgg_SigmaEOverEShift','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'jec_syst_FlavorQCD','title':'CMS_scale_j_FlavorQCD','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'jec_syst_RelativeBal','title':'CMS_scale_j_RelativeBal','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'jec_syst_Total','title':'CMS_scale_j','type':'factory','prior':'lnN','correlateAcrossYears':1},
                # {'name':'jer_syst','title':'CMS_res_j','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'Electron_Scale2G_IJazZ','title':'CMS_hgg_Electron_Scale2G_IJazZ','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'PhotonIDMVAShape','title':'CMS_hgg_phoIdMva','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'MuonResolution','title':'CMS_res_m','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'MuonScale','title':'CMS_scale_m','type':'factory','prior':'lnN','correlateAcrossYears':1},
]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# SIGNAL SHAPE SYSTEMATICS

signal_shape_systematics = [
                {'name':'Material','title':'Material','type':'signal_shape','mode':'scalesCorr','mean':'0.0','sigma':'1.0','correlateAcrossYears':1},
                {'name':'FNUF','title':'FNUF','type':'signal_shape','mode':'scalesCorr','mean':'0.0','sigma':'1.0','correlateAcrossYears':1},
                {'name':'ScaleEB2G_IJazZ','title':'ScaleEB2G_IJazZ','type':'signal_shape','mode':'scales','mean':'0.0','sigma':'1.0','correlateAcrossYears':0},
                {'name':'ScaleEE2G_IJazZ','title':'ScaleEE2G_IJazZ','type':'signal_shape','mode':'scales','mean':'0.0','sigma':'1.0','correlateAcrossYears':0},
                {'name':'Smearing2G_IJazZ','title':'Smearing2G_IJazZ','type':'signal_shape','mode':'smears','mean':'0.0','sigma':'1.0','correlateAcrossYears':0}, 
]