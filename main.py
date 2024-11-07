from getPricing import getPrice, saveData
from predictions import predict_prices
from chart import plot
import os

def csv_check(symbol):
    # Directory and file paths
    csv_dir = "./4/csv"
    historical_data_csv = f"{csv_dir}/{symbol}_2weeks_data.csv"
    predicted_prices_csv = f"{csv_dir}/{symbol}_price_predictions.csv"

    # Check if 'csv' directory exists, create it if not
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    return historical_data_csv, predicted_prices_csv

def intro():
    #Ask if the user wants to view stocks, futures, or crypto
    print("\nWelcome to the financial data visualization tool!\n--------------------------------------------------\n")
    choice = input("Please select the type of data you would like to view (1 = Stocks, 2 = Crypto, 3 = futures): ")
    while (choice != "1" and choice != "2" and choice != "3"):
        choice = input("\n\nInvalid Choice! Please select the type of data you would like to view (1 = Stocks, 2 = Crypto, 3 = futures): ")
    if (choice == "1"):
        ticker = input("Enter the stock ticker symbol (e.g., AAPL): ").upper()
        price = getPrice(ticker, choice)
    elif (choice == "2"):
        print("Crypto selected")
        ticker = input("Enter the cryptocurrency symbol (e.g., BTC): ").upper()
        price = getPrice(ticker, choice)
    elif (choice == "3"):
        print("Futures selected")
        ticker = input("Enter the futures symbol (e.g., GC): ").upper()
        price = getPrice(ticker, choice)

    print("Ticker" + ticker)
    print("Price: " + str(price))
    return ticker, price, choice

def main():
    ticker, current_price, choice = intro()
    historical_data_csv, predicted_prices_csv = csv_check(ticker)
    saveData(ticker, choice, historical_data_csv)
    predict_prices(historical_data_csv, predicted_prices_csv)
    plot(historical_data_csv, predicted_prices_csv, ticker)
    

if __name__ == "__main__":
    main()