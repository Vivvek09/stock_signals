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
stocks = ["ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS", 
    "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "BPCL.NS", 
    "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS", 
    "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", 
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS", 
    "INFY.NS", "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS", 
    "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS", 
    "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS", 
    "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS", 
    "TITAN.NS", "ULTRACEMCO.NS", "UPL.NS", "WIPRO.NS"]

# Define the date range
end_date = date.today()+timedelta(days=1)
start_date = end_date - timedelta(days=40)
num_periods = 20

# Calculate the start date x days before
start_date_x_days_before = get_date_x_days_before(start_date, num_periods * 2)

# Streamlit app
st.title("Stock Buy and Sell Signals")


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
            if (stock_data['Open'].iloc[i] <= stock_data['SMA'].iloc[i]) and (stock_data['Close'].iloc[i] >= stock_data['SMA'].iloc[i]) and (stock_data['Open'].iloc[i]<stock_data['Close'].iloc[i]):
                stock_data.loc[stock_data.index[i], 'Buy Signal'] = 1
            elif (stock_data['Open'].iloc[i] >= stock_data['SMA'].iloc[i]) and (stock_data['Close'].iloc[i] <= stock_data['SMA'].iloc[i]) and (stock_data['Open'].iloc[i]>stock_data['Close'].iloc[i]):
                stock_data.loc[stock_data.index[i], 'Sell Signal'] = 1
            if (stock_data['Close'].iloc[i-1] >= stock_data['SMA'].iloc[i-1]) and (stock_data['Open'].iloc[i] <= stock_data['SMA'].iloc[i]) and (stock_data['Close'].iloc[i] <= stock_data['SMA'].iloc[i]) and (stock_data['Open'].iloc[i]>stock_data['Close'].iloc[i]):
                stock_data.loc[stock_data.index[i], 'Sell Signal'] = 1
            if (stock_data['Close'].iloc[i-1] <= stock_data['SMA'].iloc[i-1]) and (stock_data['Open'].iloc[i] >= stock_data['SMA'].iloc[i]) and (stock_data['Close'].iloc[i] >= stock_data['SMA'].iloc[i]) and (stock_data['Open'].iloc[i]<stock_data['Close'].iloc[i]):
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
st.write(f"{end_date}")
if buy_signals[day_index]:
    for stock, signal_date, signal in buy_signals[day_index]:
        st.write(f"{signal_date}: {stock} - {signal}")
        chart_url = f"https://finance.yahoo.com/quote/{stock}/chart/#eyJsYXlvdXQiOnsiaW50ZXJ2YWwiOiJkYXkiLCJwZXJpb2RpY2l0eSI6MSwidGltZVVuaXQiOm51bGwsImNhbmRsZVdpZHRoIjoxMy4wNDUxNDk1MTQ3OTk1MTUsImZsaXBwZWQiOmZhbHNlLCJ2b2x1bWVVbmRlcmxheSI6ZmFsc2UsImFkaiI6dHJ1ZSwiY3Jvc3NoYWlyIjp0cnVlLCJjaGFydFR5cGUiOiJjYW5kbGUiLCJleHRlbmRlZCI6ZmFsc2UsIm1hcmtldFNlc3Npb25zIjp7fSwiYWdncmVnYXRpb25UeXBlIjoib2hsYyIsImNoYXJ0U2NhbGUiOiJsaW5lYXIiLCJwYW5lbHMiOnsiY2hhcnQiOnsicGVyY2VudCI6MSwiZGlzcGxheSI6Il5OU0VJIiwiY2hhcnROYW1lIjoiY2hhcnQiLCJpbmRleCI6MCwieUF4aXMiOnsibmFtZSI6ImNoYXJ0IiwicG9zaXRpb24iOm51bGx9LCJ5YXhpc0xIUyI6W10sInlheGlzUkhTIjpbImNoYXJ0Il19fSwic2V0U3BhbiI6eyJtdWx0aXBsaWVyIjozLCJiYXNlIjoibW9udGgiLCJwZXJpb2RpY2l0eSI6eyJwZXJpb2QiOjEsInRpbWVVbml0IjoiZGF5In0sInNob3dFdmVudHNRdW90ZSI6dHJ1ZSwiZm9yY2VMb2FkIjp0cnVlfSwib3V0bGllcnMiOmZhbHNlLCJhbmltYXRpb24iOnRydWUsImhlYWRzVXAiOnsic3RhdGljIjp0cnVlLCJkeW5hbWljIjpmYWxzZSwiZmxvYXRpbmciOmZhbHNlfSwibGluZVdpZHRoIjoyLCJmdWxsU2NyZWVuIjp0cnVlLCJzdHJpcGVkQmFja2dyb3VuZCI6dHJ1ZSwiY29sb3IiOiIjMDA4MWYyIiwic3R1ZHlMZWdlbmQiOnsiZXhwYW5kZWQiOmZhbHNlfSwic3ltYm9scyI6W3sic3ltYm9sIjoiXk5TRUkiLCJzeW1ib2xPYmplY3QiOnsic3ltYm9sIjoiXk5TRUkiLCJxdW90ZVR5cGUiOiJJTkRFWCIsImV4Y2hhbmdlVGltZVpvbmUiOiJBc2lhL0tvbGthdGEiLCJwZXJpb2QxIjoxNjc3MTc3MDAwLCJwZXJpb2QyIjoxNzE3NDkzNDAwfSwicGVyaW9kaWNpdHkiOjEsImludGVydmFsIjoiZGF5IiwidGltZVVuaXQiOm51bGwsInNldFNwYW4iOm51bGx9XSwic3R1ZGllcyI6eyLigIxCb2xsaW5nZXIgQmFuZHPigIwgKDIwLDIsbWEseSkiOnsidHlwZSI6IkJvbGxpbmdlciBCYW5kcyIsImlucHV0cyI6eyJQZXJpb2QiOjIwLCJGaWVsZCI6ImZpZWxkIiwiU3RhbmRhcmQgRGV2aWF0aW9ucyI6MiwiTW92aW5nIEF2ZXJhZ2UgVHlwZSI6Im1hIiwiQ2hhbm5lbCBGaWxsIjp0cnVlLCJpZCI6IuKAjEJvbGxpbmdlciBCYW5kc.KAjCAoMjAsMixtYSx5KSIsImRpc3BsYXkiOiLigIxCb2xsaW5nZXIgQmFuZHPigIwgKDIwLDIsbWEseSkifSwib3V0cHV0cyI6eyJCb2xsaW5nZXIgQmFuZHMgVG9wIjoiYXV0byIsIkJvbGxpbmdlciBCYW5kcyBNZWRpYW4iOiJhdXRvIiwiQm9sbGluZ2VyIEJhbmRzIEJvdHRvbSI6ImF1dG8ifSwicGFuZWwiOiJjaGFydCIsInBhcmFtZXRlcnMiOnsiY2hhcnROYW1lIjoiY2hhcnQiLCJlZGl0TW9kZSI6dHJ1ZSwicGFuZWxOYW1lIjoiY2hhcnQifSwiZGlzYWJsZWQiOmZhbHNlfX0sInJhbmdlIjpudWxsfSwiZXZlbnRzIjp7ImRpdnMiOnRydWUsInNwbGl0cyI6dHJ1ZSwidHJhZGluZ0hvcml6b24iOiJub25lIiwic2lnRGV2RXZlbnRzIjpbXX0sInByZWZlcmVuY2VzIjp7ImN1cnJlbnRQcmljZUxpbmUiOnRydWUsImRpc3BsYXlDcm9zc2hhaXJzV2l0aERyYXdpbmdUb29sIjpmYWxzZSwiZHJhd2luZ3MiOm51bGwsImhpZ2hsaWdodHNSYWRpdXMiOjEwLCJoaWdobGlnaHRzVGFwUmFkaXVzIjozMCwibWFnbmV0IjpmYWxzZSwiaG9yaXpvbnRhbENyb3NzaGFpckZpZWxkIjpudWxsLCJsYWJlbHMiOnRydWUsImxhbmd1YWdlIjpudWxsLCJ0aW1lWm9uZSI6IkFzaWEvS29sa2F0YSIsIndoaXRlc3BhY2UiOjUwLCJ6b29tSW5TcGVlZCI6bnVsbCwiem9vbU91dFNwZWVkIjpudWxsLCJ6b29tQXRDdXJyZW50TW91c2VQb3NpdGlvbiI6ZmFsc2V9fQ--"
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
