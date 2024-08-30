import streamlit as st
import backend.formulas as bsm
import backend.plots as plots

st.title("Plots")

# SECTION 1: P&L HEATMAP
st.header("P&L Heatmaps")
st.subheader("Underlying Price vs Volatility")
st.subheader("P&L = Adjusted Premium Price - Purchase Price")

# Inputs
s = st.session_state.s
k = st.session_state.k
r = st.session_state.r
sigma = st.session_state.sigma
t = st.session_state.t
call = round(bsm.call(s,k,r,t,sigma),2)
put = round(bsm.put(s,k,r,t,sigma),2)

call_purchase_price = st.number_input("Call Purchase Price",value=call)
put_purchase_price = st.number_input("Put Purchase Price",value=put)

col1_a, col2_a = st.columns([1,1])
with col1_a:
    price_lower = st.number_input("Underlying Price Lower Bound",value=s-25)
    price_upper = st.number_input("Underlying Price Upper Bound",value=s+25)
with col2_a:
    volatility_lower = st.number_input("Volatility Lower Bound",value=sigma-0.19)
    volatility_upper = st.number_input("Volatility Upper Bound",value=sigma+0.2)
price_bounds = (price_lower,price_upper)
volatility_bounds = (volatility_lower,volatility_upper)

with col1_a:
    st.write("Call Matrix:")
    call_matrix = plots.price_heatmap(price_bounds, volatility_bounds, call_purchase_price, k, r, t, 0)
    st.pyplot(call_matrix)

with col2_a:
    st.write("Put Matrix:")
    put_matrix = plots.price_heatmap(price_bounds, volatility_bounds, put_purchase_price, k, r, t, 1)
    st.pyplot(put_matrix)

# SECTION 2: P&L GRAPH
st.subheader("Underlying Price vs P&L")
st.subheader("P&L = max(S - K - Purchase Price, -Purchase Price)")
no_contracts = st.number_input("Number of purchased contracts",value=1)

col1_b, col2_b = st.columns([1,1])
with col1_b:
    call_pnl = plots.profit_chart(price_bounds,call_purchase_price,k,no_contracts,0)
    st.pyplot(call_pnl)
with col2_b:
    put_pnl = plots.profit_chart(price_bounds,call_purchase_price,k,no_contracts,1)
    st.pyplot(put_pnl)
