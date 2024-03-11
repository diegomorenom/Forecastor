from abc import ABC, abstractmethod

import itertools
import os
import sys
from tqdm import tqdm
from time import sleep

import importlib

import warnings
warnings.filterwarnings('ignore')
#import pprint

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))
data_path = str(parent_path) + "/forecastor/data_processing"
modeling_path = str(parent_path) + "/forecastor/modeling"

sys.path.append(data_path)
sys.path.append(modeling_path)


from data_handler import get_time_series, get_splitted_df, fill_values, structure_predictions, save_predictions
from data_modeling import model_data


class BaseForecastingProcess(ABC):
    def __init__(self, data, models, parameters, forecast_days):
        self.data = data
        self.models = models
        self.parameters = parameters
        self.forecast_days = forecast_days

    @abstractmethod
    def process_data(self):
        pass

    @abstractmethod
    def run_all_models(self):
        pass

    @abstractmethod
    def save_forecast(self, df_pred):
        pass

class ForecastingProcess(BaseForecastingProcess):
    def __init__(self, data, models, parameters, forecast_days):
        super().__init__(data, models, parameters, forecast_days)
        self.data = data
        self.models = models
        self.parameters = parameters
        self.forecast_days = forecast_days
    
    def process_data(self):
        df_info = get_splitted_df(self.data)
        df_ts = get_time_series(df_info)
        df_ts = fill_values(df_ts)
        return df_ts

    def run_all_models(self):
        df_ts = self.process_data()
        for model in self.models:
            model_parameters = self.parameters[model]
            module = importlib.import_module(model)
            model_class = getattr(module, model)
            model_type = model_parameters['model_type']
            if model_type == 'TimeSeries':
                model_instance = model_class(df_ts, model_parameters, self.forecast_days)
            elif model_type == 'Regression':
                df_reg, scaler = model_data(df_ts)
                model_instance = model_class(df_reg, scaler, model_parameters, self.forecast_days)
            
            fitted_model = model_instance.fit_model()
            df_yhat = model_instance.predict(fitted_model)
            
            self.save_forecast(df_yhat, model_parameters['model_name'])

    def save_forecast(self, df_pred, model):
        df_pred = structure_predictions(self.data['date'].max(), df_pred, model)
        save_predictions(self.data['date'].max(), df_pred, model)

