from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

# Load the new regression model for predicting stock price 30 days ahead
with open(r'C:\Users\Sezy\OneDrive\Own_Workspace\Popular_Stocks\Saved_Models\stock_price_predictor_model.pkl', 'rb') as f:
    regression_model = pickle.load(f)

app = Flask(__name__)

# Function to predict the future stock price (using the regression model)
def predict_stock_price(stock_data, model):
    features = ['Open', 'High', 'Low', 'Close', 'Volume']  # Features used to train the model
    X = stock_data[features]
    
    # Predict the stock price using the regression model
    predicted_price = model.predict(X)
    
    return np.mean(predicted_price)  # Return the average prediction

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict_route():
    # Get the ticker from the form submission
    ticker = request.form.get('ticker')
    if not ticker:
        return "Ticker is required!", 400

    # Load the stock data for the selected ticker from CSV
    csv_path = r"C:\Users\Sezy\OneDrive\Own_Workspace\Popular_Stocks\CSV_FILES\top_100_stocks_2025_updated.csv"
    data = pd.read_csv(csv_path)
    stock_data = data[data['Ticker'] == ticker]
    
    if stock_data.empty:
        return f"Stock ticker {ticker} not found.", 404

    # Get the most recent available data (last row)
    latest_data = stock_data.iloc[-1]

    # Extract the relevant information
    latest_date = latest_data['Date']
    current_price = latest_data['Close']

    # Prepare the features for prediction (using the last available data)
    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    latest_features = latest_data[features].values.reshape(1, -1)

    # Predict the stock price using the regression model
    predicted_price = regression_model.predict(latest_features)[0]

    # Calculate the price change percentage
    price_change = ((predicted_price - current_price) / current_price) * 100

    # Render the stock_page.html template with the predictions
    return render_template('stock_page.html', 
                           ticker=ticker,
                           current_price=current_price,
                           predicted_price=predicted_price,
                           price_change=price_change,
                           latest_date=latest_date)

if __name__ == '__main__':
    app.run(debug=True)
