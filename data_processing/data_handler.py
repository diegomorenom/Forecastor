import pandas as pd

import os
import sys

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))
data_base_path = str(parent_path)+"/Forecastor/data_processing/data_base"


def get_data():
    data = pd.read_csv(data_base_path+"/train.csv")  
    return data

def get_time_series(data, family, store_nbr):
    df_time_serie = data[(data['family']==family)&(data['store_nbr']==store_nbr)]
    df_time_serie = df_time_serie[['date', 'sales']]
    return df_time_serie

def get_stores(data):
    stores = list(data['store_nbr'].unique())
    return stores

def get_families(data):
    families = list(data['family'].unique())
    return families

def train_test_split(data, n_test):
 return data[:-n_test], data[-n_test:]