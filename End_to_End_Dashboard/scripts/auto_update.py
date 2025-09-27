import os
import schedule
import time
import logging
from scripts.data_fetch import fetch_data
from scripts.data_clean import clean_data
from scripts.analysis import analyze_data

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job():
    try:
        logging.info("Starting daily stock data update...")
        
        
        fetch_data(ticker='AAPL', period='1y', interval='1d')
        
        # Clean and process data
        clean_data()
        
        # Run analysis and predictions
        analyze_data()
        
        logging.info("Daily stock data update completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Schedule the job every day at a specific time (e.g., 09:00 AM)
schedule.every().day.at("09:00").do(job)

if __name__ == "__main__":
    logging.info("Scheduler started. Waiting for the next scheduled job...")
    while True:
        schedule.run_pending()
        time.sleep(1)