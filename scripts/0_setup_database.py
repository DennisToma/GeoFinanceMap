import sqlite3

conn = sqlite3.connect("data/stock_data.db")
cursor = conn.cursor()

# 'stocks' table for general stock information
# 'Ticker', 'Name', 'Sector', 'Industry', 'Country', 'Zip Code', 'State', 'City', 'Address
cursor.execute("""
CREATE TABLE IF NOT EXISTS stocks (
    ticker TEXT PRIMARY KEY,
    name TEXT,
    sector TEXT,
    industry TEXT,
    country TEXT,
    zip_code TEXT,
    state TEXT,
    city TEXT,
    address TEXT
)
""")



# 'daily_data' table for storing daily trading data
cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_data (
    ticker TEXT,
    date DATE,
    open REAL,
    close REAL,
    low REAL,
    high REAL,
    volume INTEGER,
    PRIMARY KEY (ticker, date),
    FOREIGN KEY (ticker) REFERENCES stocks(ticker)
)
""")

conn.commit()
conn.close()
