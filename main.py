from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict
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
store_path = str(parent_path) + "/forecastor/data_processing/data_base"
forecast_files = str(parent_path) + "/forecastor/data_processing/forecast_files"

sys.path.append(data_path)
sys.path.append(forecast_path)

from data_handler import get_data

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost",
    "http://localhost:5174/",  # Add your React frontend URL here
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5174"],  # Update this with your React frontend URL
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"],
# )


#Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Metadata(BaseModel):
    prediction_column: str
    date_column: str


@app.post("/save_file/")
async def save_file(
    metadata_str: str = Form(...),
    csv_file: UploadFile = File(...)):
    
    metadata_dict = eval(metadata_str)
    
    # Read CSV file
    data = pd.read_csv(csv_file.file)
    
    data_columns = [metadata_dict['date_column'], metadata_dict['prediction_column']]
    data = data[data_columns]
    data.columns = ['date_column', 'prediction_column']
    
    # Save the CSV file
    data.to_csv(store_path+'/data_api.csv')

    return {"message": f"Data saved successfully. Columns {data.columns}, Metadata: {metadata_dict}"}



class ForecastRequest(BaseModel):
    forecastDays: int = Field(..., description="Number of forecast days")
    selectedModels: List[str] = Field(..., description="List of selected models")

@app.post("/process_forecast")
async def process_forecast(request_data: ForecastRequest):
    forecast_days = request_data.forecastDays
    selected_models = request_data.selectedModels
    print(f"Received forecast days: {forecast_days}")
    print(f"Received selected models: {selected_models}")
    with open('forecast_info.JSON', 'w', encoding='utf-8') as f:
        json.dump(request_data.__dict__, f, ensure_ascii=False, indent=4)

    # Read CSV file
    data = get_data()

    parameters_json = open('parameters.json')
    parameters = json.load(parameters_json)

    # Instantiate ForecastingProcess class
    forecast_process_instance = fp.ForecastingProcess(data, selected_models, parameters[1], forecast_days)

    # Call run_all_models method
    forecast_process_instance.run_all_models()

    return {"message": "Forecasting process completed successfully."}

@app.get("/forecast/{filename}")
async def get_forecast_file(filename: str):
    # Construct the full path to the forecast file
    file_path = os.path.join(forecast_files, filename)
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Serve the file using FileResponse
        return FileResponse(file_path)
    else:
        # Return a 404 Not Found response if the file does not exist
        return {"error": "File not found"}
    
@app.get("/data_base/{filename}")
async def get_data_file(filename: str):
    # Construct the full path to the forecast file
    file_path = os.path.join(store_path, filename)
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Serve the file using FileResponse
        return FileResponse(file_path)
    else:
        # Return a 404 Not Found response if the file does not exist
        return {"error": "File not found"}