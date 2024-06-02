import yfinance as yf
import datetime as dt
import streamlit as st
from datetime import date, timedelta

# Define the function to get a date x days before a given date
def get_date_x_days_before(start_date, num_days_before):
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
start_date = end_date - timedelta(days=40)
num_periods = 20

# Calculate the start date x days before
start_date_x_days_before = get_date_x_days_before(start_date, num_periods * 2)

# Streamlit app
st.title("Stock Buy and Sell Signals")
st.write(f"Analyzing data from {start_date} to {end_date}")

# Initialize lists to store results
buy_signals = {0: [], 1: [], 2: []}
sell_signals = {0: [], 1: [], 2: []}
failed_stocks = []

# Loop through each stock ticker
for stock in stocks:
    try:
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

        # Check for buy or sell signals in the last 3 days
        if not stock_data.empty:
            for i in range(3):
                if len(stock_data) > i:
                    latest_data = stock_data.iloc[-(i+1)]
                    if latest_data['Buy Signal'] == 1:
                        buy_signals[i].append((stock, latest_data.name.date(), 'Buy'))
                    if latest_data['Sell Signal'] == 1:
                        sell_signals[i].append((stock, latest_data.name.date(), 'Sell'))
    except Exception as e:
        failed_stocks.append(stock)
        st.write(f"Failed to process {stock}: {e}")

# Select the day to display signals
days = ["Today", "Yesterday", "Day Before Yesterday"]
selected_day = st.selectbox("Select the day to view signals", days)

# Determine the index based on selected day
day_index = days.index(selected_day)

# Display the results
st.subheader(f"Buy Signals for {selected_day}")
if buy_signals[day_index]:
    for stock, signal_date, signal in buy_signals[day_index]:
        st.write(f"{signal_date}: {stock} - {signal}")
        chart_url = f"https://finance.yahoo.com/quote/{stock}/chart"
        st.markdown(f"[View {stock} chart]({chart_url})")
else:
    st.write(f"No buy signals for {selected_day.lower()}.")

st.subheader(f"Sell Signals for {selected_day}")
if sell_signals[day_index]:
    for stock, signal_date, signal in sell_signals[day_index]:
        st.write(f"{signal_date}: {stock} - {signal}")
        chart_url = f"https://finance.yahoo.com/quote/{stock}/chart"
        st.markdown(f"[View {stock} chart]({chart_url})")
else:
    st.write(f"No sell signals for {selected_day.lower()}.")

# Display any failed stock tickers
if failed_stocks:
    st.subheader("Failed to process the following stocks:")
    for stock in failed_stocks:
        st.write(stock)
