from sqlalchemy import create_engine
from pricefind import pricefind
import pymysql
import pandas as pd

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='@Ja10192',
                             db='stock_prices')

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="@Ja10192",
                               db="stock_prices"))

cursor = connection.cursor()
cursor.execute("Select * from stock_prices.security")
myresult = cursor.fetchall()

sql = "INSERT INTO `security` (`Ticker`, `Name`) VALUES (%s, %s)"

df1 = pd.read_sql('''select * from stock_prices.security''',engine)
if not df1['ticker'].str.contains('AAPL').any():
    cursor.execute(sql, ("AAPL","Apple"))
    connection.commit()

df = pricefind('AAPL','12/31/2020','04/05/2021')
df.insert(0,"ticker","AAPL")
df.to_sql('daily_price', con = engine, if_exists = 'append', chunksize = 1000, index=False)

connection.close()