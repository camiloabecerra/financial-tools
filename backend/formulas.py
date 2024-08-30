import numpy as np
from scipy.stats import norm
import math
import sys

def d1(s, k, r, t, sigma):
    return (np.log(s/k) + (r + (sigma ** 2) / 2) * t) / (sigma * math.sqrt(t))

def d2(s, k, r, t, sigma):
    return d1(s, k, r, t, sigma) - sigma * math.sqrt(t)

def call(s=100, k=105, r=0.05, t=1, sigma=0.2):
    return norm.cdf(d1(s,k,r,t,sigma)) * s - norm.cdf(d2(s,k,r,t,sigma)) * k * math.e ** (-r * t)

def put(s=100, k=105, r=0.05, t=1, sigma=0.2):
    return norm.cdf(-d2(s,k,r,t,sigma)) * k * math.e ** (-r * t) - norm.cdf(-d1(s,k,r,t,sigma)) * s

def nr_step(f, x0):
    def derivative_est(x):
        dx = 0.0000000000001
        return (f(x + dx) - f(x)) / dx
    return x0 - f(x0) / derivative_est(x0)

def implied_volatility(market_price, s=100, k=105, r=0.05, t=1):
    diff = lambda sigma: call(s,k,r,t,sigma) - market_price

    iv = 0.2
    while abs(diff(iv)) > 10 ** -6:
        iv = nr_step(diff, iv)
    return iv

# Rate of change of option premium vs underlying price
def delta(s=100, k=105, r=0.05, t=1, sigma=0.2, call_or_put=0):
    n = norm.cdf(d1(s,k,r,t,sigma))
    if call_or_put == 0: # call
        return n
    else: # put
        return n - 1

# Rate of change of delta vs underlying price
def gamma(s=100, k=105, r=0.05, t=1, sigma=0.2):
    return norm.pdf(d1(s,k,r,t,sigma)) / (s * sigma * math.sqrt(t))

# Time decay: rate of change of option premium vs time
def theta(s=100, k=105, r=0.05, t=1, sigma=0.2, call_or_put=0):
    term1 = -(s * norm.pdf(d1(s,k,r,t,sigma)) * sigma) / (2 * math.sqrt(t))
    if call_or_put == 0: # call
        term2 = -(r * k * norm.cdf(d2(s,k,r,t,sigma)) * math.e ** (-r * t))
    else: # put
        term2 = r * k * norm.cdf(-d2(s,k,r,t,sigma)) * math.e ** (-r * t)

    return term1 + term2

# Rate of change of option premium vs risk free rate
def rho(s=100, k=105, r=0.05, t=1, sigma=0.2, call_or_put=0):
    if call_or_put == 0: # call
        return k * t * norm.cdf(d2(s,k,r,t,sigma)) * math.e ** (-r * t)
    else: # put
        return -(k * t * norm.cdf(-d2(s,k,r,t,sigma)) * math.e ** (-r * t))

# Rate of change of option premium vs volatility
def vega(s=100, k=105, r=0.05, t=1, sigma=0.2):
    return s * math.sqrt(t) * norm.pdf(d1(s,k,r,t,sigma))
