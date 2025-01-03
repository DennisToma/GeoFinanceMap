import yfinance as yf
import pandas as pd
import sqlite3
import time

with open('data/working_tickers.txt', 'r') as file:
    tickers = file.readlines()
    tickers = [ticker.strip() for ticker in tickers]
    #tickers = tickers[:300]  # Limiting to 10 tickers for testing
start = '2000-01-01'
end = '2024-01-01'
db_path = 'data/stock_data.db'
print(f"Total number of collecting tickers: {len(tickers)}")

def get_stock_info(tickers, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for ticker in tickers:
        print(f"Processing {ticker}...  ({tickers.index(ticker)+1}/{len(tickers)})")
        data = yf.Ticker(ticker)
        try:
            row = (
                ticker,
                data.info.get('longName', 'N/A'),
                data.info.get('sector', 'N/A'),
                data.info.get('industry', 'N/A'),
                data.info.get('country', 'N/A'),
                data.info.get('zip', 'N/A'),
                data.info.get('state', 'N/A'),
                data.info.get('city', 'N/A'),
                data.info.get('address1', 'N/A') 
            )
            
            # Insert data into the stocks table
            cursor.execute("""
                INSERT OR IGNORE INTO stocks (
                    ticker, name, sector, industry, country, zip_code, state, city, address
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, row)

        except KeyError as e:
            print(f"Data for {ticker} is missing key information: {e}")
        except Exception as e:
            print(f"An error occurred with ticker {ticker}: {e}")           
        time.sleep(1)

    conn.commit()
    conn.close()


def get_historic_data(tickers, start, end, db_path):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM daily_data")
    
    historic_data = yf.download(tickers, start=start, end=end, progress=False, group_by='ticker')
    
    for ticker in tickers:
        print(f"Processing {ticker}...  ({tickers.index(ticker)+1}/{len(tickers)})")
        ticker_data = historic_data[ticker].reset_index()
        
        ticker_data = ticker_data.drop(columns=['Close'])
        ticker_data['ticker'] = ticker
        
        ticker_data = ticker_data.rename(columns={
            'Date': 'date',
            'Open': 'open',
            'Adj Close': 'close',
            'Low': 'low',
            'High': 'high',
            'Volume': 'volume'
        })

        ticker_data[['ticker', 'date', 'open', 'close', 'low', 'high', 'volume']].to_sql(
            'daily_data', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()
    
    
get_stock_info(tickers, db_path)
get_historic_data(tickers, start, end, db_path)