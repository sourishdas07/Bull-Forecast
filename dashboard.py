import streamlit as st
from streamlit_option_menu import option_menu
import yfinance as yf
import pandas as pd
from datetime import date
from datetime import timedelta, datetime


# Styling
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    selected = option_menu(
        menu_title= "",
        options = ["performance overview", "relative returns"],
    )


if selected == "performance overview":

    st.title("Performance Overview")

    start_date = st.date_input('Start', value = pd.to_datetime('2021-01-01'))
    end_date = st.date_input('End', value = pd.to_datetime('today'))

    indicators = ('Relative Return', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume')
    selected_indicator = st.multiselect("Select An Indicator", indicators)

    df = pd.read_excel('company_list.xlsx')
    tickers = df['Symbol'].values.tolist()
    dropdown = st.multiselect("Select A Stock", tickers)

    if len(dropdown) > 0:
        df = yf.download(dropdown, start_date, end_date)[selected_indicator]
        st.line_chart(df)

        
if selected == "relative returns":

    st.title("Relative Returns")

    start_date = st.date_input('Start', value = pd.to_datetime('2021-01-01'))
    end_date = st.date_input('End', value = pd.to_datetime('today'))

    df = pd.read_excel('company_list.xlsx')
    tickers = df['Symbol'].values.tolist()
    dropdown = st.multiselect("Select A Stock", tickers)

    # Relative Return
    def relativeret(df):
        rel = df.pct_change()
        cumret = (1 + rel).cumprod() - 1
        cumret = cumret.fillna(0)
        return cumret

    if len(dropdown) > 0:
        df = relativeret(yf.download(dropdown, start_date, end_date)['Adj Close'])
        st.line_chart(df)

        



    

    
