#!/bin/bash

JUST_ZERO=1
models=(
    "ACCESS-CM2"
    "ACCESS-ESM1-5"
    "BCC-CSM2-MR"
    "CanESM5"
    "EC-Earth3"
    "FGOALS-g3"
    "INM-CM4-8"
    "INM-CM5-0"
    "IPSL-CM6A-LR"
    "KACE-1-0-G"
    "MIROC6"
    "MIROC-ES2L"
    "MPI-ESM1-2-HR"
    "MRI-ESM2-0"
    "NorESM2-MM"
    "UKESM1-0-LL"
)


for model in "${models[@]}"; do
        echo "Clean ${model}"
        cd "data/$model"
        list=$(ls -al | grep -v clipped | grep nc)

        if [ $JUST_ZERO -eq 1 ] ; then
            file_list=$(printf "%s\n" "$list" | awk '$5 == 0 {print $NF}')
        else 
            file_list=$(printf "%s\n" "$list" | awk '{print $NF}')
        fi

        printf "%s\n" "$file_list" | xargs -I{} rm {}
        cd -
done
