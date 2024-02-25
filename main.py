from forecast_generator import forecast_process as fp

import os
import sys
import itertools
from tqdm import tqdm
from time import sleep

import warnings
warnings.filterwarnings('ignore')
#import pprint

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))
data_path = str(parent_path) + "/neural_network/data_processing"
model_path = str(parent_path) + "/neural_network/modeling"

sys.path.append(data_path)
sys.path.append(model_path)


from data_handler import get_data, get_stores, get_families, get_time_series, get_splitted_df, fill_values, structure_predictions, save_predictions


# Prepare your data, models, parameters, and forecast_days
data = get_data()
models = ['HoltWinters']
parameters = {
                "seasonal": "add", 
                "seasonal_periods": 7
            }
forecast_days = 30

# Instantiate a class that inherits from BaseForecastingProcess
forecast_process_instance = fp.ForecastingProcess(data, models, parameters, forecast_days)

# Call the run_all_models method
forecast_process_instance.run_all_models()