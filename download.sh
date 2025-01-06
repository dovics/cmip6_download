models=(
    # "ACCESS-CM2"
    # "ACCESS-ESM1-5"
    # "BCC-CSM2-MR"
    # "CanESM5"
    # "EC-Earth3"
    # "FGOALS-g3"
    # "INM-CM4-8"
    # "INM-CM5-0"
    # "IPSL-CM6A-LR"
    # "KACE-1-0-G"
    "MIROC6"
    "MIROC-ES2L"
    # "MPI-ESM1-2-HR"
    # "MRI-ESM2-0"
    # "NorESM2-MM"
    # "UKESM1-0-LL"
)

mode=("historical" "ssp126" "ssp245" "ssp370" "ssp585")

for model in "${models[@]}"; do
    for m in "${mode[@]}"; do
        echo "Downloading ${model} ${m}"
        cd "data/$model"
        bash wget_script_$mode.sh
        cd ../..
    done
done
