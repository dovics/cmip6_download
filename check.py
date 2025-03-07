import os
import re
from datetime import datetime, timedelta
import csv

def check_data_completeness(data_dir):
    """
    Checks the completeness of climate model data files in a given directory.

    Args:
        data_dir (str): The path to the directory containing the data files.
    """

    required_vars = [
        # "hur",
        "hurs", 
        # "pr", 
        # "rsds", 
        # "sfcWind", 
        # "tas", 
        # "tasmin", 
        # "tasmax"
    ]
    
    required_models = [
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
    required_scenarios = ["historical", "ssp126", "ssp245", "ssp370", "ssp585"]
    
    output_data = {}

    file_pattern = re.compile(
        r"^(?P<variable>\w+)_day_(?P<model>[\w-]+)_(?P<scenario>\w+)_"
        r"(?P<batch>\w+)_(gn|gr|gr1)_(?P<start_time>\d{8})-(?P<end_time>\d{8})\.clipped\.nc$"
    )

    grouped_files = {}

    for root, _, files in os.walk(data_dir):
        for file in files:
            match = file_pattern.match(file)
            if match:
                file_info = match.groupdict()
                if (
                    file_info["variable"] in required_vars
                    and file_info["model"] in required_models
                    and file_info["scenario"] in required_scenarios
                ):
                    key = (
                        file_info["variable"],
                        file_info["model"],
                        file_info["scenario"],
                        file_info["batch"],
                    )
                    if key not in grouped_files:
                        grouped_files[key] = []
                    grouped_files[key].append(file_info)

    for (variable, model, scenario, batch), files in grouped_files.items():
        key = (model, f"{variable}_{scenario}")
        if model not in output_data:
            output_data[model] = {}
        
        start_dates = [datetime.strptime(f["start_time"], "%Y%m%d") for f in files]
        end_dates = [datetime.strptime(f["end_time"], "%Y%m%d") for f in files]
        
        start_dates.sort()
        end_dates.sort()

        if scenario == "historical":
            expected_start = datetime(1960, 1, 1)
            expected_end = datetime(2014, 12, 30)
        else:
            expected_start = datetime(2015, 1, 1)
            expected_end = datetime(2100, 12, 30)
        
        missing_data = []
        if start_dates[0] > expected_start or end_dates[-1] < expected_end:
            missing_data.append(f"Expected range {expected_start.strftime('%Y%m%d')}-{expected_end.strftime('%Y%m%d')}, found {start_dates[0].strftime('%Y%m%d')}-{end_dates[-1].strftime('%Y%m%d')}")
        
        for i in range(len(start_dates) - 1):
            if (end_dates[i] + timedelta(days=1)) != start_dates[i+1] and (end_dates[i] + timedelta(days=2)) != start_dates[i+1]:
                missing_data.append(f"Gap in data: {end_dates[i].strftime('%Y%m%d')}-{start_dates[i+1].strftime('%Y%m%d')}")
        
        if missing_data:
            output_data[model][f"{variable}_{scenario}"] = "; ".join(missing_data)
        else:
            output_data[model][f"{variable}_{scenario}"] = ""

    with open("output.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        
        header = ["model"]
        for var in required_vars:
            for scenario in required_scenarios:
                header.append(f"{var}_{scenario}")
        writer.writerow(header)

        for model, data in output_data.items():
            row = [model]
            for var in required_vars:
                for scenario in required_scenarios:
                    row.append(data.get(f"{var}_{scenario}", ""))
            writer.writerow(row)

if __name__ == "__main__":
    data_directory = "data"
    check_data_completeness(data_directory)
