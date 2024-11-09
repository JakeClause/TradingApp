from intro import run_gui
from getPricing import getPrice, saveData
from predictions import predict_prices
from chart import plot
import os

def csv_check(symbol):
    csv_dir = "./TradingAPP/csv"
    historical_data_csv = f"{csv_dir}/{symbol}_2weeks_data.csv"
    predicted_prices_csv = f"{csv_dir}/{symbol}_price_predictions.csv"

    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    return historical_data_csv, predicted_prices_csv

def main():
    # Call the GUI to get user input
    ticker, current_price, choice = run_gui()

    # Ensure that the user entered valid input
    if not ticker or not current_price or not choice:
        print("Operation canceled or invalid input.")
        return

    # Proceed with the main processing logic
    historical_data_csv, predicted_prices_csv = csv_check(ticker)
    saveData(ticker, choice, historical_data_csv)
    predict_prices(historical_data_csv, predicted_prices_csv)
    plot(historical_data_csv, predicted_prices_csv, ticker)

if __name__ == "__main__":
    main()
