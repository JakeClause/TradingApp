import pandas as pd
import matplotlib.pyplot as plt
import os
import mplfinance as mpf

def load_data(historical_file, predictions_file):
    # Load historical data
    if os.path.exists(historical_file):
        try:
            data = pd.read_csv(historical_file, parse_dates=True, index_col=0)
            print("Historical Data Loaded Successfully")
        except Exception as e:
            print(f"Error loading historical data: {e}")
            return None, None
    else:
        print("Historical data file not found.")
        return None, None

    # Load predictions data
    if os.path.exists(predictions_file):
        try:
            predictions = pd.read_csv(predictions_file, parse_dates=True, index_col=0)
            print("Predictions Data Loaded Successfully")
        except Exception as e:
            print(f"Error loading predictions data: {e}")
            return data, None  # Return historical data even if predictions fail
    else:
        print("Predictions data file not found.")
        return data, None  # Return historical data even if predictions file is missing

    return data, predictions


def plot(historical_file, predictions_file, ticker):
    data, predictions = load_data(historical_file, predictions_file)
    """Plot futures data and predictions."""
    # Prepare data for candlestick plotting
    data = data[['Open', 'High', 'Low', 'Close']]  # Ensure you have Open, High, Low, Close columns

    # Calculate Bollinger Bands
    window = 20  # Number of periods for the moving average
    std_dev = 2  # Number of standard deviations for the bands

    data['MA'] = data['Close'].rolling(window=window).mean()  # Moving average
    data['Upper Band'] = data['MA'] + (data['Close'].rolling(window=window).std() * std_dev)  # Upper band
    data['Lower Band'] = data['MA'] - (data['Close'].rolling(window=window).std() * std_dev)  # Lower band

    # Get the last actual price
    last_actual_price = data['Close'].iloc[-1]
    # formated price to 2 decimal places
    last_actual_price = round(last_actual_price, 2)

    # Add the last actual price to the start of predictions to ensure continuity
    first_prediction_index = predictions.index[0]
    predictions.loc[first_prediction_index, 'Predicted Price'] = last_actual_price

    # Combine actual and predicted data
    full_data = pd.concat([data, predictions[['Predicted Price']]], axis=1)

    # Set the plot style for the candlestick chart
    ap = [
        mpf.make_addplot(full_data['Close'], color='blue', alpha=0.425, linestyle='-', label='Price'),
        mpf.make_addplot(full_data['MA'], color='orange', linestyle='-', label='Moving Average'),
        mpf.make_addplot(full_data['Upper Band'], color='red', linestyle='--', label='Upper Bollinger Band'),
        mpf.make_addplot(full_data['Lower Band'], color='green', linestyle='--', label='Lower Bollinger Band'),
        mpf.make_addplot(full_data['Predicted Price'], color='purple', linestyle='-', label='Predicted Price')
    ]

    # Current price
    last_close = data['Close'].iloc[-1]
    # Create the figure for mplfinance plot
    fig, ax = mpf.plot(full_data, type='candle', style='charles', title=f'{ticker}\'s Historical Prices ' + str(last_actual_price),
                        ylabel='Price in USD', volume=False, addplot=ap, figratio=(12, 8), figscale=1.2, returnfig=True)

    # Maximize the window for mplfinance
    mng = plt.get_current_fig_manager()

    # Windows method to maximize the plot window
    try:
        mng.window.state('zoomed')  # For Windows
    except:
        mng.window.showMaximized()  # For Linux / MacOS

    plt.show()
