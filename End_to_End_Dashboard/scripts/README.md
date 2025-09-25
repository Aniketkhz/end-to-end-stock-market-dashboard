# Overview of the Scripts Folder

The `scripts` folder contains Python scripts that are essential for the data collection, cleaning, analysis, and automation processes of the End-to-End Dashboard project. Each script serves a specific purpose in the workflow of fetching, processing, and analyzing stock market data. Below is a brief description of each script:

1. **data_fetch.py**: This script is responsible for fetching live stock market data using the `yfinance` library. It allows users to specify the ticker symbol, period, and interval for the data retrieval. The fetched data is saved as a CSV file in the `data` folder.

2. **data_clean.py**: This script processes the raw stock market data obtained from `data_fetch.py`. It handles missing values, removes duplicates, and computes new columns such as Daily Change %, 20-day moving average, and 50-day moving average. The cleaned data is saved with a `_processed` suffix.

3. **analysis.py**: This script performs analytics on the processed stock market data. It computes additional key performance indicators (KPIs) and can implement machine learning models, such as Linear Regression, to predict the next day's closing price. The predictions are added to the processed CSV file.

4. **auto_update.py**: This script automates the daily update of stock data. It uses the `schedule` library to run tasks that fetch the latest stock data, process it, and perform optional analysis or predictions. The script is designed to run daily at a specified time.

Each script is designed to be modular and can be executed independently, allowing for flexibility in the data processing pipeline.