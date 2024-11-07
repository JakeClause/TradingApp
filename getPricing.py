import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def getPrice(symbol, choice):
    updated_symbol = symbol
    if choice == "2":
        updated_symbol += '-USD'  # Crypto
    elif choice == "3":
        updated_symbol += '=F'  # Futures

    try:
        # Define the time range based on interval availability
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)  # Reduced to 7 days for 1-minute data

        print(f"Fetching data from {start_time} to {end_time}")

        # Fetch historical data
        all_data = yf.download(updated_symbol, start=start_time, end=end_time, interval='1m', progress=False)

        # Get the current price (live data or last close price)
        futures = yf.Ticker(updated_symbol)
        live_price = futures.history(period="1d")['Close'].iloc[-1]

        if all_data.empty:
            print("\nNo data available. The market may have been closed.")
            return pd.DataFrame(), None

        return all_data, live_price

    except yf.YFPricesMissingError:
        print(f"\nError: No price data found for {updated_symbol}. The futures contract may be delisted or the symbol is incorrect.")
        return pd.DataFrame(), None
    except Exception as e:
        print(f"\nAn unexpected error occurred while fetching data for {updated_symbol}: {e}")
        return pd.DataFrame(), None


def saveData(ticker, choice, historical_data_csv):
    print("Fetching historical data and live price...")
    historical_data, live_price = getPrice(ticker, choice)

    if live_price is not None:
        print(f"\nLive price of {ticker}: ${live_price:.2f}")

    if historical_data is not None and not historical_data.empty:
        # Reset index to turn the datetime index into a column
        historical_data = historical_data.reset_index()

        # Remove any unwanted rows that may contain the ticker symbol in the first column
        if historical_data.iloc[0, 1] == ticker:  # Check if the first row has the ticker
            historical_data = historical_data.drop(historical_data.index[0])

        # Convert datetime to the desired format
        historical_data['Datetime'] = pd.to_datetime(historical_data['Datetime']).dt.strftime('%Y-%m-%d %I:%M %p')

        # Rename columns explicitly if they are not in the desired format
        historical_data.columns = ['Datetime', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']

        # Check for the correct column names
        print("Columns in historical data after renaming:", historical_data.columns.tolist())

        # Save the cleaned DataFrame to CSV
        historical_data.to_csv(historical_data_csv, index=False)
        print(f"Historical data saved to {historical_data_csv}")