import os
import pandas as pd
import numpy as np
import datetime as dt

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

def pricefind(symbol,sdate,edate):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}&datatype=csv"
    df = pd.read_csv(url)
    df.rename(columns={'timestamp':'Date','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
    df = df[(df['Date'] >= sdate) & (df['Date'] <= edate)]
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%m/%d/%Y')
    new_df = df.to_dict('records')
    return new_df