#!/bin/bash

set -e

MAX_CONCURRENT=5
current_jobs=0
models=(
    # "ACCESS-CM2"
    # "ACCESS-ESM1-5"
    # "BCC-CSM2-MR"
    # "CanESM5"
    "EC-Earth3"
    "FGOALS-g3" # historical
    "INM-CM4-8"
    "INM-CM5-0"
    "IPSL-CM6A-LR"
    "KACE-1-0-G"
    "MIROC6"
    "MIROC-ES2L"
    "MPI-ESM1-2-HR" # ssp126
    "MRI-ESM2-0" # historical
    "NorESM2-MM"
    "UKESM1-0-LL"
)

mode=("historical" "ssp126" "ssp245" "ssp370" "ssp585")

for model in "${models[@]}"; do
    # for m in "${mode[@]}"; do
        echo "Downloading ${model} ${m}"
        cd "data/$model"
        bash wget_script_historical_hurs_02.sh
        
        bash wget_script_ssp_hurs.sh

        cd ../..

       
    # done
done