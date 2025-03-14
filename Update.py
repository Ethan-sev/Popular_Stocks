import yfinance as yf
import pandas as pd
import numpy as np

# Function to calculate additional features
def calculate_indicators(stock_data):
    # Simple Moving Averages (SMA)
    stock_data['SMA_7'] = stock_data['Close'].rolling(window=7).mean()
    stock_data['SMA_30'] = stock_data['Close'].rolling(window=30).mean()
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()

    # Exponential Moving Averages (EMA)
    stock_data['EMA_10'] = stock_data['Close'].ewm(span=10, adjust=False).mean()
    stock_data['EMA_50'] = stock_data['Close'].ewm(span=50, adjust=False).mean()

    # Relative Strength Index (RSI)
    delta = stock_data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    stock_data['RSI'] = 100 - (100 / (1 + rs))

    # Fill missing values created by the rolling calculations
    stock_data.fillna(0, inplace=True)
    
    return stock_data

# Function to fetch new data
def fetch_new_data(ticker_symbols, start_date="2020-01-01"):
    all_data = pd.DataFrame()

    # Loop through each ticker symbol and fetch data
    for ticker_symbol in ticker_symbols:
        print(f"Fetching data for {ticker_symbol}...")

        # Create a Ticker object for each stock
        ticker = yf.Ticker(ticker_symbol)

        # Fetch historical market data from the start date to the present
        historical_data = ticker.history(start=start_date, end=pd.to_datetime("today").strftime('%Y-%m-%d'))

        # Add a new column 'Ticker' with the ticker symbol for each row
        historical_data['Ticker'] = ticker_symbol

        # Calculate technical indicators
        historical_data = calculate_indicators(historical_data)

        # Append the data to the all_data DataFrame
        all_data = pd.concat([all_data, historical_data])

    return all_data

# Function to update CSV
def update_csv(csv_path, ticker_symbols, start_date="2020-01-01"):
    try:
        # Load the existing CSV file
        existing_data = pd.read_csv(csv_path)

        # Fetch the latest data
        new_data = fetch_new_data(ticker_symbols, start_date)

        # Clean up the column names in case of any differences
        new_data.columns = new_data.columns.str.strip()

        # Merge the new data with the existing data, avoiding duplicates
        updated_data = pd.concat([existing_data, new_data]).drop_duplicates(subset=['Ticker', 'Date'])

        # Save the updated data back to the CSV file
        updated_data.to_csv(csv_path, index=False)
        print(f"Data successfully updated and saved to {csv_path}")

    except Exception as e:
        print(f"An error occurred while updating the CSV: {e}")

# List of ticker symbols to update
ticker_symbols = [ "MSFT", "AAPL", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "SPY", "V", "AMD", 
                   "NVDA", "INTC", "CSCO", "WMT", "DIS", "MCD", "BA", "PYPL", "SNAP", "NKE", 
                   "XOM", "CVX", "JNJ", "PFE", "BABA", "T", "VZ", "GE", "IBM", "GS", "JPM", 
                   "MS", "GS", "UNH", "CVS", "HD", "LOW", "UPS", "SBUX", "BLK", "DELL", "LMT", 
                   "ABT", "TXN", "TMO", "MRK", "AMAT", "INTU", "ADI", "MU", "LULU", "PLUG", 
                   "F", "GM", "COF", "STZ", "KMX", "TSCO", "LMT", "SHOP", "SQ", "BIDU", "SPG", 
                   "MELI", "BA", "ATVI", "GS", "CAT", "HLT", "TGT", "DOW", "COP", "BA", "NKE", 
                   "LULU", "GS", "JNJ", "JPM", "BRK-A", "MSFT", "V", "TSLA", "XOM", "PFE", 
                   "WMT", "GE", "T", "VZ", "AMZN", "BABA", "CSCO", "NVDA", "AAPL", "GOOGL", "INTC", 
                   "AMT", "CVX", "META", "WFC", "KO", "PEP", "K", "SBUX", "NKE", "LOW", "MCD", 
                   "DIS", "WMT", "XOM", "UPS", "HD", "TMO", "PYPL", "UBER", "ZM", "TEAM", "MDB", 
                   "DKNG"]

# Path to the CSV file
csv_path = r'C:\Users\Sezy\OneDrive\Personal_Trading_Algo\CSV_FILES\top_100_stocks_2025_updated.csv'

# Update the CSV
update_csv(csv_path, ticker_symbols)
