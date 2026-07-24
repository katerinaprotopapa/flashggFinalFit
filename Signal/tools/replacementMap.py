# Python script to hold replacement model mapping for different analyses
from collections import OrderedDict as od

# Add analyses to globalReplacementMap. See "STXS" as an example
globalReplacementMap = od()

# Example analysis which with cats Untagged_Tag0,VBF_Tag0
globalReplacementMap['example'] = od()
# For WRONG VERTEX SCENARIO:
#  * single proc x cat for wrong vertex since for dZ > 1cm shape independent of proc x cat
#  * use proc x cat with highest number of WV events
globalReplacementMap['example']['procWV'] = "GG2H"
globalReplacementMap['example']['catWV'] = "Untagged_Tag0"
# For RIGHT VERTEX SCENARIO:
#  * default you should add is diagonal process from given category 
#  * if few events in diagonal process then may need to change the category aswell (see catRVMap)
#  * map must contain entry for all cats being processed (for replacement proc and cat)
globalReplacementMap['example']['procRVMap'] = od()
globalReplacementMap["example"]["procRVMap"]["Untagged_Tag0"] = "GG2H"
globalReplacementMap["example"]["procRVMap"]["VBF_Tag0"] = "VBF"
# Replacement category for RV fit
globalReplacementMap["example"]["catRVMap"] = od()
globalReplacementMap["example"]["catRVMap"]["Untagged_Tag0"] = "Untagged_Tag0"
globalReplacementMap["example"]["catRVMap"]["VBF_Tag0"] = "VBF_Tag0"

# Tutorial analysis
globalReplacementMap['tutorial'] = od()
# For WRONG VERTEX SCENARIO:
#  * single proc x cat for wrong vertex since for dZ > 1cm shape independent of proc x cat
#  * use proc x cat with highest number of WV events
globalReplacementMap['tutorial']['procWV'] = "GG2H"
globalReplacementMap['tutorial']['catWV'] = "EBEB_highR9highR9"
# For RIGHT VERTEX SCENARIO
#  * default mapping is to use diagonal process from given category 
#  * if few events in diagonal process then may need to change the category aswell (see catRVMap)
#  * map must contain entry for all cats being processed (for replacement proc and cat)
globalReplacementMap['tutorial']['procRVMap'] = od()
globalReplacementMap["tutorial"]["procRVMap"]["EBEB_highR9highR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EBEB_highR9lowR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EBEB_lowR9highR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EBEE_highR9highR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EBEE_highR9lowR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EBEE_lowR9highR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EEEB_highR9highR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EEEB_highR9lowR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EEEB_lowR9highR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EEEE_incl"] = "GG2H"
globalReplacementMap['tutorial']['catRVMap'] = od()
globalReplacementMap["tutorial"]["catRVMap"]["EBEB_highR9highR9"] = "EBEB_highR9highR9"
globalReplacementMap["tutorial"]["catRVMap"]["EBEB_highR9lowR9"] = "EBEB_highR9lowR9"
globalReplacementMap["tutorial"]["catRVMap"]["EBEB_lowR9highR9"] = "EBEB_lowR9highR9"
globalReplacementMap["tutorial"]["catRVMap"]["EBEE_highR9highR9"] = "EBEE_highR9highR9"
globalReplacementMap["tutorial"]["catRVMap"]["EBEE_highR9lowR9"] = "EBEE_highR9lowR9"
globalReplacementMap["tutorial"]["catRVMap"]["EBEE_lowR9highR9"] = "EBEE_lowR9highR9"
globalReplacementMap["tutorial"]["catRVMap"]["EEEB_highR9highR9"] = "EEEB_highR9highR9"
globalReplacementMap["tutorial"]["catRVMap"]["EEEB_highR9lowR9"] = "EEEB_highR9lowR9"
globalReplacementMap["tutorial"]["catRVMap"]["EEEB_lowR9highR9"] = "EEEB_lowR9highR9"
globalReplacementMap["tutorial"]["catRVMap"]["EEEE_incl"] = "EEEE_incl"


# STXS analysis
globalReplacementMap['STXS'] = od()
# For WRONG VERTEX SCENARIO:
#  * single proc x cat for wrong vertex since for dZ > 1cm shape independent of proc x cat
#  * use proc x cat with highest number of WV events
globalReplacementMap['STXS']['procWV'] = "GG2H_0J_PTH_GT10"
globalReplacementMap['STXS']['catWV'] = "RECO_0J_PTH_GT10_Tag1"
# For RIGHT VERTEX SCENARIO:
#  * default mapping is to use diagonal process from given category 
#  * if few events in diagonal process then may need to change the category aswell (see catRVMap)
#  * map must contain entry for all cats being processed (for replacement proc and cat)
globalReplacementMap['STXS']['procRVMap'] = od()
globalReplacementMap["STXS"]["procRVMap"]["RECO_0J_PTH_0_10_Tag0"] = "GG2H_0J_PTH_0_10"
globalReplacementMap["STXS"]["procRVMap"]["RECO_0J_PTH_0_10_Tag1"] = "GG2H_0J_PTH_0_10"
globalReplacementMap["STXS"]["procRVMap"]["RECO_0J_PTH_0_10_Tag2"] = "GG2H_0J_PTH_0_10"
globalReplacementMap["STXS"]["procRVMap"]["RECO_0J_PTH_GT10_Tag0"] = "GG2H_0J_PTH_GT10"
globalReplacementMap["STXS"]["procRVMap"]["RECO_0J_PTH_GT10_Tag1"] = "GG2H_0J_PTH_GT10"
globalReplacementMap["STXS"]["procRVMap"]["RECO_0J_PTH_GT10_Tag2"] = "GG2H_0J_PTH_GT10"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_0_60_Tag0"] = "GG2H_1J_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_0_60_Tag1"] = "GG2H_1J_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_0_60_Tag2"] = "GG2H_1J_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_120_200_Tag0"] = "GG2H_1J_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_120_200_Tag1"] = "GG2H_1J_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_120_200_Tag2"] = "GG2H_1J_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_60_120_Tag0"] = "GG2H_1J_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_60_120_Tag1"] = "GG2H_1J_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_60_120_Tag2"] = "GG2H_1J_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_0_60_Tag0"] = "GG2H_GE2J_MJJ_0_350_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_0_60_Tag1"] = "GG2H_GE2J_MJJ_0_350_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_0_60_Tag2"] = "GG2H_GE2J_MJJ_0_350_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_120_200_Tag0"] = "GG2H_GE2J_MJJ_0_350_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_120_200_Tag1"] = "GG2H_GE2J_MJJ_0_350_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_120_200_Tag2"] = "GG2H_GE2J_MJJ_0_350_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_60_120_Tag0"] = "GG2H_GE2J_MJJ_0_350_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_60_120_Tag1"] = "GG2H_GE2J_MJJ_0_350_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_60_120_Tag2"] = "GG2H_GE2J_MJJ_0_350_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_PTH_200_300_Tag0"] = "GG2H_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_PTH_200_300_Tag1"] = "GG2H_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_PTH_300_450_Tag0"] = "GG2H_PTH_300_450"
globalReplacementMap["STXS"]["procRVMap"]["RECO_PTH_300_450_Tag1"] = "GG2H_PTH_300_450"
globalReplacementMap["STXS"]["procRVMap"]["RECO_PTH_450_650_Tag0"] = "GG2H_PTH_450_650"
globalReplacementMap["STXS"]["procRVMap"]["RECO_PTH_GT650_Tag0"] = "GG2H_PTH_GT650"
globalReplacementMap["STXS"]["procRVMap"]["RECO_THQ_LEP"] = "THQ"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag0"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag1"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag2"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag3"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag0"] = "TTH_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag1"] = "TTH_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag2"] = "TTH_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag3"] = "TTH_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_200_300_Tag0"] = "TTH_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_200_300_Tag1"] = "TTH_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_200_300_Tag2"] = "TTH_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag0"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag1"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag2"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag3"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_GT300_Tag0"] = "TTH_PTH_GT300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_GT300_Tag1"] = "TTH_PTH_GT300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_GT300_Tag2"] = "TTH_PTH_GT300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_0_60_Tag0"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_0_60_Tag1"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_0_60_Tag2"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_120_200_Tag0"] = "TTH_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_120_200_Tag1"] = "TTH_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_200_300_Tag0"] = "TTH_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_200_300_Tag1"] = "TTH_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_60_120_Tag0"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_60_120_Tag1"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_60_120_Tag2"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_GT300_Tag0"] = "TTH_PTH_GT300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFLIKEGGH_Tag0"] = "GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFLIKEGGH_Tag1"] = "GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_BSM_Tag0"] = "VBF_GE2J_MJJ_GT350_PTH_GT200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_BSM_Tag1"] = "VBF_GE2J_MJJ_GT350_PTH_GT200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag0"] = "VBF_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag1"] = "VBF_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag0"] = "VBF_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag1"] = "VBF_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3_HIGHMJJ_Tag0"] = "VBF_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3_HIGHMJJ_Tag1"] = "VBF_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3_LOWMJJ_Tag0"] = "GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3_LOWMJJ_Tag1"] = "GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_VHHAD_Tag0"] = "WH2HQQ_GE2J_MJJ_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_VHHAD_Tag1"] = "GG2H_GE2J_MJJ_0_350_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VH_MET_Tag0"] = "QQ2HLL_PTV_150_250_0J"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VH_MET_Tag1"] = "QQ2HLL_PTV_75_150"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VH_MET_Tag2"] = "QQ2HLL_PTV_75_150"
globalReplacementMap["STXS"]["procRVMap"]["RECO_WH_LEP_PTV_0_75_Tag0"] = "QQ2HLNU_PTV_0_75"
globalReplacementMap["STXS"]["procRVMap"]["RECO_WH_LEP_PTV_0_75_Tag1"] = "QQ2HLNU_PTV_0_75"
globalReplacementMap["STXS"]["procRVMap"]["RECO_WH_LEP_PTV_75_150_Tag0"] = "QQ2HLNU_PTV_75_150"
globalReplacementMap["STXS"]["procRVMap"]["RECO_WH_LEP_PTV_75_150_Tag1"] = "QQ2HLNU_PTV_75_150"
globalReplacementMap["STXS"]["procRVMap"]["RECO_WH_LEP_PTV_GT150_Tag0"] = "QQ2HLNU_PTV_150_250_0J"
globalReplacementMap["STXS"]["procRVMap"]["RECO_ZH_LEP_Tag0"] = "QQ2HLL_PTV_0_75"
globalReplacementMap["STXS"]["procRVMap"]["RECO_ZH_LEP_Tag1"] = "QQ2HLL_PTV_0_75"
# Replacement category for RV fit
globalReplacementMap["STXS"]["catRVMap"] = od()
globalReplacementMap["STXS"]["catRVMap"]["RECO_0J_PTH_0_10_Tag0"] = "RECO_0J_PTH_0_10_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_0J_PTH_0_10_Tag1"] = "RECO_0J_PTH_0_10_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_0J_PTH_0_10_Tag2"] = "RECO_0J_PTH_0_10_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_0J_PTH_GT10_Tag0"] = "RECO_0J_PTH_GT10_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_0J_PTH_GT10_Tag1"] = "RECO_0J_PTH_GT10_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_0J_PTH_GT10_Tag2"] = "RECO_0J_PTH_GT10_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_0_60_Tag0"] = "RECO_1J_PTH_0_60_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_0_60_Tag1"] = "RECO_1J_PTH_0_60_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_0_60_Tag2"] = "RECO_1J_PTH_0_60_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_120_200_Tag0"] = "RECO_1J_PTH_120_200_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_120_200_Tag1"] = "RECO_1J_PTH_120_200_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_120_200_Tag2"] = "RECO_1J_PTH_120_200_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_60_120_Tag0"] = "RECO_1J_PTH_60_120_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_60_120_Tag1"] = "RECO_1J_PTH_60_120_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_60_120_Tag2"] = "RECO_1J_PTH_60_120_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_0_60_Tag0"] = "RECO_GE2J_PTH_0_60_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_0_60_Tag1"] = "RECO_GE2J_PTH_0_60_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_0_60_Tag2"] = "RECO_GE2J_PTH_0_60_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_120_200_Tag0"] = "RECO_GE2J_PTH_120_200_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_120_200_Tag1"] = "RECO_GE2J_PTH_120_200_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_120_200_Tag2"] = "RECO_GE2J_PTH_120_200_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_60_120_Tag0"] = "RECO_GE2J_PTH_60_120_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_60_120_Tag1"] = "RECO_GE2J_PTH_60_120_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_60_120_Tag2"] = "RECO_GE2J_PTH_60_120_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_PTH_200_300_Tag0"] = "RECO_PTH_200_300_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_PTH_200_300_Tag1"] = "RECO_PTH_200_300_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_PTH_300_450_Tag0"] = "RECO_PTH_300_450_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_PTH_300_450_Tag1"] = "RECO_PTH_300_450_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_PTH_450_650_Tag0"] = "RECO_PTH_450_650_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_PTH_GT650_Tag0"] = "RECO_PTH_GT650_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_THQ_LEP"] = "RECO_THQ_LEP"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag0"] = "RECO_TTH_HAD_PTH_0_60_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag1"] = "RECO_TTH_HAD_PTH_0_60_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag2"] = "RECO_TTH_HAD_PTH_0_60_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag3"] = "RECO_TTH_HAD_PTH_0_60_Tag3"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag0"] = "RECO_TTH_HAD_PTH_120_200_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag1"] = "RECO_TTH_HAD_PTH_120_200_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag2"] = "RECO_TTH_HAD_PTH_120_200_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag3"] = "RECO_TTH_HAD_PTH_120_200_Tag3"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_200_300_Tag0"] = "RECO_TTH_HAD_PTH_200_300_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_200_300_Tag1"] = "RECO_TTH_HAD_PTH_200_300_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_200_300_Tag2"] = "RECO_TTH_HAD_PTH_200_300_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag0"] = "RECO_TTH_HAD_PTH_60_120_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag1"] = "RECO_TTH_HAD_PTH_60_120_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag2"] = "RECO_TTH_HAD_PTH_60_120_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag3"] = "RECO_TTH_HAD_PTH_60_120_Tag3"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_GT300_Tag0"] = "RECO_TTH_HAD_PTH_GT300_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_GT300_Tag1"] = "RECO_TTH_HAD_PTH_GT300_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_GT300_Tag2"] = "RECO_TTH_HAD_PTH_GT300_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_0_60_Tag0"] = "RECO_TTH_LEP_PTH_0_60_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_0_60_Tag1"] = "RECO_TTH_LEP_PTH_0_60_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_0_60_Tag2"] = "RECO_TTH_LEP_PTH_0_60_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_120_200_Tag0"] = "RECO_TTH_LEP_PTH_120_200_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_120_200_Tag1"] = "RECO_TTH_LEP_PTH_120_200_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_200_300_Tag0"] = "RECO_TTH_LEP_PTH_200_300_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_200_300_Tag1"] = "RECO_TTH_LEP_PTH_200_300_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_60_120_Tag0"] = "RECO_TTH_LEP_PTH_60_120_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_60_120_Tag1"] = "RECO_TTH_LEP_PTH_60_120_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_60_120_Tag2"] = "RECO_TTH_LEP_PTH_60_120_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_GT300_Tag0"] = "RECO_TTH_LEP_PTH_GT300_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFLIKEGGH_Tag0"] = "RECO_VBFLIKEGGH_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFLIKEGGH_Tag1"] = "RECO_VBFLIKEGGH_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_BSM_Tag0"] = "RECO_VBFTOPO_BSM_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_BSM_Tag1"] = "RECO_VBFTOPO_BSM_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag0"] = "RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag1"] = "RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag0"] = "RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag1"] = "RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3_HIGHMJJ_Tag0"] = "RECO_VBFTOPO_JET3_HIGHMJJ_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3_HIGHMJJ_Tag1"] = "RECO_VBFTOPO_JET3_HIGHMJJ_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3_LOWMJJ_Tag0"] = "RECO_VBFTOPO_JET3_LOWMJJ_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3_LOWMJJ_Tag1"] = "RECO_VBFTOPO_JET3_LOWMJJ_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_VHHAD_Tag0"] = "RECO_VBFTOPO_VHHAD_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_VHHAD_Tag1"] = "RECO_VBFTOPO_VHHAD_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VH_MET_Tag0"] = "RECO_VH_MET_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VH_MET_Tag1"] = "RECO_VH_MET_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VH_MET_Tag2"] = "RECO_VH_MET_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_WH_LEP_PTV_0_75_Tag0"] = "RECO_WH_LEP_PTV_0_75_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_WH_LEP_PTV_0_75_Tag1"] = "RECO_WH_LEP_PTV_0_75_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_WH_LEP_PTV_75_150_Tag0"] = "RECO_WH_LEP_PTV_75_150_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_WH_LEP_PTV_75_150_Tag1"] = "RECO_WH_LEP_PTV_75_150_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_WH_LEP_PTV_GT150_Tag0"] = "RECO_WH_LEP_PTV_GT150_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_ZH_LEP_Tag0"] = "RECO_ZH_LEP_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_ZH_LEP_Tag1"] = "RECO_ZH_LEP_Tag1"

# kl analysis - C1reco
globalReplacementMap['kl_C1reco'] = od()
# For WRONG VERTEX SCENARIO:
#  * single proc x cat for wrong vertex since for dZ > 1cm shape independent of proc x cat
#  * use proc x cat with highest number of WV events
globalReplacementMap['kl_C1reco']['procWV'] = "TTH"
globalReplacementMap['kl_C1reco']['catWV'] = "hadr_C1_10_29"
# For RIGHT VERTEX SCENARIO:
#  * default mapping is to use diagonal process from given category 
#  * if few events in diagonal process then may need to change the category aswell (see catRVMap)
#  * map must contain entry for all cats being processed (for replacement proc and cat)
# Previous (boundary-based) categorisation, kept for reference
# globalReplacementMap['kl_C1reco']['procRVMap'] = od()
# globalReplacementMap["kl_C1reco"]["procRVMap"]["hadr_C1_LT_20"] = "ttH"
# globalReplacementMap["kl_C1reco"]["procRVMap"]["hadr_C1_20_40"] = "ttH"
# globalReplacementMap["kl_C1reco"]["procRVMap"]["hadr_C1_40_60"] = "ttH"
# globalReplacementMap["kl_C1reco"]["procRVMap"]["hadr_C1_60_80"] = "ttH"
# globalReplacementMap["kl_C1reco"]["procRVMap"]["hadr_C1_GT_80"] = "ttH"
# globalReplacementMap["kl_C1reco"]["procRVMap"]["lept_C1_LT_15"] = "ttH"
# globalReplacementMap["kl_C1reco"]["procRVMap"]["lept_C1_15_30"] = "ttH"
# globalReplacementMap["kl_C1reco"]["procRVMap"]["lept_C1_30_45"] = "ttH"
# globalReplacementMap["kl_C1reco"]["procRVMap"]["lept_C1_45_60"] = "ttH"
# globalReplacementMap["kl_C1reco"]["procRVMap"]["lept_C1_60_75"] = "ttH"
# globalReplacementMap["kl_C1reco"]["procRVMap"]["lept_C1_GT_75"] = "ttH"
# globalReplacementMap["kl_C1reco"]["catRVMap"] = od()
# globalReplacementMap["kl_C1reco"]["catRVMap"]["hadr_C1_LT_20"] = "hadr_C1_LT_20"
# globalReplacementMap["kl_C1reco"]["catRVMap"]["hadr_C1_20_40"] = "hadr_C1_20_40"
# globalReplacementMap["kl_C1reco"]["catRVMap"]["hadr_C1_40_60"] = "hadr_C1_40_60"
# globalReplacementMap["kl_C1reco"]["catRVMap"]["hadr_C1_60_80"] = "hadr_C1_60_80"
# globalReplacementMap["kl_C1reco"]["catRVMap"]["hadr_C1_GT_80"] = "hadr_C1_GT_80"
# globalReplacementMap["kl_C1reco"]["catRVMap"]["lept_C1_LT_15"] = "lept_C1_LT_15"
# globalReplacementMap["kl_C1reco"]["catRVMap"]["lept_C1_15_30"] = "lept_C1_15_30"
# globalReplacementMap["kl_C1reco"]["catRVMap"]["lept_C1_30_45"] = "lept_C1_30_45"
# globalReplacementMap["kl_C1reco"]["catRVMap"]["lept_C1_45_60"] = "lept_C1_45_60"
# globalReplacementMap["kl_C1reco"]["catRVMap"]["lept_C1_60_75"] = "lept_C1_60_75"
# globalReplacementMap["kl_C1reco"]["catRVMap"]["lept_C1_GT_75"] = "lept_C1_GT_75"

globalReplacementMap['kl_C1reco']['procRVMap'] = od()
globalReplacementMap["kl_C1reco"]["procRVMap"]["hadr_C1_LT_10"] = "TTH"
globalReplacementMap["kl_C1reco"]["procRVMap"]["hadr_C1_10_21"] = "TTH"
globalReplacementMap["kl_C1reco"]["procRVMap"]["hadr_C1_21_30"] = "TTH"
globalReplacementMap["kl_C1reco"]["procRVMap"]["hadr_C1_30_36"] = "TTH"
globalReplacementMap["kl_C1reco"]["procRVMap"]["hadr_C1_36_42"] = "TTH"
globalReplacementMap["kl_C1reco"]["procRVMap"]["hadr_C1_42_63"] = "TTH"
globalReplacementMap["kl_C1reco"]["procRVMap"]["hadr_C1_GT_63"] = "TTH"
globalReplacementMap["kl_C1reco"]["procRVMap"]["lept_C1_LT_15"] = "TTH"
globalReplacementMap["kl_C1reco"]["procRVMap"]["lept_C1_15_30"] = "TTH"
globalReplacementMap["kl_C1reco"]["procRVMap"]["lept_C1_30_43"] = "TTH"
globalReplacementMap["kl_C1reco"]["procRVMap"]["lept_C1_43_63"] = "TTH"
globalReplacementMap["kl_C1reco"]["procRVMap"]["lept_C1_63_70"] = "TTH"
globalReplacementMap["kl_C1reco"]["procRVMap"]["lept_C1_GT_70"] = "TTH"

# Replacement category for RV fit
globalReplacementMap["kl_C1reco"]["catRVMap"] = od()
globalReplacementMap["kl_C1reco"]["catRVMap"]["hadr_C1_LT_10"] = "hadr_C1_LT_10"
globalReplacementMap["kl_C1reco"]["catRVMap"]["hadr_C1_10_21"] = "hadr_C1_10_21"
globalReplacementMap["kl_C1reco"]["catRVMap"]["hadr_C1_21_30"] = "hadr_C1_21_30"
globalReplacementMap["kl_C1reco"]["catRVMap"]["hadr_C1_30_36"] = "hadr_C1_30_36"
globalReplacementMap["kl_C1reco"]["catRVMap"]["hadr_C1_36_42"] = "hadr_C1_36_42"
globalReplacementMap["kl_C1reco"]["catRVMap"]["hadr_C1_42_63"] = "hadr_C1_42_63"
globalReplacementMap["kl_C1reco"]["catRVMap"]["hadr_C1_GT_63"] = "hadr_C1_GT_63"
globalReplacementMap["kl_C1reco"]["catRVMap"]["lept_C1_LT_15"] = "lept_C1_LT_15"
globalReplacementMap["kl_C1reco"]["catRVMap"]["lept_C1_15_30"] = "lept_C1_15_30"
globalReplacementMap["kl_C1reco"]["catRVMap"]["lept_C1_30_43"] = "lept_C1_30_43"
globalReplacementMap["kl_C1reco"]["catRVMap"]["lept_C1_43_63"] = "lept_C1_43_63"
globalReplacementMap["kl_C1reco"]["catRVMap"]["lept_C1_63_70"] = "lept_C1_63_70"
globalReplacementMap["kl_C1reco"]["catRVMap"]["lept_C1_GT_70"] = "lept_C1_GT_70"

# kl analysis - pt
globalReplacementMap['kl_pt'] = od()
# For WRONG VERTEX SCENARIO:
#  * single proc x cat for wrong vertex since for dZ > 1cm shape independent of proc x cat
#  * use proc x cat with highest number of WV events
globalReplacementMap['kl_pt']['procWV'] = "ttH"
globalReplacementMap['kl_pt']['catWV'] = "hadr_C1_10_29"
# For RIGHT VERTEX SCENARIO:
#  * default mapping is to use diagonal process from given category 
#  * if few events in diagonal process then may need to change the category aswell (see catRVMap)
#  * map must contain entry for all cats being processed (for replacement proc and cat)
globalReplacementMap['kl_pt']['procRVMap'] = od()
globalReplacementMap["kl_pt"]["procRVMap"]["hadr_pt_LT_60"] = "ttH"
globalReplacementMap["kl_pt"]["procRVMap"]["hadr_pt_60_120"] = "ttH"
globalReplacementMap["kl_pt"]["procRVMap"]["hadr_pt_120_200"] = "ttH"
globalReplacementMap["kl_pt"]["procRVMap"]["hadr_pt_200_300"] = "ttH"
globalReplacementMap["kl_pt"]["procRVMap"]["hadr_pt_GT_300"] = "ttH"
globalReplacementMap["kl_pt"]["procRVMap"]["lept_pt_LT_60"] = "ttH"
globalReplacementMap["kl_pt"]["procRVMap"]["lept_pt_60_120"] = "ttH"
globalReplacementMap["kl_pt"]["procRVMap"]["lept_pt_120_200"] = "ttH"
globalReplacementMap["kl_pt"]["procRVMap"]["lept_pt_200_300"] = "ttH"
globalReplacementMap["kl_pt"]["procRVMap"]["lept_pt_GT_300"] = "ttH"
# Replacement category for RV fit
globalReplacementMap["kl_pt"]["catRVMap"] = od()
globalReplacementMap["kl_pt"]["catRVMap"]["hadr_pt_LT_60"] = "hadr_pt_LT_60"
globalReplacementMap["kl_pt"]["catRVMap"]["hadr_pt_60_120"] = "hadr_pt_60_120"
globalReplacementMap["kl_pt"]["catRVMap"]["hadr_pt_120_200"] = "hadr_pt_120_200"
globalReplacementMap["kl_pt"]["catRVMap"]["hadr_pt_200_300"] = "hadr_pt_200_300"
globalReplacementMap["kl_pt"]["catRVMap"]["hadr_pt_GT_300"] = "hadr_pt_GT_300"
globalReplacementMap["kl_pt"]["catRVMap"]["lept_pt_LT_60"] = "lept_pt_LT_60"
globalReplacementMap["kl_pt"]["catRVMap"]["lept_pt_60_120"] = "lept_pt_60_120"
globalReplacementMap["kl_pt"]["catRVMap"]["lept_pt_120_200"] = "lept_pt_120_200"
globalReplacementMap["kl_pt"]["catRVMap"]["lept_pt_200_300"] = "lept_pt_200_300"
globalReplacementMap["kl_pt"]["catRVMap"]["lept_pt_GT_300"] = "lept_pt_GT_300"


