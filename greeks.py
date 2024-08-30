import streamlit as st
import backend.formulas as bsm

st.title("Option Greeks")
col1, col2 = st.columns([1,1])

# Inputs
s = st.session_state.s
k = st.session_state.k
r = st.session_state.r
sigma = st.session_state.sigma
t = st.session_state.t

c_delta = round(bsm.delta(s,k,r,t,sigma,0),3)
c_gamma = round(bsm.gamma(s,k,r,t,sigma),3)
c_theta = round(bsm.theta(s,k,r,t,sigma,0),3)
c_rho = round(bsm.rho(s,k,r,t,sigma,0),3)
c_vega = round(bsm.vega(s,k,r,t,sigma),3)
with col1:
    st.subheader("Call Option Greeks")
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
    st.subheader("Put Option Greeks")
    st.write("Delta:",p_delta)
    st.write("Gamma:",p_gamma)
    st.write("Theta:",p_theta)
    st.write("Rho:",p_rho)
    st.write("Vega:",p_vega)
