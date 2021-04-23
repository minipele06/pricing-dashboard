import mysql.connector
from mysql.connector import Error
import pandas as pd
import os

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

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

create_security_table = """
CREATE TABLE security (
  ticker VARCHAR(10) PRIMARY KEY,
  name VARCHAR(100) NULL,
  sector VARCHAR(100) NULL,
  industry VARCHAR(100) NULL,
  created_date DATETIME NULL DEFAULT CURRENT_TIMESTAMP(),
  last_updated DATETIME NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()
  );
 """

create_price_table = """
CREATE TABLE daily_price (
  price_id INT PRIMARY KEY AUTO_INCREMENT,
  ticker VARCHAR(10),
  price_date DATE NOT NULL,
  Open DECIMAL(11,2) NULL DEFAULT NULL,
  High DECIMAL(11,2) NULL DEFAULT NULL,
  Low DECIMAL(11,2) NULL DEFAULT NULL,
  Close DECIMAL(11,2) NULL DEFAULT NULL,
  Volume BIGINT(20) NULL DEFAULT NULL
  );
 """

alter_price_table = """
ALTER TABLE daily_price
ADD FOREIGN KEY(ticker)
REFERENCES security(ticker)
ON DELETE SET NULL;
"""

connection = create_db_connection("localhost", "root", "@Ja10192", "stock_prices") # Connect to the Database
#execute_query(connection, create_security_table)
execute_query(connection, create_price_table)
execute_query(connection, alter_price_table)
