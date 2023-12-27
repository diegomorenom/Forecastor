import os
import sys
#import pprint

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))
data_path = str(parent_path) + "/Forecastor/data_processing"

sys.path.append(data_path)


from data_handler import get_data, get_stores, get_families, get_time_series

df = get_data()
print(df.head())

stores = get_stores(df)
families = get_families(df)

for s in stores:
    for f in families:
        ts = get_time_series(df, f, s)
        print(s,f, len(ts))

