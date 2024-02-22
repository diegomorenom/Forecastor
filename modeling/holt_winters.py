from statsmodels.tsa.holtwinters import ExponentialSmoothing

import os
import sys
import pandas as pd

import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.simplefilter('ignore', ConvergenceWarning)

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))
data_path = str(parent_path) + "/holt_winters/data_processing"
sys.path.append(data_path)


from data_handler import get_data, get_stores, get_families, get_time_series

# holt winters
def holt_winters_forecast(data, forecast_days):
    # create class
    model = ExponentialSmoothing(data,seasonal="add", seasonal_periods=7)
    # fit model
    model_fit = model.fit()
    # make prediction
    yhat = model_fit.forecast(forecast_days)
    return yhat

