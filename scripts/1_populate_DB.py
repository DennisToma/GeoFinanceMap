import yfinance as yf
import pandas as pd
import sqlite3
import time

def clear_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM stocks")
        cursor.execute("DELETE FROM daily_data")
        conn.commit()
        print("Database tables cleared.")
    except Exception as e:
        print(f"An error occurred while clearing tables: {e}")
    finally:
        conn.close()

def process_ticker(ticker, region, suffix_dict, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Attempt to download historical data for the ticker
    try:
        data = yf.download(ticker, start="2000-01-01", progress=False)

        if data.empty:
            ticker_with_suffix = ticker + "." + suffix_dict.get(region, "")
            print(f"Unsuccessful. Trying {ticker_with_suffix}")
            data = yf.download(ticker_with_suffix, start="2000-01-01", progress=False)
            if data.empty:
                print(f"Data not available for {ticker} or {ticker_with_suffix}. Skipping.")
                return
            ticker = ticker_with_suffix
        print(f"Data successfully retrieved for {ticker}. Adding to database.")

        # Add stock info to database
        stock_info = yf.Ticker(ticker)
        row = (
            ticker,
            stock_info.info.get('longName', 'N/A'),
            stock_info.info.get('sector', 'N/A'),
            stock_info.info.get('industry', 'N/A'),
            stock_info.info.get('country', 'N/A'),
            stock_info.info.get('zip', 'N/A'),
            stock_info.info.get('state', 'N/A'),
            stock_info.info.get('city', 'N/A'),
            stock_info.info.get('address1', 'N/A')
        )

        cursor.execute("""
            INSERT OR IGNORE INTO stocks (
                ticker, name, sector, industry, country, zip_code, state, city, address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)

        # Add historical data to the database
        data = data.reset_index()
        data['ticker'] = ticker

        data = data.rename(columns={
            'Date': 'date',
            'Open': 'open',
            'Close': 'close',
            'Low': 'low',
            'High': 'high',
            'Volume': 'volume'
        })

        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
        data[['ticker', 'date', 'open', 'close', 'low', 'high', 'volume']].to_sql(
            'daily_data', conn, if_exists='append', index=False)

        conn.commit()
        print(f"Data for {ticker} successfully added to the database.\n")

    except Exception as e:
        print(f"An error occurred with ticker {ticker}: {e}")

    finally:
        conn.close()

def main():
    excel_path = "data/FTSE_All-World.xlsx"
    db_path = "data/stock_data.db"

    # Clear database tables at the start
    clear_tables(db_path)

    # Load and preprocess the Excel file
    df = pd.read_excel(excel_path, sheet_name='Positionen', skiprows=6)
    df = df.dropna(subset=['Ticker'])

    # Load region suffix dictionary
    suffix_data = pd.read_excel(excel_path, sheet_name='suffix_dict')
    suffix_dict = dict(zip(suffix_data['Region'], suffix_data['Suffix']))

    for index, row in df.iterrows():
        ticker = row['Ticker']
        region = row['Region']
        print(f"({index + 1}/{len(df)}) Processing ticker: {ticker}")
        process_ticker(ticker, region, suffix_dict, db_path)
        time.sleep(1)  # To avoid hitting API rate limits

if __name__ == "__main__":
    main()