import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_and_process_data(file_path):
    logging.info("Loading data from %s", file_path)
    
    # Try reading with different settings
    df = pd.read_csv(file_path, index_col=0)
    
    # Print columns and index for debugging
    logging.info(f"Index name: {df.index.name}")
    logging.info(f"Columns found: {df.columns.tolist()}")
    logging.info(f"First few index values: {df.index[:3].tolist()}")
    
    # The index should be the Date
    if df.index.name is None or df.index.name != 'Date':
        df.index.name = 'Date'
    
    # Reset index to make Date a column
    df.reset_index(inplace=True)
    
    # Ensure Date column exists
    if 'Date' not in df.columns:
        logging.error(f"Cannot find Date column. Available columns: {df.columns.tolist()}")
        return

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

    # Compute moving averages
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()

    # Save processed CSV
    processed_file_path = os.path.splitext(file_path)[0] + '_processed.csv'
    df.to_csv(processed_file_path, index=False)
    logging.info(f"Processed data saved to {processed_file_path}")

if __name__ == "__main__":
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    
    # Process ALL raw data files
    if os.path.exists(data_folder):
        for file_name in os.listdir(data_folder):
            if file_name.endswith('_data.csv') and not file_name.endswith('_processed.csv'):
                logging.info(f"Processing {file_name}...")
                clean_and_process_data(os.path.join(data_folder, file_name))
    else:
        logging.error(f"Data folder not found: {data_folder}")