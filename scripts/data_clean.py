import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_and_process_data(file_path):
    logging.info("Loading data from %s", file_path)
    df = pd.read_csv(file_path)

    if 'Date' not in df.columns and df.index.name == 'Date':
        df.reset_index(inplace=True)

    df['Date'] = pd.to_datetime(df['Date'])

    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.ffill(inplace=True)
    df.drop_duplicates(inplace=True)
    df['Daily Change %'] = df['Close'].pct_change() * 100
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()

    processed_file_path = os.path.splitext(file_path)[0] + '_processed.csv'
    df.to_csv(processed_file_path, index=False)
    logging.info(f"Processed data saved to {processed_file_path}")

if __name__ == "__main__":
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    
    # Process ALL CSV files in data folder
    for file_name in os.listdir(data_folder):
        if file_name.endswith('_data.csv') and not file_name.endswith('_processed.csv'):
            clean_and_process_data(os.path.join(data_folder, file_name))