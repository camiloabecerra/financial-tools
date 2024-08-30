import streamlit as st
import backend.plots as plots
import backend.env_loading as env
import requests
import pandas as pd

popular_tickers = {
    "Apple Inc.": "AAPL",
    "Microsoft Corporation": "MSFT",
    "Amazon.com, Inc.": "AMZN",
    "Alphabet Inc. (Class A)": "GOOGL",
    "Tesla, Inc.": "TSLA",
    "NVIDIA Corporation": "NVDA",
    "Meta Platforms, Inc.": "META",
    "Berkshire Hathaway Inc. (Class B)": "BRK.B",
    "Visa Inc.": "V",
    "Johnson & Johnson": "JNJ",
    "JPMorgan Chase & Co.": "JPM",
    "Procter & Gamble Co.": "PG",
    "UnitedHealth Group Incorporated": "UNH",
    "The Home Depot, Inc.": "HD",
    "Exxon Mobil Corporation": "XOM",
    "Other":"Other"
}

st.title("Stock Quote")
ticker = st.selectbox("Select stock:", popular_tickers.keys())

if ticker == "Other":
    ticker = st.text_input("Input stock ticker:")
else:
    ticker = popular_tickers[ticker]

# Button
col1_a, col2_a = st.columns([1,1])
if "quote_get_clicked" not in st.session_state:
    st.session_state.quote_get_clicked = False
def click_quote():
    st.session_state.quote_get_clicked = True
with col1_a:
    st.button("Get Price", on_click=click_quote)

if "ts_clicked" not in st.session_state:
    st.session_state.ts_clicked = False
def click_ts():
    st.session_state.ts_clicked = True
with col2_a:
    st.button("Show time series", on_click=click_ts)

if st.session_state.quote_get_clicked:
    # API Request
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={env.api_key}"
    r = requests.get(url)
    quote = r.json()["Global Quote"]

    col1_b, col2_b = st.columns([1,1])
    with col1_b:
        st.write("Symbol:",ticker)
    with col2_b:
        st.write("Latest Trading Day:",quote["07. latest trading day"])

    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
        st.write("Open: $", round(float(quote["02. open"]),2))
        st.write("Last Close: $", round(float(quote["08. previous close"]),2))
    with col2:
        st.write("High: $", round(float(quote["03. high"]),2))
        st.write("Low: $", round(float(quote["04. low"]),2))
    with col3:
        st.write("Price: $", round(float(quote["05. price"]),2))
        st.write("Volume:", int(quote["06. volume"]))
    with col4:
        st.write("Change: $", round(float(quote["09. change"]),2))
        st.write("Change Percent:", quote["10. change percent"])

    st.session_state.quote_get_clicked = False

def get_ys(y_dicts):
    opens = []
    highs = []
    lows = []
    closes = []
    for d in y_dicts:
        opens.append(float(d["1. open"]))
        highs.append(float(d["2. high"]))
        lows.append(float(d["3. low"]))
        closes.append(float(d["4. close"]))

    return {"open":opens, "close":closes, "high":highs, "low":lows}

if st.session_state.ts_clicked:
    url_ts = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={env.api_key_2}"
    r_ts = requests.get(url_ts)
    time_series = r_ts.json()["Time Series (Daily)"]

    X = time_series.keys()
    df_data = get_ys(time_series.values())
    df_data["times"] = X
    df = pd.DataFrame(df_data).sort_values(by="times").tail(30)
    candle_plot = plots.candlestick(df, ticker)

    st.pyplot(candle_plot)

    st.session_state.ts_clicked = False
