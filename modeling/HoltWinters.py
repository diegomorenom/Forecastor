from statsmodels.tsa.holtwinters import ExponentialSmoothing

import os
import sys
import pandas as pd

import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.simplefilter('ignore', ConvergenceWarning)

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))
forecast_path = str(parent_path) + "/forecastor/forecast_generator"
sys.path.append(forecast_path)

    
class HoltWinters:
    def __init__(self, data, models, parameters, forecast_days, time_series_model):
        self.data = data 
        self.forecast_days = forecast_days 
        self.time_series_model = time_series_model
        #self.seasonal = parameters.get("holt_winters_parameter_1", None)
        #self.seasonal_periods = parameters.get("holt_winters_parameter_2", None)
        
    def fit_model(self, df_ts):
        # Implement logic to fit time series model
        # create class
        model = ExponentialSmoothing(self.data, seasonal="add", seasonal_periods=7)
        # fit model
        fitted_model = model.fit()
        return fitted_model

    def predict(self, fitted_model):
        # Implement logic to predict using time series model
        # make prediction
        yhat = fitted_model.forecast(self.forecast_days)
        return yhat