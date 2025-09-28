
import pandas as pd
import streamlit as st
import plotly.express as px

# Load processed CSV file from data folder
data_file = 'data/AAPL_data_processed.csv'  # Update this path as needed
df = pd.read_csv(data_file)

# Title of the dashboard
st.title('Stock Market Dashboard')


st.sidebar.header('User Input Features')
ticker = st.sidebar.selectbox('Select Ticker Symbol', df['Ticker'].unique())
start_date = st.sidebar.date_input('Start Date', df['Date'].min())
end_date = st.sidebar.date_input('End Date', df['Date'].max())

# Filter data based on user input
filtered_data = df[(df['Ticker'] == ticker) & (df['Date'] >= str(start_date)) & (df['Date'] <= str(end_date))]

# Line chart for Close price over 
st.subheader('Close Price Over Time')
fig_close = px.line(filtered_data, x='Date', y='Close', title='Close Price')
st.plotly_chart(fig_close)

# Bar chart for Daily Change %
st.subheader('Daily Change %')
fig_change = px.bar(filtered_data, x='Date', y='Daily Change %', title='Daily Change %')
st.plotly_chart(fig_change)

# Optional: Moving Averages
if st.sidebar.checkbox('Show Moving Averages'):
    st.subheader('Moving Averages')
    fig_ma = px.line(filtered_data, x='Date', y=['MA_20', 'MA_50'], title='Moving Averages')
    st.plotly_chart(fig_ma)