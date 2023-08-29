import requests
import json
import pandas as pd
import datetime

def get_data():
    url = 'https://stockanalysis.com/api/screener/s/f?m=marketCap&s=desc&c=no,s,n,marketCap,price,change,revenue,volume,industry,sector,revenueGrowth,netIncome,fcf,netCash&cn=0&f=exchange-is-NASDAQ&p=2&dd=true&i=allstocks'
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        stock_data = json.loads(response.text)
        # Extract data
        nested_data = stock_data['data']['data']
        # Making dataframe with all stock data
        df = pd.DataFrame(nested_data)
        df = df.rename(columns={'s': 'symbol', 'n': 'company name',
                                'fcf': 'free_cash_flow', 'netCash': 'net_cash_debt'})
        df.drop('no', axis=1, inplace=True)
        return df


def specific_stock_data(symbol):
    url = f'https://stockanalysis.com/api/charts/s/{symbol}/MAX/l/week'
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        stock_data = json.loads(response.text)
        # Extract data
        nested_data = stock_data['data']
        # Making dataframe with all stock data
        df = pd.DataFrame(nested_data)
        df = df.rename(columns={'t': 'date', 'c': 'close'})
        df['date'] = df['date'].apply(lambda x: datetime.datetime.fromtimestamp(x))
        df['date'] = df['date'].dt.date
        df.drop('o', axis=1, inplace=True)
        return df





