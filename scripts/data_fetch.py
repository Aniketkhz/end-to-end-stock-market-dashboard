import os
import yfinance as yf
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_stock_data(ticker, period='1y', interval='1d'):
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    stock_data = yf.download(ticker, period=period, interval=interval)

    if stock_data.empty:
        logging.warning(f"No data found for {ticker}")
        return

    # Reset the index so date
    stock_data.reset_index(inplace=True)

    # Save CSV with Date column
    file_path = os.path.join(data_dir, f"{ticker}_data.csv")
    stock_data.to_csv(file_path, index=False)
    logging.info(f"Saved {ticker} data to {file_path}")

if __name__ == "__main__":
    fetch_stock_data('AAPL')
