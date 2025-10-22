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
data_folder = os.path.join(BASE_DIR, '..', 'data')  # Goes up one level to find data folder

# Check if data folder exists
if not os.path.exists(data_folder):
    st.error(f"❌ Data folder not found at: {data_folder}")
    st.info("📁 Expected structure:\n```\nEnd to End/\n├── scripts/\n│   └── app.py\n└── data/\n    └── AAPL_data_processed.csv\n```")
    st.info("Run these commands:\n```\ncd scripts\npython data_fetch.py\npython data_clean.py\n```")
    st.stop()

# Get available tickers
try:
    all_files = os.listdir(data_folder)
    tickers = [f.replace('_data_processed.csv', '') for f in all_files 
               if f.endswith('_data_processed.csv')]
    
    if not tickers:
        st.error("❌ No processed data files found.")
        st.info(f"📂 Files in data folder: {all_files}")
        st.info("Run these commands:\n```\ncd scripts\npython data_fetch.py\npython data_clean.py\n```")
        st.stop()
except Exception as e:
    st.error(f"Error reading data folder: {e}")
    st.stop()

selected_ticker = st.sidebar.selectbox("Select Ticker", sorted(tickers))
file_path = os.path.join(data_folder, f'{selected_ticker}_data_processed.csv')

if not os.path.exists(file_path):
    st.error(f"❌ Data file not found: {file_path}")
    st.stop()

df = load_data(file_path)

# Date r
start_date = st.sidebar.date_input("Start Date", df['Date'].min().date())
end_date = st.sidebar.date_input("End Date", df['Date'].max().date())
df_filtered = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

# Check if filtered data is empty
if df_filtered.empty:
    st.error("❌ No data available for the selected date range.")
    st.stop()

# Dashboard Title & KPIs (Key)
st.title(f"📈 {selected_ticker} Stock Dashboard")
latest_close = df_filtered['Close'].iloc[-1]
latest_change = df_filtered['Daily Change %'].iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Latest Close Price", f"${latest_close:.2f}")
col2.metric("Daily Change %", f"{latest_change:.2f}%", 
            delta=f"{latest_change:.2f}%")
col3.metric("Total Days", len(df_filtered))

# Close Price and Moving Averages Chart
st.subheader("📊 Close Price & Moving Averages")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['Close'], 
                         mode='lines', name='Close', line=dict(color='#00CC96', width=2)))
if 'MA_20' in df_filtered.columns:
    fig.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['MA_20'], 
                             mode='lines', name='MA 20', line=dict(color='#FFA15A', width=1.5)))
if 'MA_50' in df_filtered.columns:
    fig.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['MA_50'], 
                             mode='lines', name='MA 50', line=dict(color='#EF553B', width=1.5)))
fig.update_layout(
    xaxis_title="Date", 
    yaxis_title="Price ($)", 
    template="plotly_dark", 
    hovermode="x unified",
    height=500
)
st.plotly_chart(fig, use_container_width=True)

# Daily Changes %
st.subheader("📈 Daily Change %")
colors = ['red' if x < 0 else 'green' for x in df_filtered['Daily Change %']]
fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=df_filtered['Date'], 
    y=df_filtered['Daily Change %'], 
    name='Daily Change %',
    marker_color=colors
))
fig2.update_layout(
    xaxis_title="Date", 
    yaxis_title="Daily Change (%)", 
    template="plotly_dark", 
    hovermode="x unified",
    height=400
)
st.plotly_chart(fig2, use_container_width=True)

# Volume Charts
if 'Volume' in df_filtered.columns:
    st.subheader("📊 Trading Volume")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=df_filtered['Date'], 
        y=df_filtered['Volume'], 
        name='Volume',
        marker_color='#636EFA'
    ))
    fig3.update_layout(
        xaxis_title="Date", 
        yaxis_title="Volume", 
        template="plotly_dark",
        height=400
    )
    st.plotly_chart(fig3, use_container_width=True)

# Data Tables
with st.expander("📋 View Raw Data"):
    st.dataframe(df_filtered.tail(50), use_container_width=True)