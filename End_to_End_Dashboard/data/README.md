# Overview of the Data Folder

The `data` folder is a crucial component of the End-to-End Dashboard project. It is designed to store all the stock market data files used throughout the project. 

## Structure

- **Raw Data**: This folder will contain the raw CSV files fetched from the stock market using the `data_fetch.py` script. The naming convention for these files will be `<TICKER>_data.csv`, where `<TICKER>` is the stock ticker symbol.
  
- **Processed Data**: After cleaning and processing, the cleaned CSV files will be saved in this folder with a `_processed` suffix, following the format `<TICKER>_data_processed.csv`.

## Purpose

The primary purpose of the `data` folder is to organize and manage the stock market data efficiently, ensuring that both raw and processed data are easily accessible for analysis and visualization in the dashboard. This structure facilitates data management and enhances the overall workflow of the project.