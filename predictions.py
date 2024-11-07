import yfinance as yf
import pandas as pd
import numpy as np  # Ensure numpy is imported
from datetime import datetime, timedelta

def predict_prices(historical_file, predictions_csv):
    # Read the CSV file, parsing 'Datetime' and setting it as the index
    data = pd.read_csv(historical_file, parse_dates=['Datetime'], index_col='Datetime')
    
    # Check if 'Close' exists and drop NaNs if there are any initial rows with NaNs
    if 'Close' not in data.columns:
        print("Error: 'Close' column not found in the CSV file. Please check the format.")
        print(f"Columns found: {data.columns}")
        return

    # Drop rows with NaNs in the 'Close' column
    data.dropna(subset=['Close'], inplace=True)  # Remove any rows without Close values

    # Ensure the data is sorted by date
    data = data.sort_index()

    if len(data) >= 2:
        # Continue with your existing logic for price prediction...
        n = 5  # You can adjust this value for the moving average window
        data['Moving Average'] = data['Close'].rolling(window=n).mean()

        last_price = data['Close'].iloc[-1]
        moving_avg = data['Moving Average'].iloc[-1]

        # Calculate momentum and volatility
        momentum = data['Close'].diff().iloc[-1]
        volatility = np.std(data['Close'].tail(n))

        # Generate future dates for predictions
        future_dates = [data.index[-1] + timedelta(hours=i) for i in range(1, 85)]

        # Create a list for predicted prices
        predicted_prices = []
        for i in range(len(future_dates)):
            if i % 6 == 0:
                momentum = np.random.normal(loc=0, scale=volatility)
                volatility = np.std(data['Close'].tail(n) + predicted_prices[-n:] if len(predicted_prices) >= n else data['Close'].tail(n))

            price_change = momentum + np.random.normal(loc=0, scale=volatility)
            next_price = last_price + price_change
            next_price = np.clip(next_price, moving_avg - (volatility * 2), moving_avg + (volatility * 2))

            predicted_prices.append(next_price)
            last_price = next_price

        # Create a DataFrame for the predicted prices
        future_data = pd.DataFrame({
            'Datetime': future_dates,
            'Predicted Price': predicted_prices,
        })

        # Save the predicted prices to a new CSV file
        future_data.to_csv(predictions_csv, index=False)
        print(f"Predicted prices saved to {predictions_csv}")
    else:
        print("Not enough data to make predictions.")
