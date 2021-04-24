from sqlalchemy import create_engine
from app.pricefind import pricefind
import pymysql
import pandas as pd

def sqlupload(symbol,sdate,edate):
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='@Ja10192',
                                db='stock_prices')

    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                        .format(user="root",
                                pw="@Ja10192",
                                db="stock_prices"))

    cursor = connection.cursor()
    #cursor.execute("Select * from stock_prices.security")
    #myresult = cursor.fetchall()

    sql = "INSERT INTO `security` (`Ticker`) VALUES (%s)"

    df1 = pd.read_sql('''select * from stock_prices.security''',engine)
    if not df1['ticker'].str.contains(symbol).any():
        cursor.execute(sql, (symbol))
        connection.commit()

    df2 = pd.read_sql('''select * from stock_prices.daily_price''',engine)

    df3 = pricefind(symbol,sdate,edate)
    df3.insert(0,"price_id",symbol + df3['strdate'])
    df3.insert(1,"ticker",symbol)
    df3.drop('strdate',axis=1,inplace=True)

    df3 = df3.merge(df2, on=['price_id'], how= 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
    df3.drop(columns=['ticker_y','price_date_y','Open_y','High_y','Low_y','Close_y','Volume_y','_merge'],axis=1,inplace=True)
    df3.rename(columns={'ticker_x':'ticker','price_date_x':'price_date','Open_x':'Open','High_x':'High','Low_x':'Low','Close_x':'Close','Volume_x':'Volume'}, inplace=True)

    if not df3.empty:
        df3.to_sql('daily_price', con = engine, if_exists = 'append', chunksize = 1000, index=False)

    connection.close()

    df1 = pd.read_sql(f'''select * from stock_prices.daily_price where ticker="{symbol}" and price_date>="{sdate}" and price_date<="{edate}"''',engine)
    df1.drop(columns=['price_id','ticker'],axis=1,inplace=True)
    df1.rename(columns={'price_date':'Date'}, inplace=True)
    df1 = df1.to_dict('records')
    return df1