
from sklearn.ensemble import RandomForestRegressor

import os
import sys
import pandas as pd
import numpy as np
from datetime import timedelta


path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))
data_path = str(parent_path) + "/random_forest/data_processing"
sys.path.append(data_path)
from data_modeling import scale_back_data

def random_forest_model(df):
    # Labels are the values we want to predict
    labels = np.array(df['var1(t)'])
    # Remove the labels from the features
    # axis 1 refers to the columns
    features= df.drop('var1(t)', axis = 1)
    # Saving feature names for later use
    feature_list = list(features.columns)
    # Convert to numpy array
    features = np.array(features)
    # Instantiate model with 1000 decision trees
    rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
    # Train the model on training data
    rf.fit(features, labels)
    return rf

def labels_pred(last_row):
    features_list = []
    columns = len(last_row)
    for c in range(columns):
        if c != 0:
            sales = last_row[c]
            features_list.append(sales)
    return features_list  

def random_forest_forecast(df_reg, forecast_days, scaler):
    print("Training model")
    rf_model = random_forest_model(df_reg)
    df_forecast = df_reg.copy()
    columns = len(df_reg.columns)
    last_row = list(df_reg.values[-1].tolist())
    print('Making predictions')
    for d in range(forecast_days):
        features = labels_pred(last_row)
        features = np.array(features).reshape((1, columns-1))
        prediction = rf_model.predict(features)
        del last_row[0] 
        last_row.append(prediction[0])
        forecast_date = df_forecast.index.max() + timedelta(days=1)
        df_forecast.loc[forecast_date] = last_row 
    df_pred = scale_back_data(df_forecast, scaler)
    print(df_pred)
    df_pred = df_pred[df_pred.columns[-1]]
    return df_pred

