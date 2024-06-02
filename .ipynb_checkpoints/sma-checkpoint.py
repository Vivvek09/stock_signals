import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt

# Define the function to get a date x days before a given date
def get_date_x_days_before(date_string, num_days_before):
    date_object = dt.datetime.strptime(date_string, "%Y-%m-%d")
    new_date = date_object - dt.timedelta(days=num_days_before)
    new_date_string = new_date.strftime("%Y-%m-%d")
    return new_date_string

# Define the stock and date range
stock = "AAPL"
start_date = "2020-12-10"
end_date = "2020-12-31"
num_periods = 20

# Calculate the start date x days before to accommodate the period size
start_date_x_days_before = get_date_x_days_before(start_date, num_periods * 2)

# Download the stock data
stock_data = yf.download(stock, start=start_date_x_days_before, end=end_date)

# Compute the 20-day Simple Moving Average (SMA)
stock_data["SMA"] = stock_data["Close"].rolling(window=num_periods).mean()

# Remove the dates before the actual start date
stock_data = stock_data[start_date:]

# Initialize columns for buy and sell signals
stock_data['Buy Signal'] = 0
stock_data['Sell Signal'] = 0

# Iterate through the data to find buy and sell signals
for i in range(1, len(stock_data)):
    if (stock_data['Open'][i] < stock_data['SMA'][i]) and (stock_data['Close'][i] > stock_data['SMA'][i]):
        stock_data.at[stock_data.index[i], 'Buy Signal'] = 1
    elif (stock_data['Open'][i] > stock_data['SMA'][i]) and (stock_data['Close'][i] < stock_data['SMA'][i]):
        stock_data.at[stock_data.index[i], 'Sell Signal'] = 1

# Plot the data with buy and sell signals
plt.figure(figsize=(14, 7))
plt.plot(stock_data.index, stock_data['Close'], label='Closing Price', color='black')
plt.plot(stock_data.index, stock_data['SMA'], label='20-Day SMA', color='blue')
plt.plot(stock_data.index, stock_data['Open'], label='20-Day SMA', color='green')

# Plot buy signals
plt.plot(stock_data[stock_data['Buy Signal'] == 1].index,
         stock_data['SMA'][stock_data['Buy Signal'] == 1],
         '^', markersize=10, color='green', label='Buy Signal')

# Plot sell signals
plt.plot(stock_data[stock_data['Sell Signal'] == 1].index,
         stock_data['SMA'][stock_data['Sell Signal'] == 1],
         'v', markersize=10, color='red', label='Sell Signal')

plt.title(f"{stock} Closing Prices and 20-Day SMA with Buy/Sell Signals")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the plot as a file (optional)
# plt.savefig("AAPL_SMA_Buy_Sell_Signals.png", dpi=200)

# Display the plot
plt.show()

# Print the buy/sell signals
print(stock_data[stock_data['Buy Signal'] == 1][['Open', 'Close', 'SMA', 'Buy Signal']])
print(stock_data[stock_data['Sell Signal'] == 1][['Open', 'Close', 'SMA', 'Sell Signal']])
