micromamba activate higgs-dna-FF
cd HiggsDNA_21Feb/higgs_dna/scripts/postprocessing/
#python create_dir_structure.py -i /eos/cms/store/group/phys_higgs/cmshgg/Run3HggSTXS_working/Run3HggSTXS-all2022MC_0fa29a5b449779fc669985823d131ba8386a2dfa_22b0c33dda06afbeef4aa0bab5e5db74f0285803_2024-11-23/processed/multiclassifier_ff_corrected.parquet --target /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march
python create_dir_structure.py -i /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/final_fits_corrected.parquet --target /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march

python3 prepare_output_file.py --input /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal --merge  --cats --catDict config_jsons/for_HIG_STXSRUN3/category_STXS_stage0.json --skip-normalisation
python3 prepare_output_file.py --input /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal --root  --cats --catDict config_jsons/for_HIG_STXSRUN3/category_STXS_stage0.json 
python3 prepare_output_file.py --input /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/data --merge  --cats --catDict config_jsons/for_HIG_STXSRUN3/category_STXS_stage0.json --skip-normalisation
python3 prepare_output_file.py --input /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/data --root  --cats --catDict config_jsons/for_HIG_STXSRUN3/category_STXS_stage0.json


cd ../../../../higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Trees2WS
micromamba deactivate
cmsenv
source ../setup.sh



python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/gghtruth/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root  --inputMass 125 --productionMode gghtruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/tthtruth/output_TTHToGG_M125_13TeV_amcatnlo_pythia8.root  --inputMass 125 --productionMode tthtruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/thtruth/output_THToGG_M125_13TeV_amcatnlo_pythia8.root  --inputMass 125 --productionMode thtruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/whltruth/output_WHlToGG_M125_13TeV_amcatnlo_pythia8.root  --inputMass 125 --productionMode whltruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/zhltruth/output_ZHlToGG_M125_13TeV_amcatnlo_pythia8.root  --inputMass 125 --productionMode zhltruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/vbftruth/output_VBFHToGG_M125_13TeV_amcatnlo_pythia8.root  --inputMass 125 --productionMode vbftruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/vhqtruth/output_VHQToGG_M125_13TeV_amcatnlo_pythia8.root  --inputMass 125 --productionMode vhqtruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/bbhtruth/output_BBHToGG_M125_13TeV_amcatnloFXFX_pythia8.root  --inputMass 125 --productionMode bbhtruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/ggzhtruth/output_GluGluZToLLHToGG_M125_13TeV_amcatnloFXFX_pythia8.root  --inputMass 125 --productionMode ggzhtruth --year 2022preEE


python3 trees2ws_data.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/data/root/Data/allData_data.root 



#fix the ws naming extensions
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/gghtruth/ws_gghtruth/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_gghtruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces_11march/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/tthtruth/ws_tthtruth/output_TTHToGG_M125_13TeV_amcatnlo_pythia8_tthtruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces_11march/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/thtruth/ws_thtruth/output_THToGG_M125_13TeV_amcatnlo_pythia8_thtruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces_11march/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/whltruth/ws_whltruth/output_WHlToGG_M125_13TeV_amcatnlo_pythia8_whltruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces_11march/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/zhltruth/ws_zhltruth/output_ZHlToGG_M125_13TeV_amcatnlo_pythia8_zhltruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces_11march/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/vbftruth/ws_vbftruth/output_VBFHToGG_M125_13TeV_amcatnlo_pythia8_vbftruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces_11march/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/vhqtruth/ws_vhqtruth/output_VHQToGG_M125_13TeV_amcatnlo_pythia8_vhqtruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces_11march/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/bbhtruth/ws_bbhtruth/output_BBHToGG_M125_13TeV_amcatnloFXFX_pythia8_bbhtruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces_11march/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified_5march/signal/root/ggzhtruth/ws_ggzhtruth/output_GluGluZToLLHToGG_M125_13TeV_amcatnloFXFX_pythia8_ggzhtruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces_11march/signal_2022preEE

cd ../Signal

#python3 ../scripts/fTest.py --cat tth --procs GG2H,TTH,VBF,whl,zhl --ext tutorial_2022preEE --inputWSDir ../../Workspaces_tutorial/workspaces/signal_2022preEE
python3 RunSignalScripts.py --inputConfig config_tutorial_2022preEE.py --mode fTest --modeOpts "--doPlots"
for i in {0,1,2,3,4,5}; do ./outdir_tutorial_2022preEE/fTest/jobs/condor_fTest_tutorial_2022preEE.sh ${i};done

python3 RunSignalScripts.py --inputConfig config_tutorial_2022preEE.py --mode signalFit --modeOpts "--doPlots" --groupSignalFitJobsByCat
for i in {0,1,2,3,4,5}; do ./outdir_tutorial_2022preEE/signalFit/jobs/condor_signalFit_tutorial_2022preEE.sh ${i};done

python3 RunPackager.py --cats GGH_RECO,TH_RECO,TTH_RECO,VBF_VHQ_RECO,WHleptonic_RECO,ZHleptonic_RECO --exts tutorial_2022preEE --mergeYears --massPoints 125
for cat in {"GGH_RECO","TH_RECO","TTH_RECO","VBF_VHQ_RECO","WHleptonic_RECO","ZHleptonic_RECO"}; do python3 RunPlotter.py --procs all --years 2022preEE --cats $cat --ext packaged; done


cd ../Background

python3 RunBackgroundScripts.py --inputConfig config_tutorial.py --mode fTestParallel

for i in {"GGH_RECO","TH_RECO","TTH_RECO","VBF_VHQ_RECO","WHleptonic_RECO","ZHleptonic_RECO"}; do python3 ../Plots/makeMultipdfPlot.py --inputWSFile ../Background/outdir_tutorial/CMS-HGG_multipdf_${i}.root --cat $i --ext tutorial --mass 125.38 --inputSignalWSFile ../Signal/outdir_packaged/CMS-HGG_sigfit_packaged_${i}.root;done

cd ../Datacard

python3 RunYields.py --inputWSDirMap 2022preEE=/eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces_11march/signal_2022preEE --cats auto --procs auto --ext Run3STXS --mergeYears --skipCOWCorr  --batch condor --queue espresso
python3 makeDatacard.py --ext Run3STXS  --analysis Run3STXS --years 2022preEE --doTrueYield --skipCOWCorr  --doMCStatUncertainty --saveDataFrame --output Datacard_tutorial


cd ../Combine

cp ../Datacard/Datacard_tutorial.txt .



rsync -av /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Background/outdir_tutorial/* Models/background --exclude bkgfTest-Data --exclude fTestParallel 
rsync -av /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Signal/outdir_packaged/* Models/signal --exclude packageSignal --exclude Plots  

python3 RunText2Workspace.py --mode mu_inclusive --batch local --ext _tutorial

#asimov
python3 RunFits.py --inputJson inputs_tutorial/inputs_tutorial_bestfit_syst.json --mode mu_inclusive --ext _tutorial --mass 125.38 --batch condor --queue espresso 
./runFits_tutorial_mu_inclusive/condor_bestfit_syst_r.sh 0

python3 RunFits.py --inputJson inputs_tutorial/inputs_tutorial_profile1D_syst.json --mode mu_STXS0 --ext _tutorial --mass 125.38 --batch condor --queue espresso 
hadd scan.root higgsCombine_profile1D_syst_r.POINTS.*
./runFits_tutorial_mu_inclusive/condor_profile1D_syst_r.sh 0
./runFits_tutorial_mu_inclusive/condor_profile1D_syst_r.sh 1
hadd -f scan.root runFits_tutorial_mu_inclusive/higgsCombine_profile1D_syst_r.POINTS.*

plot1DScan.py test.root --y-cut 50 --y-max 20 -o profile1D.r.asimov.tutorial --POI r --main-label Syst --main-color 1 --breakdown Stat --logo-sub Internal

#STXS0
python3 RunFits.py --inputJson inputs_tutorial/inputs_tutorial_bestfit_syst.json --mode mu_STXS0 --ext _tutorial --mass 125.38 --batch condor --queue espresso 
for i in {"r_gghtruth","r_tthtruth","r_thtruth","r_vbftruth","r_whltruth","r_zhltruth"}; do ./runFits_tutorial_mu_STXS0/condor_profile1D_statonly_${i}.sh 0;done 
cd runFits_tutorial_mu_STXS0/
mkdir plots
cd ..
for i in {"r_gghtruth","r_tthtruth","r_thtruth","r_vbftruth","r_whltruth","r_zhltruth"}; do plot1DScan.py runFits_tutorial_mu_STXS0/higgsCombine_profile1D_statonly_${i}.POINTS.0.39.MultiDimFit.mH125.38.root --y-cut 50 --y-max 20 -o runFits_tutorial_mu_STXS0/plots/profile1D.${i}.asimov.tutorial --POI ${i} --main-label Stat --main-color 1 --breakdown Stat --logo-sub Internal;done

#now observed sensitivity, pulls, yields, impacts, postfit etc