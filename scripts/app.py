import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

st.sidebar.header("Stock Dashboard Settings")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(BASE_DIR, 'data')  # FIXED: Removed '..'

# Check if data folder exists
if not os.path.exists(data_folder):
    st.error(f"❌ Data folder not found at: {data_folder}")
    st.info("Please create a 'data' folder and run data_fetch.py and data_clean.py first.")
    st.stop()

# Get available tickers
try:
    tickers = [f.replace('_data_processed.csv', '') for f in os.listdir(data_folder) 
               if f.endswith('_data_processed.csv')]
    if not tickers:
        st.error("❌ No processed data files found.")
        st.info("Run these commands:\n1. python scripts/data_fetch.py\n2. python scripts/data_clean.py")
        st.stop()
except Exception as e:
    st.error(f"Error reading data folder: {e}")
    st.stop()

selected_ticker = st.sidebar.selectbox("Select Ticker", tickers)
file_path = os.path.join(data_folder, f'{selected_ticker}_data_processed.csv')

if not os.path.exists(file_path):
    st.error(f"❌ Data file not found: {file_path}")
    st.stop()

df = load_data(file_path)

# Date range filter
start_date = st.sidebar.date_input("Start Date", df['Date'].min())
end_date = st.sidebar.date_input("End Date", df['Date'].max())
df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

# Check if filtered data is empty
if df.empty:
    st.error("❌ No data available for the selected date range.")
    st.stop()

# Dashboard
st.title(f"📈 {selected_ticker} Stock Dashboard")
latest_close = df['Close'].iloc[-1]
latest_change = df['Daily Change %'].iloc[-1]

col1, col2 = st.columns(2)
col1.metric("Latest Close Price", f"${latest_close:.2f}")
col2.metric("Daily Change %", f"{latest_change:.2f}%")

# Charts
st.subheader("Close Price & Moving Averages")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close'))
if 'MA_20' in df.columns:
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_20'], mode='lines', name='MA 20'))
if 'MA_50' in df.columns:
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_50'], mode='lines', name='MA 50'))
fig.update_layout(xaxis_title="Date", yaxis_title="Price ($)", template="plotly_dark", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Daily Change %")
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=df['Date'], y=df['Daily Change %'], name='Daily Change %'))
fig2.update_layout(xaxis_title="Date", yaxis_title="Daily Change (%)", template="plotly_dark", hovermode="x unified")
st.plotly_chart(fig2, use_container_width=True)