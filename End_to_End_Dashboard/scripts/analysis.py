# Python script to predict next day's stock closing price
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def predict_next_day_close(file_path):
    # Load processed CSV data
    try:
        data = pd.read_csv(file_path)
        logging.info("Loaded processed data successfully.")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return

    # Prepare data for prediction
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    
    # Create features and target variable
    data['Prev_Close'] = data['Close'].shift(1)
    data.dropna(inplace=True)  # Drop rows with NaN values

    X = data[['Prev_Close']]
    y = data['Close']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    logging.info("Model training completed.")

    # Make prediction for the next day
    last_close = data['Close'].iloc[-1]
    predicted_close = model.predict([[last_close]])[0]
    logging.info(f"Predicted next day's closing price: {predicted_close}")

    # Add predicted value as a new column in the DataFrame
    data['Predicted_Close'] = data['Close'].shift(-1)
    data.iloc[-1, data.columns.get_loc('Predicted_Close')] = predicted_close

    # Save updated CSV in the data folder
    output_file_path = file_path.replace('.csv', '_processed.csv')
    try:
        data.to_csv(output_file_path, index=True)
        logging.info(f"Updated data saved to {output_file_path}.")
    except Exception as e:
        logging.error(f"Error saving updated data: {e}")

if __name__ == "__main__":
    predict_next_day_close('../data/AAPL_data_processed.csv')  # Adjust path as necessary