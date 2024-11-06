import pandas as pd
import sqlite3

conn = sqlite3.connect("data/stock_data.db")

stocks = pd.read_sql_query("SELECT * FROM stocks LIMIT 3", conn)
daily_data = pd.read_sql_query("SELECT * FROM daily_data LIMIT 10", conn)

conn.close()

print(stocks.head())
print(daily_data.head())