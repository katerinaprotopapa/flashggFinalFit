import argparse
import os
import json
import re
import glob

import pyarrow.parquet as pq

from commonTools import *
from commonObjects import *
from utils import *

parser = argparse.ArgumentParser()
#parser.add_argument("-i", "--input-file", required=True, type=str, help='Path to input file')
parser.add_argument("-i", "--input-dir", required=True, type=str, help='Path to input directory')
parser.add_argument("-c", "--config", required=True, type=str, help='Config file')
parser.add_argument("--category", required=False, default='pred_C1_reco', type=str, help='Config file') # for STXS this is 'category'
args = parser.parse_args()

# Load config
with open(args.config, "r") as jf:
    config = json.load(jf)

# Extract files and loop over
list_of_files = glob.glob(f"{args.input_dir}/events*.parquet")
for i, input_file in enumerate(list_of_files):

    print("\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    input_file_base = input_file.split("/")[-1]
    print(f" * Processing: {input_file_base} [{i+1}/{len(list_of_files)}]")

    # Load parquet file
    f = pq.ParquetFile(input_file).read()
    df = f.to_pandas()

    # renaming categories 
    if 'categories' in config:
        df[args.category] = df[args.category].map(str).map(config['categories'])
    # renaming 'mass' column to 'CMS_hgg_mass'
    if 'mass' in df.columns:
        df = df.rename(columns={'mass': 'CMS_hgg_mass'})

    # Extract process for file name
    proc = input_file.split("__")[-1].strip(".parquet")
    # skip specific procs e.g MC background
    if proc in config.get('procs_to_drop', []):
        continue

    # Extract categories
    cats = list(df[args.category].unique())
    if 'cats_to_drop' in config:
        cats = [cat for cat in cats if cat not in config['cats_to_drop']]

    # Define output_file
    output_file = re.sub(".parquet", ".root", input_file)
    f_out = ROOT.TFile(output_file, "RECREATE")
    f_out_dir = f_out.mkdir(inputWSName__.split("/")[0])
    f_out_dir.cd()
    # Build workspace
    ws = ROOT.RooWorkspace(inputWSName__.split("/")[1],inputWSName__.split("/")[1])

    # Add variables to workspace
    list_of_vars = add_vars_to_workspace(ws, config['main_vars'])

    # Loop over categories
    for cat in cats:

        # Mask events in cat
        mask = (df[args.category] == cat)

        # Make RooArgSet
        aset = make_argset(ws, config['main_vars'])

        # Build RooDataSet
        d_name = f"{proc}__125__{sqrts__}__{cat}"
        d = ROOT.RooDataSet.from_pandas(df[mask], aset, weight_name="weight", name=d_name, title=d_name)

        # Add to workspace
        getattr(ws, 'import')(d)

    # Write ws to file
    ws.Write()

    # Close file and delete workspace from heap
    f_out.Close()


