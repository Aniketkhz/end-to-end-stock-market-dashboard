# End-to-End Stock Market Dashboard

## Project Overview
This project is designed to provide an end-to-end solution for fetching, processing, analyzing, and visualizing stock market data. It utilizes various libraries and tools to create a comprehensive dashboard that allows users to interact with stock market data in real-time.

## Business Value
The dashboard serves investors, analysts, and enthusiasts by providing insights into stock performance, trends, and predictions. It enables informed decision-making based on historical and real-time data.

## Tech Stack
- **Python**: Main programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **yfinance**: Fetching live stock market data
- **Plotly**: Interactive visualizations
- **Streamlit**: Web application framework for the dashboard
- **Scikit-learn**: Machine learning library for predictions
- **Schedule**: Task scheduling for automation

## Features
- Fetch live stock market data using the yfinance library
- Clean and process data to compute key metrics
- Visualize stock prices and daily changes with interactive charts
- Predict future stock prices using machine learning models
- Automate daily updates of stock data

## Instructions for Running Locally
1. Clone the repository:
   ```
   git clone <repository-url>
   cd End_to_End_Dashboard
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit dashboard:
   ```
   streamlit run dashboard/app.py
   ```

## Deployment Instructions
To deploy the dashboard on Heroku:
1. Ensure you have the Heroku CLI installed and are logged in.
2. Create a new Heroku app:
   ```
   heroku create <app-name>
   ```
3. Push the code to Heroku:
   ```
   git push heroku main
   ```
4. Open the app in your browser:
   ```
   heroku open
   ```

## Optional Screenshots and Architecture Diagrams
(Include any relevant visuals here)