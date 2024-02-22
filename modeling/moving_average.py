from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import timedelta

import os
import sys
import pandas as pd

import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.simplefilter('ignore', ConvergenceWarning)

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))
data_path = str(parent_path) + "/moving_average/data_processing"
sys.path.append(data_path)

# simple moving average
def moving_average_model(data, forecast_days):
    y_hat_sma = data.copy()
    y_hat_sma['forecast'] = data['sales'].rolling(forecast_days).mean()
    return y_hat_sma

def moving_average_forecast(df_ts, forecast_days):
    data_df = df_ts.copy()
    for d in range(forecast_days):
        df_yhat =  moving_average_model(data_df, forecast_days)
        last_sale = df_yhat['forecast'].iloc[-1]
        df_forecast = df_yhat.reset_index()
        forecast_date = df_forecast.date.max() + timedelta(days=1)
        df_forecast = df_forecast[['date','sales']]
        df_forecast = df_forecast._append(pd.DataFrame({"date":[forecast_date],"sales":[last_sale]}),ignore_index=True)
        df_forecast = df_forecast.set_index('date')
        data_df = df_forecast.copy()

    return df_forecast


