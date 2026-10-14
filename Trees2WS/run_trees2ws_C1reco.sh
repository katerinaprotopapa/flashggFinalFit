#!/bin/bash
set -e

FINAL_FITS_DIR=/vols/cms/evp18/trilinear_higgs/run3hggstxs/src/run3hggstxs/final_fits
ROOWORKSPACES_DIR=/vols/cms/evp18/higgsdna_finalfits_tutorial_24/07_FinalFits/CMSSW_14_1_0_pre4/src/flashggFinalFit/RooWorkspaces/C1_reco/signal

eras=('preEE' 'postEE' 'preBPix' 'postBPix' '2024')

for era in "${eras[@]}"; do
    echo "=== era: $era ==="

    # procs = subdirectories in final_fits/MC/${era}/, excluding the data-driven background bucket
    procs=()
    for dir in "$FINAL_FITS_DIR"/MC/${era}/*/; do
        proc=$(basename "$dir")
        [ "$proc" == "background" ] && continue
        procs+=("$proc")
    done
    length=${#procs[@]}

    for ((i=0;i<length;i++)); do
        python3 trees2ws_kl.py \
            --inputConfig config_C1reco.py \
            --inputTreeFile "$FINAL_FITS_DIR/MC/${era}/${procs[i]}/nominal" \
            --inputMass 125 \
            --productionMode ${procs[i]} \
            --year ${era} \
            --doSystematics \
            --categorisationConfig config_categories_C1reco.json
    done

    mkdir -p "$ROOWORKSPACES_DIR/${era}"

    for ((i=0;i<length;i++)); do
        cp "$FINAL_FITS_DIR/MC/${era}/${procs[i]}/nominal/C1_reco/ws_${procs[i]}/output_${procs[i]}_M125_pythia8_${procs[i]}.root" \
           "$ROOWORKSPACES_DIR/${era}/"
    done
done

python3 trees2ws_data_kl.py \
    --inputConfig config_C1reco.py \
    --inputTreeFile "$FINAL_FITS_DIR/Data/merged" \
    --categorisationConfig config_categories_C1reco.json
