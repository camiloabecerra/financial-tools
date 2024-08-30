import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import backend.formulas as bsm

# Prices formatting: df({"times":[], "open":[],"close":[],"high":[],"low":[]})
def candlestick(prices, ticker):
    plt.figure()
    set_color = lambda r: "green" if r["open"] <= r["close"] else "red"
    open_close_width = .3
    high_low_width = .03

    # Plotting high-lows
    plt.bar(prices["times"], height=prices["high"]-prices["low"], bottom=prices["low"], width=high_low_width,
        color=prices.apply(set_color,axis=1))

    # Plotting open-closes
    plt.bar(prices["times"], height=prices.apply(lambda r: r["close"]-r["open"] if r["open"] <= r["close"] else r["open"]-r["close"],axis=1),
        bottom=prices.apply(lambda r: r["open"] if r["open"]<=r["close"] else r["close"],axis=1),
        width=open_close_width, color=prices.apply(set_color,axis=1))

    # Formatting
    x_ticks = [prices["times"].iloc[0], prices["times"].iloc[-1]]
    plt.xticks(x_ticks)
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    plt.title(f"{ticker} Price Over Past 30 Trading Days")

    return plt

INTERVALS_PH = 7
def price_heatmap(price_bounds,volatility_bounds,purchase_price,k,r,t,call_or_put):
    premium_prices = []
    price_step = (price_bounds[1] - price_bounds[0]) / (INTERVALS_PH - 1)
    volatility_step = (volatility_bounds[1] - volatility_bounds[0]) / (INTERVALS_PH - 1)
    price_labels = []
    volatility_labels = []

    # Populate labels
    for c in range(INTERVALS_PH):
        price_labels.append(round(price_bounds[0] + (c * price_step),2))
        volatility_labels.append(round(volatility_bounds[0] + (c * volatility_step),2))
    volatility_labels.reverse()

    # Populate premium_prices
    for current_sigma in volatility_labels:
        l = []
        for current_s in price_labels:
            if call_or_put == 0: # call
                value = bsm.call(current_s,k,r,t,current_sigma)
            else: # put
                value = bsm.put(current_s,k,r,t,current_sigma)

            pnl = value - purchase_price
            l.append(round(pnl,2))
        premium_prices.append(l)

    # Create plot
    fig, ax = plt.subplots()
    norm = mcolors.TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
    im = ax.imshow(premium_prices, cmap="RdYlGn",norm=norm)

    plt.ylabel("Volatility")
    plt.xlabel("Underlying Asset Price (USD)")
    ax.set_xticks(np.arange(INTERVALS_PH), labels=map(lambda x: round(x,2),price_labels))
    ax.set_yticks(np.arange(INTERVALS_PH), labels=volatility_labels)
    for i in range(INTERVALS_PH):
        for j in range(INTERVALS_PH):
            text = ax.text(j, i, premium_prices[i][j], ha="center", va="center", color="w")

    return plt


INTERVALS_PC = 10
def profit_chart(price_bounds, purchase_price, exercise_price, no_contracts, call_or_put):
    def profit_formula(s):
        if call_or_put == 0: # call
            return max(s - exercise_price - purchase_price, -purchase_price) * no_contracts
        else: # put
            return max(exercise_price - s - purchase_price, -purchase_price) * no_contracts

    price_labels = []
    pnl = []
    price_step = (price_bounds[1] - price_bounds[0]) / (INTERVALS_PC - 1)
    # Populate labels
    for c in range(INTERVALS_PC):
        price_labels.append(round(price_bounds[0] + (c * price_step),2))
        pnl.append(profit_formula(price_labels[c]))

    # Create plot
    plt.figure()
    plt.xlabel("Underlying Asset Price (USD)")
    plt.ylabel("Profit/Loss (USD)")
    plt.xticks([price_bounds[0], price_bounds[1]])
    plt.yticks([pnl[0], 0, pnl[-1]])
    plt.plot(price_labels,pnl)
    plt.plot(price_labels,[0]*INTERVALS_PC,color="red")
    return plt
