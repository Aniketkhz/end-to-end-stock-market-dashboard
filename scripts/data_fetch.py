import os
import yfinance as yf
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_stock_data(ticker, period='1y', interval='1d'):
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logging.info(f"Created data directory: {data_dir}")

    logging.info(f"Fetching data for {ticker}...")
    stock_data = yf.download(ticker, period=period, interval=interval)

    if stock_data.empty:
        logging.warning(f"No data found for {ticker}")
        return

    # Reset the index to make Date a column
    stock_data.reset_index(inplace=True)
    
    # If columns are MultiIndex, flatten them
    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = [col[0] if col[1] == '' else col[1] for col in stock_data.columns]
    
    # Ensure column names are clean
    stock_data.columns = stock_data.columns.str.strip()
    
    # Save CSV with proper Date column
    file_path = os.path.join(data_dir, f"{ticker}_data.csv")
    stock_data.to_csv(file_path, index=False)
    logging.info(f"Saved {ticker} data to {file_path}")
    logging.info(f"Columns saved: {stock_data.columns.tolist()}")
    logging.info(f"Total rows: {len(stock_data)}")

if __name__ == "__main__":
    # You can add multiple tickers here
    tickers = ['AAPL', 'GOOGL', 'MSFT']  # Add more as needed
    
    for ticker in tickers:
        try:
            fetch_stock_data(ticker)
        except Exception as e:
            logging.error(f"Error fetching {ticker}: {e}")