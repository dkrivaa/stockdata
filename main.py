import requests
import json
import pandas as pd
import datetime

import helpers

df = helpers.get_data()

symbol = df['symbol'][0]
df_data = helpers.specific_stock_data(symbol)
df_data.set_index('date', inplace=True)
df_data.rename(columns={'close': f'{symbol}'}, inplace=True)


for i in range(1, len(df)):
    symbol = df['symbol'][i]
    new_stock = helpers.specific_stock_data(df['symbol'][i])
    new_stock.set_index('date', inplace=True)
    new_stock.rename(columns={'close': f'{symbol}'}, inplace=True)

    df_data = pd.merge(df_data, new_stock, how='outer', left_index=True, right_index=True)

df_data.index = pd.to_datetime(df_data.index, unit='s')

df_data.to_csv('stockdata.csv')



