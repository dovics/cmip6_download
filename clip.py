from pathlib import Path
import xarray as xr

use_cache = True
cmip6_data_dir = "data"
cmip6_model_list = [
    "ACCESS-CM2",
    "ACCESS-ESM1-5",
    "BCC-CSM2-MR",
    "CanESM5",
    "EC-Earth3",
    "FGOALS-g3",
    "INM-CM4-8",
    "INM-CM5-0",
    "IPSL-CM6A-LR",
    "KACE-1-0-G",
    "MIROC6",
    "MIROC-ES2L",
    "MPI-ESM1-2-HR",
    "MRI-ESM2-0",
    "NorESM2-MM",
    "UKESM1-0-LL",
]

def range_cmip6_origin_data(process_func):
    for model in cmip6_model_list:
        for file in Path(cmip6_data_dir).joinpath(model).rglob(f'*.nc'):
            if file.name.endswith(".clipped.nc"):
                continue
            print(f"{file} start processing")
            if file.is_file():
                process_func(file)


def clip_nc_file(path: Path):
    key = path.name.split("_")[0]
    target = path.with_suffix(".clipped.nc")
    if use_cache and target.exists():
        print(f"Using cached data {target}")
        return target

    ds = xr.load_dataset(path)
    # 选择 lat 和 lon 范围内的数据
    clipped_da = ds[key].sel(lat=slice(30, 55), lon=slice(70, 100))
    clipped_da.to_netcdf(target)
    return target



range_cmip6_origin_data(clip_nc_file)
