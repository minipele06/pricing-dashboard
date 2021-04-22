import os
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt


API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

def pricefind(symbol,sdate,edate):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}&datatype=csv"
    df = pd.read_csv(url)
    df.rename(columns={'timestamp':'price_date','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'}, inplace=True)
    df['price_date'] = pd.to_datetime(df['price_date']).dt.normalize()
    new_df = df[(df['price_date'] >= sdate) & (df['price_date'] <= edate)]
    # x = df['Date']
    # y = df['Close']
    # fig = plt.figure(figsize=(16, 12))
    # plt.plot(df['Date'],df['Close'])
    # plt.xlabel('Date',fontsize=10)
    # plt.savefig("my_chart_name.png")
    new_df = new_df.to_dict('records')
    return new_df