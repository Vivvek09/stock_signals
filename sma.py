import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import date

# Define the function to get a date x days before a given date
def get_date_x_days_before(start_date, num_days_before):
    """Calculates a date x days before a given date.

    Args:
        start_date (datetime.date): The starting date object.
        num_days_before (int): The number of days to subtract.

    Returns:
        str: The date x days before the start date in YYYY-MM-DD format.
    """
    date_object = dt.datetime.strptime(start_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
    new_date = date_object - dt.timedelta(days=num_days_before)
    return new_date.strftime("%Y-%m-%d")

# Define the list of stock tickers
stocks = ["HDFCLIFE.NS", "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", # Add more tickers as needed
          "KOTAKBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS", "HINDUNILVR.NS",
          "ITC.NS", "AXISBANK.NS", "BAJFINANCE.NS", "LT.NS", "M&M.NS",
          "SUNPHARMA.NS", "HCLTECH.NS", "ASIANPAINT.NS", "MARUTI.NS", "NESTLEIND.NS",
          "WIPRO.NS", "ULTRACEMCO.NS", "TATASTEEL.NS", "POWERGRID.NS", "GRASIM.NS",
          "NTPC.NS", "TECHM.NS", "JSWSTEEL.NS", "TATAMOTORS.NS", "ADANIPORTS.NS",
          "TITAN.NS", "INDUSINDBK.NS", "BPCL.NS", "HINDALCO.NS", "DRREDDY.NS",
          "COALINDIA.NS", "DIVISLAB.NS", "SBILIFE.NS", "BRITANNIA.NS", "HEROMOTOCO.NS",
          "EICHERMOT.NS", "BAJAJFINSV.NS", "ONGC.NS", "SHREECEM.NS", "CIPLA.NS",
          "ADANIGREEN.NS", "GAIL.NS", "IOC.NS", "VEDL.NS", "DLF.NS"]

# Define the date range
end_date = date.today()
start_date = end_date - dt.timedelta(days=40)
num_periods = 20

# Calculate the start date x days before
start_date_x_days_before = get_date_x_days_before(start_date, num_periods * 2)

# Initialize lists to store results
buy_signals = []
sell_signals = []

# Loop through each stock ticker
for stock in stocks:
    # Download the stock data
    stock_data = yf.download(stock, start=start_date_x_days_before, end=end_date)

    # Compute the 20-day Simple Moving Average (SMA)
    stock_data["SMA"] = stock_data["Close"].rolling(window=num_periods).mean()
    
    # Remove the dates before the actual start date
    stock_data = stock_data.loc[start_date:]
    
    # Initialize columns for buy and sell signals
    stock_data['Buy Signal'] = 0
    stock_data['Sell Signal'] = 0

    # Iterate through the data to find buy and sell signals
    for i in range(1, len(stock_data)):
        if (stock_data['Open'].iloc[i] <= stock_data['SMA'].iloc[i]) and (stock_data['Close'].iloc[i] >= stock_data['SMA'].iloc[i]):
            stock_data.loc[stock_data.index[i], 'Buy Signal'] = 1
        elif (stock_data['Open'].iloc[i] >= stock_data['SMA'].iloc[i]) and (stock_data['Close'].iloc[i] <= stock_data['SMA'].iloc[i]):
            stock_data.loc[stock_data.index[i], 'Sell Signal'] = 1
        if (stock_data['Close'].iloc[i-1] >= stock_data['SMA'].iloc[i-1]) and (stock_data['Open'].iloc[i] <= stock_data['SMA'].iloc[i]) and (stock_data['Close'].iloc[i] <= stock_data['SMA'].iloc[i]):
            stock_data.loc[stock_data.index[i], 'Sell Signal'] = 1
        if (stock_data['Close'].iloc[i-1] <= stock_data['SMA'].iloc[i-1]) and (stock_data['Open'].iloc[i] >= stock_data['SMA'].iloc[i]) and (stock_data['Close'].iloc[i] >= stock_data['SMA'].iloc[i]):
            stock_data.loc[stock_data.index[i], 'Buy Signal'] = 1

    # Check if there is a buy or sell signal for today
    if not stock_data.empty:
        latest_data = stock_data.iloc[-1]
        if latest_data['Buy Signal'] == 1:
            buy_signals.append(stock)
        if latest_data['Sell Signal'] == 1:
            sell_signals.append(stock)

# Print the results
print("Buy Signals for Today:")
for stock in buy_signals:
    print(stock)

    

print("\nSell Signals for Today:")
for stock in sell_signals:
    print(stock)