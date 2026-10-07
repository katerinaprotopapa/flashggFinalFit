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

                # weights in nominal parquet (a_w)
                {'name':'weight_AlphaS','title':'pdf_alphas','type':'factory','prior':'lnN','correlateAcrossYears':1,'tiers':['shape']}, # shape (holding total signal yield fixed and only lets events migrate between cats) - I think the reason for not floating norm here is because that is accounted in the alphaS above and so we would be double counting? see https://gitlab.cern.ch/ekprotop/higgs-dna-fork/-/blob/evp18/HiggsDNA_C1/higgs_dna/systematics/event_weight_systematics.py?ref_type=heads
                {'name':'weight_PS_ISR','title':'ps_isr','type':'factory','prior':'lnN','correlateAcrossYears':1,'tiers':['default']}, # ishape (similar migration as shape but overall yield of the process also allowed to float): same as above
                {'name':'weight_PS_FSR','title':'ps_fsr','type':'factory','prior':'lnN','correlateAcrossYears':1,'tiers':['default']}, # ishape: same as above
              ]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# EXPERIMENTAL SYSTEMATICS 

experimental_systematics = [
                {'name':'lumi_1','title':'lumi_1','type':'constant','prior':'lnN','correlateAcrossYears':-1,'value':{'preEE':'1.0138', 'postEE':'1.0138', 'preBPix':'1.0017', 'postBPix':'1.0017', '2024':'1.0020', '2025':'1.0020'}}, # FIXME: 2025 copied from 2024 for now. found in https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun3
                {'name':'lumi_2','title':'lumi_2','type':'constant','prior':'lnN','correlateAcrossYears':-1,'value':{'preEE':'-', 'postEE':'-', 'preBPix':'1.0127', 'postBPix':'1.0127', '2024':'1.0068', '2025':'1.0068'}},
                {'name':'lumi_3','title':'lumi_3','type':'constant','prior':'lnN','correlateAcrossYears':-1,'value':{'preEE':'-', 'postEE':'-', 'preBPix':'-', 'postBPix':'-', '2024':'1.0144', '2025':'1.0144'}},

                # weight
                {'name':'weight_Pileup','title':'CMS_pileup_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':1},# https://gitlab.cern.ch/cms-analysis/general/systematics/-/blob/master/systematics_master.yml?ref_type=heads
                {'name':'weight_TriggerSF','title':'CMS_eff_g_trigger','type':'factory','prior':'lnN','correlateAcrossYears':0}, # https://cms-alcm.web.cern.ch/notes/CMS-AN-2025-004/AN2025_004_v4_20260611_081027.pdf
                {'name':'weight_PreselSF','title':'CMS_eff_g_PreselSF_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':1}, # https://cms-alcm.web.cern.ch/notes/CMS-AN-2025-004/AN2025_004_v4_20260611_081027.pdf
                {'name':'weight_ElectronVetoSF','title':'CMS_eff_g_CSEV_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':1}, # https://gitlab.cern.ch/cms-analysis/general/systematics/-/blob/master/systematics_master.yml?ref_type=heads
                {'name':'weight_ElectronIdLooseSF','title':'CMS_eff_e_id_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':1}, # https://gitlab.cern.ch/cms-analysis/general/systematics/-/blob/master/systematics_master.yml?ref_type=heads
                {'name':'weight_ElectronIdRecoSF','title':'CMS_eff_e_reco_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':1}, # https://gitlab.cern.ch/cms-analysis/general/systematics/-/blob/master/systematics_master.yml?ref_type=heads
                {'name':'weight_NUM_TightPFIso_DEN_MediumID','title':'CMS_eff_m_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':1}, # correlated since: https://muon-wiki.docs.cern.ch/guidelines/corrections/ this is discouraged in https://gitlab.cern.ch/cms-analysis/general/systematics/-/blob/master/systematics_master.yml?ref_type=heads
                {'name':'weight_Tau_ID','title':'CMS_eff_t_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':0}, # btw not using the tau pog rec (since it is too overkill for us): https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendationForRun3
                {'name':'weight_bTagSF_sys_cferr1','title':'CMS_btag_fullShape_cferr1','type':'factory','prior':'lnN','correlateAcrossYears':1}, # all in this section from https://gitlab.cern.ch/cms-analysis/general/systematics/-/blob/master/systematics_master.yml?ref_type=heads
                {'name':'weight_bTagSF_sys_cferr2','title':'CMS_btag_fullShape_cferr2','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'weight_bTagSF_sys_hf','title':'CMS_btag_fullShape_hf','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'weight_bTagSF_sys_hfstats1','title':'CMS_btag_fullShape_hfstats1','type':'factory','prior':'lnN','correlateAcrossYears':0},
                {'name':'weight_bTagSF_sys_hfstats2','title':'CMS_btag_fullShape_hfstats2','type':'factory','prior':'lnN','correlateAcrossYears':0},
                {'name':'weight_bTagSF_sys_jes','title':'CMS_btag_jes','type':'factory','prior':'lnN','correlateAcrossYears':1}, # FIXME: I think this is discouraged based on: https://gitlab.cern.ch/cms-analysis/general/systematics/-/blob/master/systematics_master.yml?ref_type=heads
                {'name':'weight_bTagSF_sys_lf','title':'CMS_btag_fullShape_lf','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'weight_bTagSF_sys_lfstats1','title':'CMS_btag_fullShape_lfstats1','type':'factory','prior':'lnN','correlateAcrossYears':0},
                {'name':'weight_bTagSF_sys_lfstats2','title':'CMS_btag_fullShape_lfstats2','type':'factory','prior':'lnN','correlateAcrossYears':0},

                # shape: separate up/down parquets in final_fits/MC/<name>/{up,down}/<era>/ (a_h) - name must match the directory
                {'name':'Electron_Scale_EGM','title':'CMS_scale_e_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'Electron_Smearing_EGM','title':'CMS_res_e_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'energyErrShift','title':'CMS_HIG25020_energyErrShift','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'jec_syst_Total','title':'CMS_scale_j','type':'factory','prior':'lnN','correlateAcrossYears':0}, # split JEC sources only exist for ttH in 2022/23, so use Total (as in STXS)
                {'name':'jer_syst','title':'CMS_res_j_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':1}, # https://gitlab.cern.ch/cms-analysis/general/systematics/-/blob/master/systematics_master.yml?ref_type=heads
                {'name':'MET_unclusteredEnergy','title':'CMS_scale_met_unclustered_energy','type':'factory','prior':'lnN','correlateAcrossYears':0}, # https://gitlab.cern.ch/cms-analysis/general/systematics/-/blob/master/systematics_master.yml?ref_type=heads
                {'name':'MuonScale','title':'CMS_scale_m_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'MuonResolution','title':'CMS_res_m_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':1},
                {'name':'PhotonIDMVAShape','title':'CMS_HIG25020_shape_g_id','type':'factory','prior':'lnN','correlateAcrossYears':0}, # https://indico.cern.ch/event/1624987/contributions/6980057/attachments/3234779/5767796/PhotonID_2026_03_09-1.pdf - it hasn't been decided yet how to handle the correlation (22/23 derived together)
                {'name':'Tau_EnergyScale','title':'CMS_scale_t_13p6TeV','type':'factory','prior':'lnN','correlateAcrossYears':1}, # btw not using the tau pog rec (since it is too overkill for us) https://gitlab.cern.ch/cms-analysis/general/systematics/-/blob/master/systematics_master.yml?ref_type=heads
                {'name':'MET_XY_stat_x','title':'CMS_scale_met_xy_stat_x','type':'factory','prior':'lnN','correlateAcrossYears':0}, # not in STXS list; stat -> uncorrelated
                {'name':'MET_XY_stat_y','title':'CMS_scale_met_xy_stat_y','type':'factory','prior':'lnN','correlateAcrossYears':0}, # not in STXS list; stat -> uncorrelated
]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# SIGNAL SHAPE SYSTEMATICS

signal_shape_systematics = [
                # {'name':'Material','title':'CMS_HIG25020_scale_g_material_13p6TeV','type':'signal_shape','mode':'scalesCorr','mean':'0.0','sigma':'1.0'},
                # {'name':'FNUF','title':'CMS_HIG25020_scale_g_fnuf_13p6TeV','type':'signal_shape','mode':'scalesCorr','mean':'0.0','sigma':'1.0'},
                {'name':'ScaleEB_Zee','title':'ScaleEB_Zee','type':'signal_shape','mode':'scales','mean':'0.0','sigma':'1.0'},
                {'name':'ScaleEB_Zmmg','title':'ScaleEB_Zmmg','type':'signal_shape','mode':'scales','mean':'0.0','sigma':'1.0'},
                {'name':'ScaleEE_Zee','title':'ScaleEE_Zee','type':'signal_shape','mode':'scales','mean':'0.0','sigma':'1.0'},
                {'name':'ScaleEE_Zmmg','title':'ScaleEE_Zmmg','type':'signal_shape','mode':'scales','mean':'0.0','sigma':'1.0'},
                {'name':'Smearing','title':'Smearing','type':'signal_shape','mode':'smears','mean':'0.0','sigma':'1.0'},
]