import requests
import json
import pandas as pd

import helpers

df = helpers.get_data()
print(df['symbol'][0])
print(helpers.specific_stock_data(df['symbol'][0]))




