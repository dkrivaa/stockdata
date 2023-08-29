import requests
import json
import pandas as pd

url = 'https://stockanalysis.com/api/screener/s/f?m=marketCap&s=desc&c=no,s,n,marketCap,price,change,revenue,volume,industry,sector,revenueGrowth,netIncome,fcf,netCash&cn=0&f=exchange-is-NASDAQ&p=2&dd=true&i=allstocks'






url = 'https://stockanalysis.com/api/charts/s/aa/MAX/l/week'
response = requests.get(url)
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data
    stock_data = json.loads(response.text)
    nested_data = stock_data['data']
    print(nested_data)
    df = pd.DataFrame(nested_data)
    print(df.shape)






