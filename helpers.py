import requests
import json
import pandas as pd
import datetime


# Getting latest stock data
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


# Get history of all stocks from as early as possible (Max 1970)
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
        df_data = pd.DataFrame(nested_data)
        df_data = df_data.rename(columns={'t': 'date', 'c': 'close'})
        # df_data['date'] = df_data['date'].apply(lambda x: datetime.datetime.fromtimestamp(x))
        # df_data['date'] = df_data['date'].dt.date
        df_data.drop('o', axis=1, inplace=True)
        return df_data


# Make csv of all stocks closing
def make_csv():
    df = get_data()

    symbol = df['symbol'][0]
    df_data = specific_stock_data(symbol)
    df_data.set_index('date', inplace=True)
    df_data.rename(columns={'close': f'{symbol}'}, inplace=True)

    for i in range(1, len(df)):
        symbol = df['symbol'][i]
        new_stock = specific_stock_data(df['symbol'][i])
        new_stock.set_index('date', inplace=True)
        new_stock.rename(columns={'close': f'{symbol}'}, inplace=True)

        df_data = pd.merge(df_data, new_stock, how='outer', left_index=True, right_index=True)

    df_data.index = pd.to_datetime(df_data.index, unit='s')

    df_data.to_csv('stockdata.csv')


# Make lists of symbols (companies) according to sector affiliation
def sector_list():
    df = get_data()
    # Making empty dict to store lists of companies in the various sectors
    sector_dict = {}
    # List of sectors:
    sectors = df['sector'].unique().tolist()

    for sector in sectors:
        # Creating an empty list for each name and storing it in the dictionary
        sector_dict[sector] = []

    for i in range(0, len(df)):
        for sector in sectors:
            if df['sector'][i] == sector:
                sector_dict[sector].append(df['symbol'][i])

    # for key in sector_dict.keys():
    #     print(key, sector_dict[key])

    return sector_dict


# Make lists of symbols (companies) according to industry affiliation
def industry_list():
    df = get_data()
    # Making empty dict to store lists of companies in the various industries
    industry_dict = {}
    # List of industries:
    industries = df['industry'].unique().tolist()

    for industry in industries:
        # Creating an empty list for each name and storing it in the dictionary
        industry_dict[industry] = []

    for i in range(0, len(df)):
        for industry in industries:
            if df['industry'][i] == industry:
                industry_dict[industry].append(df['symbol'][i])

    # for key in industry_dict.keys():
    #     print(key, industry_dict[key])

    return industry_dict


