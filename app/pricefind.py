import os
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import requests
import re

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

def pricefind(symbol,sdate,edate):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}&datatype=csv"
    df = pd.read_csv(url)
    df.rename(columns={'timestamp':'price_date','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'}, inplace=True)
    df['price_date'] = pd.to_datetime(df['price_date']).dt.normalize()
    df['strdate'] = df['price_date'].dt.strftime('%Y-%m-%d')
    new_df = df[(df['price_date'] >= sdate) & (df['price_date'] <= edate)]
    return new_df

def stockinfo(symbol):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"
    r = requests.get(url)
    stuff = r.json()
    name = stuff['Name']
    sector = stuff['Sector']
    ind = stuff['Industry']
    return name,sector,ind

def tickercheck(inputString):
    return bool(re.search(r'^[A-Za-z]{1,5}$', inputString))