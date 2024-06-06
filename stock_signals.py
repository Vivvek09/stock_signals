import yfinance as yf
import datetime as dt
import streamlit as st
from datetime import date, timedelta

# Define the function to get a date x days before a given date
def get_date_x_days_before(start_date, num_days_before):
    date_object = dt.datetime.strptime(start_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
    new_date = date_object - dt.timedelta(days=num_days_before)
    return new_date.strftime("%Y-%m-%d")

# Define the list of stock tickers for each category
nifty_50_stocks = ["ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS", 
    "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "BPCL.NS", 
    "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS", 
    "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", 
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS", 
    "INFY.NS", "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS", 
    "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS", 
    "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS", 
    "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS", 
    "TITAN.NS", "ULTRACEMCO.NS", "UPL.NS", "WIPRO.NS"]

nifty_51_100_stocks = ["ABB.NS", "ACC.NS", "ADANIGREEN.NS", "ADANITRANS.NS", "ALKEM.NS", 
    "AMBUJACEM.NS", "AUROPHARMA.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BEL.NS", 
    "BERGEPAINT.NS", "BHEL.NS", "BIOCON.NS", "BOSCHLTD.NS", "CADILAHC.NS", 
    "CHOLAFIN.NS", "COLPAL.NS", "DABUR.NS", "DLF.NS", "EMAMILTD.NS", 
    "GAIL.NS", "GLAXO.NS", "GODREJCP.NS", "HAVELLS.NS", "HINDPETRO.NS", 
    "ICICIPRULI.NS", "IDFCFIRSTB.NS", "IGL.NS", "INDIGO.NS", "INDUSTOWER.NS", 
    "IOC.NS", "IRCTC.NS", "JINDALSTEL.NS", "L&TFH.NS", "LICI.NS", 
    "LUPIN.NS", "MCDOWELL-N.NS", "MOTHERSUMI.NS", "NAUKRI.NS", "NMDC.NS", 
    "PAGEIND.NS", "PEL.NS", "PETRONET.NS", "PIDILITIND.NS", "PIIND.NS", 
    "PNB.NS", "POLYCAB.NS", "RAMCOCEM.NS", "RECLTD.NS", "SAIL.NS", 
    "SBICARD.NS", "SHREECEM.NS", "SIEMENS.NS", "SRF.NS", "SRTRANSFIN.NS"]

nifty_101_200_stocks = ["AARTIIND.NS", "ABBOTINDIA.NS", "ADANIPOWER.NS", "AJANTPHARM.NS", "ALEMBICLTD.NS", 
    "APLLTD.NS", "ASHOKLEY.NS", "ASTRAL.NS", "ATUL.NS", "AUBANK.NS", 
    "BAJAJHLDNG.NS", "BALAMINES.NS", "BALKRISIND.NS", "BASF.NS", "BATAINDIA.NS", 
    "BHARATFORG.NS", "BHARATRAS.NS", "BLUEDART.NS", "BRIGADE.NS", "CANFINHOME.NS", 
    "CASTROLIND.NS", "CEATLTD.NS", "CENTRALBK.NS", "CENTURYTEX.NS", "CESC.NS", 
    "CROMPTON.NS", "CUB.NS", "CUMMINSIND.NS", "CYIENT.NS", "DCBBANK.NS", 
    "DEEPAKNTR.NS", "DHANUKA.NS", "DISHTV.NS", "EIDPARRY.NS", "ESCORTS.NS", 
    "EXIDEIND.NS", "FDC.NS", "FEDERALBNK.NS", "FORTIS.NS", "FSL.NS", 
    "GDL.NS", "GESHIP.NS", "GHCL.NS", "GILLETTE.NS", "GMRINFRA.NS", 
    "GNFC.NS", "GODFRYPHLP.NS", "GPPL.NS", "GRINDWELL.NS", "GSFC.NS", 
    "GUJGASLTD.NS", "HATSUN.NS", "HINDCOPPER.NS", "HINDZINC.NS", "HONAUT.NS", 
    "HUDCO.NS", "IBREALEST.NS", "IBULHSGFIN.NS", "IDBI.NS", "IDFC.NS", 
    "IFBIND.NS", "IGPL.NS", "IIFLWAM.NS", "INDIACEM.NS", "INDIAMART.NS", 
    "INEOSSTYRO.NS", "JBCHEPHARM.NS", "JINDALSAW.NS", "JISLJALEQS.NS", "JKCEMENT.NS", 
    "JKCEMENT.NS", "JKLAKSHMI.NS", "JUBLPHARMA.NS", "KAJARIACER.NS", "KALPATPOWR.NS", 
    "KEI.NS", "KIRLOSENG.NS", "KPITTECH.NS", "KRBL.NS", "LAXMIMACH.NS"]

# Define the date range
end_date = date.today() + timedelta(days=1)
start_date = end_date - timedelta(days=40)
num_periods = 20

# Calculate the start date x days before
start_date_x_days_before = get_date_x_days_before(start_date, num_periods * 2)

# Function to process stocks and return buy and sell signals
def process_stocks(stocks):
    buy_signals = {0: [], 1: [], 2: []}
    sell_signals = {0: [], 1: [], 2: []}
    failed_stocks = []

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
                # if (stock_data.loc[stock_data.index[i-1], 'Buy Signal'] == 1 ):
                 #   stock_data.loc[stock_data.index[i], 'Buy Signal'] = 0
                
                #if (stock_data.loc[stock_data.index[i-1], 'Sell Signal'] == 1 ):
                 #   stock_data.loc[stock_data.index[i], 'Sell Signal'] = 0
                

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
    
    return buy_signals, sell_signals, failed_stocks

# Streamlit app
st.title("Stock Buy and Sell Signals")

# Process each category of stocks
nifty_50_buy_signals, nifty_50_sell_signals, nifty_50_failed_stocks = process_stocks(nifty_50_stocks)
nifty_51_100_buy_signals, nifty_51_100_sell_signals, nifty_51_100_failed_stocks = process_stocks(nifty_51_100_stocks)
nifty_101_200_buy_signals, nifty_101_200_sell_signals, nifty_101_200_failed_stocks = process_stocks(nifty_101_200_stocks)

# Select the day to display signals
days = ["Today", "Yesterday", "Day Before Yesterday"]
selected_day = st.selectbox("Select the day to view signals", days)

# Determine the index based on selected day
day_index = days.index(selected_day)

# Function to display signals
def display_signals(buy_signals, sell_signals, failed_stocks, category):
    st.subheader(f"{category} Buy Signals for {selected_day}")
    if buy_signals[day_index]:
        for stock, signal_date, signal in buy_signals[day_index]:
            st.write(f"{signal_date}: {stock} - {signal}")
            chart_url = f"https://finance.yahoo.com/quote/{stock}/chart/"
            st.markdown(f"[{stock} Chart]({chart_url})")
    else:
        st.write(f"No buy signals for {selected_day}")

    st.subheader(f"{category} Sell Signals for {selected_day}")
    if sell_signals[day_index]:
        for stock, signal_date, signal in sell_signals[day_index]:
            st.write(f"{signal_date}: {stock} - {signal}")
            chart_url = f"https://finance.yahoo.com/quote/{stock}/chart/"
            st.markdown(f"[{stock} Chart]({chart_url})")
    else:
        st.write(f"No sell signals for {selected_day}")

    if failed_stocks:
        st.subheader(f"Failed to Process {category} Stocks")
        for stock in failed_stocks:
            st.write(stock)

# Display signals for each category
st.header("Nifty 50 Stocks")
display_signals(nifty_50_buy_signals, nifty_50_sell_signals, nifty_50_failed_stocks, "Nifty 50")

st.header("Nifty 51-100 Stocks")
display_signals(nifty_51_100_buy_signals, nifty_51_100_sell_signals, nifty_51_100_failed_stocks, "Nifty 51-100")

st.header("Nifty 101-200 Stocks")
display_signals(nifty_101_200_buy_signals, nifty_101_200_sell_signals, nifty_101_200_failed_stocks, "Nifty 101-200")
