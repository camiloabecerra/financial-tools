import streamlit as st
import pandas as pd
import backend.formulas as bsm
import backend.plots as plots

st.title("Black-Scholes Model Tools")
st.header("Option Prices and Greeks")
col1, col2  = st.columns([1,1])

# Inputs
s = st.session_state.s
k = st.session_state.k
r = st.session_state.r
sigma = st.session_state.sigma
t = st.session_state.t


# SECTION 1: PRICES AND GREEKS
call = round(bsm.call(s,k,r,t,sigma),2)
with col1:
    st.write("Call: $",call)

put = round(bsm.put(s,k,r,t,sigma),2)
with col2:
    st.write("Put: $",put)

c_delta = round(bsm.delta(s,k,r,t,sigma,0),3)
c_gamma = round(bsm.gamma(s,k,r,t,sigma),3)
c_theta = round(bsm.theta(s,k,r,t,sigma,0),3)
c_rho = round(bsm.rho(s,k,r,t,sigma,0),3)
c_vega = round(bsm.vega(s,k,r,t,sigma),3)
with col1:
    st.write("Delta:",c_delta)
    st.write("Gamma:",c_gamma)
    st.write("Theta:",c_theta)
    st.write("Rho:",c_rho)
    st.write("Vega:",c_vega)

p_delta = round(bsm.delta(s,k,r,t,sigma,1),3)
p_gamma = round(bsm.gamma(s,k,r,t,sigma),3)
p_theta = round(bsm.theta(s,k,r,t,sigma,1),3)
p_rho = round(bsm.rho(s,k,r,t,sigma,1),3)
p_vega = round(bsm.vega(s,k,r,t,sigma),3)
with col2:
    st.write("Delta:",p_delta)
    st.write("Gamma:",p_gamma)
    st.write("Theta:",p_theta)
    st.write("Rho:",p_rho)
    st.write("Vega:",p_vega)


# SECTION 2: IMPLIED VOLATILITY CALCULATOR
st.header("Implied Volatility Calculator")
mkt = st.number_input("Market Price for Call Option",value=call)
iv = round(bsm.implied_volatility(mkt,s,k,r,t),3)
st.write("Implied Volatility:", iv)
