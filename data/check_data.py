import pandas as pd
import sqlite3
import os

conn = sqlite3.connect("data/stock_data.db")
cursor = conn.cursor()

stocks = pd.read_sql_query("SELECT * FROM stocks LIMIT 30", conn)
daily_data = pd.read_sql_query("SELECT * FROM daily_data LIMIT 30", conn)
cursor.execute("SELECT COUNT(*) FROM daily_data")
row_count = cursor.fetchone()[0]

conn.close()

print(stocks.head())
print(daily_data.head())

size_bytes = os.path.getsize("data/stock_data.db")
size_mb = size_bytes / (1024 * 1024)
print(f"\nDatabase size: {size_mb:.2f} MB")
print(f"Number of rows in the daily_data table: {row_count}")