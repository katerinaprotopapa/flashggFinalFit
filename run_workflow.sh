


micromamba activate higgs-dna-FF
cd higgsdna_finalfits_tutorial_24/HiggsDNA/scripts/postprocessing/
python3 prepare_output_file.py --input ../../../05_postprocessing/classified/separate_parquets/ --merge  --cats --catDict ../../../05_postprocessing/configs/category_STXS_stage0.json --skip-normalisation
python3 prepare_output_file.py --input ../../../05_postprocessing/classified/separate_parquets/ --root  --cats --catDict ../../../05_postprocessing/configs/category_STXS_stage0.json 
python3 prepare_output_file.py --input ../../../05_postprocessing/classified/data/ --merge  --cats --catDict ../../../05_postprocessing/configs/category_STXS_stage0_data.json --skip-normalisation
python3 prepare_output_file.py --input ../../../05_postprocessing/classified/data/ --root  --cats --catDict ../../../05_postprocessing/configs/category_STXS_stage0_data.json 


cd ../../../07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Trees2WS
micromamba deactivate
cmsenv
source ../setup.sh



python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/separate_parquets/root/gghtruth/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root  --inputMass 125 --productionMode gghtruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/separate_parquets/root/tthtruth/output_TTHToGG_M125_13TeV_amcatnlo_pythia8.root  --inputMass 125 --productionMode tthtruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/separate_parquets/root/thtruth/output_THToGG_M125_13TeV_amcatnloFXFX_pythia8.root  --inputMass 125 --productionMode thtruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/separate_parquets/root/whleptonictruth/output_WHlToGG_M125_13TeV_amcatnlo_pythia8.root  --inputMass 125 --productionMode whltruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/separate_parquets/root/zhleptonictruth/output_ZHlToGG_M125_13TeV_amcatnlo_pythia8.root  --inputMass 125 --productionMode zhltruth --year 2022preEE
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/separate_parquets/root/vbfVhqtruth/output_VBFHToGG_M125_13TeV_amcatnlo_pythia8.root  --inputMass 125 --productionMode vbfVhqtruth --year 2022preEE

python3 trees2ws_data.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/data/root/Data/allData_data.root 




cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/separate_parquets/root/gghtruth/ws_gghtruth/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_gghtruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/separate_parquets/root/tthtruth/ws_tthtruth/output_TTHToGG_M125_13TeV_amcatnlo_pythia8_tthtruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/separate_parquets/root/thtruth/ws_thtruth/output_THToGG_M125_13TeV_amcatnloFXFX_pythia8_thtruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/separate_parquets/root/whleptonictruth/ws_whltruth/output_WHlToGG_M125_13TeV_amcatnlo_pythia8_whltruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/separate_parquets/root/zhleptonictruth/ws_zhltruth/output_ZHlToGG_M125_13TeV_amcatnlo_pythia8_zhltruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces/signal_2022preEE
cp /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/05_postprocessing/classified/separate_parquets/root/vbfVhqtruth/ws_vbfVhqtruth/output_VBFHToGG_M125_13TeV_amcatnlo_pythia8_vbfVhqtruth.root  /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces/signal_2022preEE

cd ../Signal

#python3 ../scripts/fTest.py --cat tth --procs GG2H,TTH,VBF,whl,zhl --ext tutorial_2022preEE --inputWSDir ../../Workspaces_tutorial/workspaces/signal_2022preEE
python3 RunSignalScripts.py --inputConfig config_tutorial_2022preEE.py --mode fTest --modeOpts "--doPlots"

python3 RunSignalScripts.py --inputConfig config_tutorial_2022preEE.py --mode signalFit --modeOpts "--doPlots" --groupSignalFitJobsByCat
python3 RunPackager.py --cats GGH_RECO,TH_RECO,TTH_RECO,VBF_VHQ_RECO,WHleptonic_RECO,ZHleptonic_RECO --exts tutorial_2022preEE --mergeYears --massPoints 125
for cat in {"GGH_RECO","TH_RECO","TTH_RECO","VBF_VHQ_RECO","WHleptonic_RECO","ZHleptonic_RECO"}; do python3 RunPlotter.py --procs all --years 2022preEE --cats $cat --ext packaged; done


cd ../Background

python3 RunBackgroundScripts.py --inputConfig config_tutorial.py --mode fTestParallel

for i in {"GGH_RECO","TH_RECO","TTH_RECO","VBF_VHQ_RECO","WHleptonic_RECO","ZHleptonic_RECO"}; do python3 ../Plots/makeMultipdfPlot.py --inputWSFile ../Background/outdir_tutorial/CMS-HGG_multipdf_${i}.root --cat $i --ext tutorial --mass 125.38 --inputSignalWSFile ../Signal/outdir_packaged/CMS-HGG_sigfit_packaged_${i}.root;done

cd ../Datacard

python3 RunYields.py --inputWSDirMap 2022preEE=/eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces/signal_2022preEE --cats auto --procs auto --ext Run3STXSX --mergeYears --skipCOWCorr  --batch condor --queue espresso
python3 makeDatacard.py --ext Run3STXS  --analysis Run3STXS --years 2022preEE --prune --doTrueYield --skipCOWCorr  --doMCStatUncertainty --saveDataFrame --output Datacard_tutorial


cd ../Combine

cp ../Datacard/Datacard_tutorial.txt .



rsync -av /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Background/outdir_tutorial/* Models/background --exclude bkgfTest-Data --exclude fTestParallel 
rsync -av /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Signal/outdir_packaged/* Models/signal --exclude packageSignal --exclude Plots  

python3 RunText2Workspace.py --mode mu_inclusive --batch local --ext _tutorial

#asimov
python3 RunFits.py --inputJson inputs_tutorial/inputs_tutorial_bestfit_syst.json --mode mu_inclusive --ext _tutorial --mass 125.38 --batch condor --queue espresso 
./runFits_tutorial_mu_inclusive/condor_bestfit_syst_r.sh 0


hadd scan.root higgsCombine_profile1D_syst_r.POINTS.*
./runFits_tutorial_mu_inclusive/condor_profile1D_syst_r.sh 0
./runFits_tutorial_mu_inclusive/condor_profile1D_syst_r.sh 1
hadd -f scan.root runFits_tutorial_mu_inclusive/higgsCombine_profile1D_syst_r.POINTS.*

plot1DScan.py runFits_tutorial_mu_inclusive/profile1D_syst_r.root --y-cut 50 --y-max 20 -o profile1D.r.asimov.tutorial --POI r --main-label Syst --main-color 1 --breakdown Stat --logo-sub Internal
#now observed sensitivity, pulls, yields, impacts, postfit etc