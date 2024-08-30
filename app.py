import streamlit as st

# Pages
pricing = st.Page("pricer.py", title="Prices", icon=":material/functions:")
# greeks = st.Page("greeks.py", title="Greeks", icon=":material/functions:")
plotting = st.Page("plotter.py", title="Plots", icon=":material/finance:")
quotes = st.Page("quotes.py", title="Quotes", icon=":material/attach_money:")
pg = st.navigation({"Tools":[pricing,plotting,quotes]})

with st.sidebar:
    s = st.number_input("Underlying Stock Price (S)",value=100.00)
    k = st.number_input("Strike Price (K)",value=105.00)
    r = st.number_input("Risk Free Rate (r)",value=0.05)
    sigma = st.number_input("Volatility (σ)",value=0.20)
    t = st.number_input("Years to maturity (T)",value=1.00)

st.session_state.s = s
st.session_state.k = k
st.session_state.r = r
st.session_state.sigma = sigma
st.session_state.t = t

pg.run()
