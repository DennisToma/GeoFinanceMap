import yfinance as yf
import pandas as pd

def get_working_tickers():
    excel_path = "data\FTSE_All-World.xlsx"

    # Load and preprocess the Excel file
    df = pd.read_excel(excel_path, sheet_name='Positionen', skiprows=6)
    df = df.dropna(subset=['Ticker'])

    # region suffix dictionary
    data = pd.read_excel(excel_path, sheet_name='suffix_dict')
    suffix_dict = dict(zip(data['Region'], data['Suffix']))

    successful_responses = 0
    working_tickers = []
    failed_tickers = []
    i = 0

    for ticker, region in zip(df['Ticker'], df['Region']):
        i += 1
        print(f"Processing ticker {i}/{len(df['Ticker'])}: {ticker}")
        try:
            data = yf.download(ticker, start="2023-01-01", end="2024-01-01", progress=False)
            
            # Check if data is returned
            if not data.empty:
                successful_responses += 1
                working_tickers.append(ticker)
            else:
                ticker_with_suffix = ticker + "." + suffix_dict.get(region, "")
                print(f"Unsuccessful. Trying {ticker_with_suffix}")
                data = yf.download(ticker_with_suffix, start="2023-01-01", end="2024-01-01", progress=False)
                
                if not data.empty:
                    print("Successful!\n")
                    successful_responses += 1
                    working_tickers.append(ticker_with_suffix)
        
        except Exception as e:
            failed_tickers.append(ticker)

    with open("data\working_tickers.txt", "w") as file:
        for ticker in working_tickers:
            file.write(f"{ticker}\n")    
    return working_tickers, failed_tickers

get_working_tickers()