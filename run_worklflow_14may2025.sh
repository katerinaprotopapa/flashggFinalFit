micromamba activate higgs-dna-FF
cd src/run3hgg/postprocessing
python create_dir_structure.py -i /eos/user/p/pkrueper/STXS3_2025/src/run3hggstxs/classification/multiclassifier_extended/final_fits_corrected.parquet --target /eos/user/p/pkrueper/STXS3_2025/src/run3hggstxs/classification/multiclassifier_extended_finalfits

python3 prepare_output_file.py --input /eos/user/p/pkrueper/STXS3_2025/src/run3hggstxs/classification/multiclassifier_extended_finalfits/signal --merge  --cats --catDict config_jsons/for_HIG_STXSRUN3/category_STXS_stage0.json --skip-normalisation
python3 prepare_output_file.py --input /eos/user/p/pkrueper/STXS3_2025/src/run3hggstxs/classification/multiclassifier_extended_finalfits/signal --root  --cats --catDict config_jsons/for_HIG_STXSRUN3/category_STXS_stage0.json 
python3 prepare_output_file.py --input /eos/user/p/pkrueper/STXS3_2025/src/run3hggstxs/classification/multiclassifier_extended_finalfits/data --merge  --cats --catDict config_jsons/for_HIG_STXSRUN3/category_STXS_stage0.json --skip-normalisation
python3 prepare_output_file.py --input /eos/user/p/pkrueper/STXS3_2025/src/run3hggstxs/classification/multiclassifier_extended_finalfits/data --root  --cats --catDict config_jsons/for_HIG_STXSRUN3/category_STXS_stage0.json


cd /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Trees2WS
micromamba deactivate
cmsenv
source ../setup.sh

# no proc "WMINUSH2HQQ_FWDH_preEE" parquet empty, and ZH2HQQ_FWDH_preEE ZH2HNUNU_FWDH_preEE VBF_FWDH_preEE have 1 / 2 / 3 events
proc_x_stxs_x_era=("GG2H__preEE" "GG2H_FWDH_preEE" "GG2HQQ__preEE"   "GG2HLL__preEE" "GG2HLL_FWDH_preEE" "GG2HNUNU__preEE" "GG2HNUNU_FWDH_preEE" "TTH__preEE" "BBH__preEE" "THQ__preEE" "THQ_FWDH_preEE" "THW__preEE" "THW_FWDH_preEE" "WMINUSH2HLNU__preEE" "WMINUSH2HLNU_FWDH_preEE" "WMINUSH2HQQ__preEE"  "WPLUSH2HQQ__preEE" "WPLUSH2HLNU__preEE" "WPLUSH2HLNU_FWDH_preEE" "ZH2HLL__preEE" "ZH2HLL_FWDH_preEE" "ZH2HQQ__preEE"  "ZH2HNUNU__preEE"  "VBF__preEE" )
length=${#proc_x_stxs_x_era[@]}
for ((i=0;i<length;i++)); do python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/STXS3_2025/src/run3hggstxs/classification/multiclassifier_extended_finalfits/signal/root/${proc_x_stxs_x_era[i]}/output_${proc_x_stxs_x_era[i]}_M125_pythia8.root  --inputMass 125 --productionMode ${proc_x_stxs_x_era[i]}  --year 2022preEE;done
python3 trees2ws_data.py --inputConfig config_tutorial.py --inputTreeFile /eos/user/p/pkrueper/STXS3_2025/src/run3hggstxs/classification/multiclassifier_extended_finalfits/data/root/Data/allData_data.root   





for ((i=0;i<length;i++)); do cp /eos/user/p/pkrueper/STXS3_2025/src/run3hggstxs/classification/multiclassifier_extended_finalfits/signal/root/${proc_x_stxs_x_era[i]}/ws_${proc_x_stxs_x_era[i]}/output_${proc_x_stxs_x_era[i]}_M125_pythia8_${proc_x_stxs_x_era[i]}.root /eos/user/p/pkrueper/HiggsDNA_and_FinalFits_tutorial24/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/Workspaces_19may/signal; done


cd ../Signal

#python3 ../scripts/fTest.py --cat tth --procs GG2H,TTH,VBF,whl,zhl --ext tutorial_2022preEE --inputWSDir ../../Workspaces_tutorial/workspaces/signal_2022preEE
python3 RunSignalScripts.py --inputConfig config_tutorial_2022preEE.py --mode fTest --modeOpts "--doPlots"
for i in {0,1,2,3,4,5}; do ./outdir_tutorial_2022preEE/fTest/jobs/condor_fTest_tutorial_2022preEE.sh ${i};done

python3 RunSignalScripts.py --inputConfig config_tutorial_2022preEE.py --mode signalFit --modeOpts "--doPlots" --groupSignalFitJobsByCat
for i in {0,1,2,3,4,5}; do ./outdir_tutorial_2022preEE/signalFit/jobs/condor_signalFit_tutorial_2022preEE.sh ${i};done

python3 RunPackager.py --cats GGH_RECO,TH_RECO,TTH_RECO,VBF_VHQ_RECO,WHleptonic_RECO,ZHleptonic_RECO --exts Run3STXS_2022preEE --mergeYears --massPoints 125
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