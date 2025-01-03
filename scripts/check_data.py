import pandas as pd
import sqlite3
import os

conn = sqlite3.connect("data/stock_data.db")
cursor = conn.cursor()

stocks = pd.read_sql_query("SELECT * FROM stocks LIMIT 30", conn)
daily_data = pd.read_sql_query("SELECT * FROM daily_data LIMIT 30", conn)
cursor.execute("SELECT COUNT(*) FROM stocks")
row_count_stocks = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(DISTINCT ticker) FROM daily_data")
ticker_count_daily = cursor.fetchone()[0]

# get daily data of ABBV where year is greater than 2015
abbv_data = pd.read_sql_query("SELECT * FROM daily_data WHERE ticker='ABBV' AND date >= '2015-01-01'", conn)
print(abbv_data.head())

conn.close()

print(stocks.head())
print(daily_data.head())

size_bytes = os.path.getsize("data/stock_data.db")
size_mb = size_bytes / (1024 * 1024)
print(f"\nDatabase size: {size_mb:.2f} MB")
print(f"Number of rows in the stocks table: {row_count_stocks}")
print(f"Number of stocks in the daily_data table: {ticker_count_daily}")