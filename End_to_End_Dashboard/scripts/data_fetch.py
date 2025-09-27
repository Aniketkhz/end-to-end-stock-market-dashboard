import os
import yfinance as yf
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_stock_data(ticker, period='1y', interval='1d'):
    # Create data directory if it doesn't exist
    data_dir = '../data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logging.info(f"Created directory: {data_dir}")

    
    try:
        stock_data = yf.download(ticker, period=period, interval=interval)
        if stock_data.empty:
            logging.warning(f"No data found for ticker: {ticker}")
            return

        # Save to CSV
        file_path = os.path.join(data_dir, f"{ticker}_data.csv")
        stock_data.to_csv(file_path)
        logging.info(f"Data for {ticker} saved to {file_path}")

    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {e}")

# Example usage
if __name__ == "__main__":
    fetch_stock_data('AAPL')