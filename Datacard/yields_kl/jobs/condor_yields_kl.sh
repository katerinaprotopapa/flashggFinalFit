#!/bin/bash
ulimit -s unlimited
set -e
cd /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src
export SCRAM_ARCH=None
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
export PYTHONNOUSERSITE=1
cd /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard
export PYTHONPATH=$PYTHONPATH:/vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/tools:/vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard/tools

if [ $1 -eq 0 ]; then
  python3 /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard/makeYields.py --cat background --procs auto --ext kl --mass 125 --inputWSDirMap preEE=../RooWorkspaces_6Feb2026/signal/preEE,postEE=../RooWorkspaces_6Feb2026/signal/postEE  --mergeYears --systWeightScheme accEff --ignore-warnings
fi
if [ $1 -eq 1 ]; then
  python3 /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard/makeYields.py --cat ttH_hadr_C1_LT10 --procs auto --ext kl --mass 125 --inputWSDirMap preEE=../RooWorkspaces_6Feb2026/signal/preEE,postEE=../RooWorkspaces_6Feb2026/signal/postEE  --mergeYears --systWeightScheme accEff --ignore-warnings
fi
if [ $1 -eq 2 ]; then
  python3 /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard/makeYields.py --cat ttH_hadr_C1_10_29 --procs auto --ext kl --mass 125 --inputWSDirMap preEE=../RooWorkspaces_6Feb2026/signal/preEE,postEE=../RooWorkspaces_6Feb2026/signal/postEE  --mergeYears --systWeightScheme accEff --ignore-warnings
fi
if [ $1 -eq 3 ]; then
  python3 /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard/makeYields.py --cat ttH_hadr_C1_29_48 --procs auto --ext kl --mass 125 --inputWSDirMap preEE=../RooWorkspaces_6Feb2026/signal/preEE,postEE=../RooWorkspaces_6Feb2026/signal/postEE  --mergeYears --systWeightScheme accEff --ignore-warnings
fi
if [ $1 -eq 4 ]; then
  python3 /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard/makeYields.py --cat ttH_hadr_C1_48_71 --procs auto --ext kl --mass 125 --inputWSDirMap preEE=../RooWorkspaces_6Feb2026/signal/preEE,postEE=../RooWorkspaces_6Feb2026/signal/postEE  --mergeYears --systWeightScheme accEff --ignore-warnings
fi
if [ $1 -eq 5 ]; then
  python3 /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard/makeYields.py --cat ttH_hadr_C1_GT_71 --procs auto --ext kl --mass 125 --inputWSDirMap preEE=../RooWorkspaces_6Feb2026/signal/preEE,postEE=../RooWorkspaces_6Feb2026/signal/postEE  --mergeYears --systWeightScheme accEff --ignore-warnings
fi
if [ $1 -eq 6 ]; then
  python3 /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard/makeYields.py --cat ttH_lept_C1_LT10 --procs auto --ext kl --mass 125 --inputWSDirMap preEE=../RooWorkspaces_6Feb2026/signal/preEE,postEE=../RooWorkspaces_6Feb2026/signal/postEE  --mergeYears --systWeightScheme accEff --ignore-warnings
fi
if [ $1 -eq 7 ]; then
  python3 /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard/makeYields.py --cat ttH_lept_C1_10_29 --procs auto --ext kl --mass 125 --inputWSDirMap preEE=../RooWorkspaces_6Feb2026/signal/preEE,postEE=../RooWorkspaces_6Feb2026/signal/postEE  --mergeYears --systWeightScheme accEff --ignore-warnings
fi
if [ $1 -eq 8 ]; then
  python3 /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard/makeYields.py --cat ttH_lept_C1_29_48 --procs auto --ext kl --mass 125 --inputWSDirMap preEE=../RooWorkspaces_6Feb2026/signal/preEE,postEE=../RooWorkspaces_6Feb2026/signal/postEE  --mergeYears --systWeightScheme accEff --ignore-warnings
fi
if [ $1 -eq 9 ]; then
  python3 /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard/makeYields.py --cat ttH_lept_C1_48_71 --procs auto --ext kl --mass 125 --inputWSDirMap preEE=../RooWorkspaces_6Feb2026/signal/preEE,postEE=../RooWorkspaces_6Feb2026/signal/postEE  --mergeYears --systWeightScheme accEff --ignore-warnings
fi
if [ $1 -eq 10 ]; then
  python3 /vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Datacard/makeYields.py --cat ttH_lept_C1_GT_71 --procs auto --ext kl --mass 125 --inputWSDirMap preEE=../RooWorkspaces_6Feb2026/signal/preEE,postEE=../RooWorkspaces_6Feb2026/signal/postEE  --mergeYears --systWeightScheme accEff --ignore-warnings
fi
