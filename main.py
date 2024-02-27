from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List, Dict
import yaml
from forecast_generator import forecast_process as fp

import json
import os
import sys

import pandas as pd

import warnings
warnings.filterwarnings('ignore')

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))
data_path = str(parent_path) + "/forecastor/data_processing"
forecast_path = str(parent_path) + "/forecastor/forecast_generator"

sys.path.append(data_path)
sys.path.append(forecast_path)


app = FastAPI()

def read_csv(file: UploadFile) -> pd.DataFrame:
    """
    Read CSV file and return DataFrame
    """
    df = pd.read_csv(file.file)
    return df

def parse_yaml(yaml_data):
    try:
        parsed_data = yaml.safe_load(yaml_data)
        return parsed_data
    except yaml.YAMLError as e:
        return {"error": "Invalid YAML format", "detail": str(e)}

@app.post("/run_forecasting/")
async def run_forecasting(
    json_file: UploadFile = File(...), 
    csv_file: UploadFile = File(...)):
    # Read JSON file
    json_data = await json_file.read()
    parsed_json = json.loads(json_data)
    
    # Read CSV file
    data = pd.read_csv(csv_file.file)
    
    # Process data here using parsed_json and df
    models = ['HoltWinters']#parsed_json[0]["Models"]
    forecast_days = parsed_json[0]["ForecastDays"]
    parameters = parsed_json[1]

    # Instantiate ForecastingProcess class
    forecast_process_instance = fp.ForecastingProcess(data, models, parameters, forecast_days)

    # Call run_all_models method
    forecast_process_instance.run_all_models()

    return {"message": "Forecasting process completed successfully."}
    