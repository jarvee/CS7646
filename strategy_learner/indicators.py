"""
Jiawei Zhang
jzhang950
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import matplotlib.pyplot as plt


def author():
        return 'jzhang950'

def compute_indicators(start_date, end_date, symbols, lookback):
        price = get_data(symbols, pd.date_range(start_date, end_date))
        sma = price.rolling(window=lookback, min_periods=lookback).mean()
        bb_std = price.rolling(window=lookback, min_periods=lookback).std()
        top_band = sma + bb_std*2
        bottom_band = sma - bb_std*2
        bb = (price - bottom_band) / (top_band - bottom_band)
        sma_over = sma / price
        momentum = (price / price.shift(lookback - 1)) - 1

        return price, sma, sma_over, bb_std, top_band, bottom_band, bb, momentum
  

def test_code():
        start_date = dt.datetime(2008,01,01)
        end_date = dt.datetime(2009,12,31)
        symbols = ['JPM']
        lookback = 14

        price, sma, sma_over, bb_std, top_band, bottom_band, bb, momentum = compute_indicators(start_date, end_date, symbols, lookback)
        
        price = price.ix[:, ['JPM']]
        sma = sma.ix[:, ['JPM']]
        sma_over = sma_over.ix[:, ['JPM']]
        bb_std = bb_std.ix[:, ['JPM']]
        top_band = top_band.ix[:, ['JPM']]
        bottom_band = bottom_band.ix[:, ['JPM']]
        bb = bb.ix[:, ['JPM']]
        momentum = momentum.ix[:, ['JPM']]

        normed_price = price / price.ix[0,:]
        normed_sma = sma /sma.ix[15,:]

        df_temp = pd.concat([normed_price, normed_sma, sma_over], keys=['price', 'SMA', 'Price/SMA'], axis=1)
        df_temp.plot(title = "Simple Moving Average")

        normed_top_band = top_band / top_band.ix[15,:]
        normed_bottom_band = bottom_band / bottom_band.ix[15,:]

        df_temp = pd.concat([normed_price, bb, normed_top_band, normed_bottom_band], keys=['price', 'Bollinger Bands', 'top band', 'bottom band'], axis=1)
        df_temp.plot(title = "Bollinger Bands")

        df_temp = pd.concat([normed_price, momentum], keys=['price', 'momentum'], axis=1)
        df_temp.plot(title = "Momentum")


        plt.show()


if __name__ == "__main__":
        test_code()
        print author()

