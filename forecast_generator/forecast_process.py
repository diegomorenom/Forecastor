from abc import ABC, abstractmethod

import itertools
import os
import sys
from tqdm import tqdm
from time import sleep

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
from holt_winters import HoltWinters

store_id = 1
family_name = 'GROCERY I'

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
        # Filter time series and regression models
        self.time_series_models = [model for model in models if issubclass(model, TimeSeriesModel)]
        self.regression_models = [model for model in models if issubclass(model, RegressionModel)]
    
    def process_data(self):
        df_info = get_splitted_df(self.data, family_name,store_id)
        df_ts = get_time_series(df_info)
        df_ts = fill_values(df_ts)
        return df_ts

    def run_all_models(self):
        df_ts = self.process_data()
        for model_class in self.models:
            model_parameters = self.parameters[model_class]
            model_instance = model_class(df_ts, self.models, model_parameters, self.forecast_days, TimeSeriesModel)
            if isinstance(model_instance, TimeSeriesModel):
                df_ts = model_instance.prepare_data_ts()
            elif isinstance(model_instance, RegressionModel):
                df_ts = model_instance.prepare_data_reg()
            fitted_model = model_instance.fit_model(model_instance, df_ts)
            df_yhat = model_instance.predict(fitted_model)
            self.save_forecast(df_yhat)

    def save_forecast(self, df_pred):
        df_pred = structure_predictions(self.data['date'].max(), df_pred, f, s)
        save_predictions(self.data['date'].max(), df_pred)

class TimeSeriesModel(ForecastingProcess):
    def __init__(self, data, models, parameters, forecast_days):
        super().__init__(data, models, parameters, forecast_days)

    def prepare_data(self):
        # Implement logic to prepare time series data
        pass

    

class RegressionModel(ForecastingProcess):
    def __init__(self, data, models, parameters, forecast_days):
        super().__init__(data, models, parameters, forecast_days)

    def prepare_data(self):
        # Implement logic to prepare data for regression model
        pass
