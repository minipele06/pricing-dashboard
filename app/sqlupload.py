import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
from pricefind import pricefind

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

connection = create_db_connection("localhost", "root", "@Ja10192", "stock_prices")

df = pricefind('AAPL','12/31/2020','04/05/2021')
df.to_sql('daily_price', con = connection, if_exists = 'append', chunksize = 1000)
