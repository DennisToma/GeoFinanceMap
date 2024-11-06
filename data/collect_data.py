import yfinance as yf
import pandas as pd

tickers = ['AAPL', 'MSFT'] #, 'GOOGL', 'AMZN', 'TSLA']
start = '2000-01-01'
end = '2024-01-01'

def get_stock_info(tickers):
    stock_info = pd.DataFrame(columns=['Ticker', 'Name', 'Sector', 'Industry', 'Country', 'Zip Code', 'State', 'City', 'Address'])

    for ticker in tickers:
        data = yf.Ticker(ticker)
        row = [ticker, 
            data.info['longName'], 
            data.info['sector'], 
            data.info['industry'], 
            data.info['country'], 
            data.info['zip'], 
            data.info['state'], 
            data.info['city'], 
            data.info['address1']]

        stock_info.loc[len(stock_info.index)] = row
        
    stock_info.to_csv('data/stock_info.csv', index=False)
    return None


def get_historic_data(tickers, start, end):
    historic_data = yf.download(tickers, start=start, end=end, progress=False)
    historic_data.to_csv('data/historic_data.csv')
    #print(historic_data)
    return None