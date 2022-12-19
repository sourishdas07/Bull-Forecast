import streamlit as st
import pandas as pd
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from streamlit_option_menu import option_menu
from datetime import timedelta, datetime

st.title("Crypto Bull")

# Styling
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)


# Backend
START = datetime.strftime((datetime.now() - timedelta(1000)), '%Y-%m-%d')
TODAY = date.today().strftime("%Y-%m-%d")

# Crypto Sample - Add More in Future
coins = ('ADA-CAD', 'BNB-CAD', 'BTC-CAD', 'DAI-CAD', 'DOGE-CAD', 'DOT-CAD',
         'ETH-CAD', 'MATIC-CAD', 'LTC-CAD', 'SOL-CAD', 'SHIB-CAD',
         'USDT-CAD', 'USDC-CAD', 'XRP-CAD')

selected_coin = st.selectbox("Select A Stock", coins)

n_months = st.slider("Months of prediction: ", 1, 24)  # Changed Years to Months
period = n_months * 30

@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data = load_data(selected_coin)

st.subheader('Raw data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text="Time Series Data",
                      xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Predict Forecast with Prophet
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and Plot Forecast
st.subheader('Forecast Data')
st.write(forecast.tail())

st.write('Forecast Data')
forecast_graph = plot_plotly(m, forecast)
st.plotly_chart(forecast_graph)

st.write('Forecast Components')
fig2 = m.plot_components(forecast)
st.write(fig2)
