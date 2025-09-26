# Python script to process stock market CSV data
import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_and_process_data(file_path):
    logging.info("Loading data from %s", file_path)
    df = pd.read_csv(file_path)

    # Reset index if needed (some CSVs from yfinance have Date as index)
    if 'Date' not in df.columns and df.index.name == 'Date':
        df.reset_index(inplace=True)

    # Ensure Date column is datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert numeric columns to floats
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill missing values & remove duplicates
    df.ffill(inplace=True)
    df.drop_duplicates(inplace=True)

    # Compute Daily Change %
    df['Daily Change %'] = df['Close'].pct_change() * 100

    # Compute all moving averages
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()

    # Save processed CSV
    processed_file_path = os.path.splitext(file_path)[0] + '_processed.csv'
    df.to_csv(processed_file_path, index=False)
    logging.info(f"Processed data saved to {processed_file_path}")

if __name__ == "__main__":
    # Use absolute path to avoid issues
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    file_name = 'AAPL_data.csv'  # Change ticker if needed
    clean_and_process_data(os.path.join(data_folder, file_name))
