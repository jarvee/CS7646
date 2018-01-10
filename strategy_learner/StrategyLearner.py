"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""
"""
Jiawei Zhang
jzhang950
"""

import datetime as dt
import pandas as pd
import util as ut
import random
import QLearner as ql
import numpy as np

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 

        # add your code to do learning here

        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose: print prices
  
        # example use with new colname 
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        volume = volume_all[syms]  # only portfolio symbols
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later
        if self.verbose: print volume

        # calculate the indicators.py to get the state
        price = prices_all
        lookback = 14
        sma = price.rolling(window=lookback, min_periods=lookback).mean()
        bb_std = price.rolling(window=lookback, min_periods=lookback).std()
        top_band = sma + bb_std*2
        bottom_band = sma - bb_std*2
        bb = (price - bottom_band) / (top_band - bottom_band)
        sma_over = sma / price
        momentum = (price / price.shift(lookback - 1)) - 1

        price = price.ix[:, syms]
        sma = sma.ix[:, syms]
        sma_over = sma_over.ix[:, syms]
        bb_std = bb_std.ix[:, syms]
        top_band = top_band.ix[:, syms]
        bottom_band = bottom_band.ix[:, syms]
        bb = bb.ix[:, syms]
        momentum = momentum.ix[:, syms]

        sma_over = sma_over.fillna(method='bfill')
        bb = bb.fillna(method='bfill')
        momentum = momentum.fillna(method='bfill')
        indicator = pd.concat([sma_over, momentum, bb], keys=['sma_over', 'momentum', 'bb'], axis=1)
        state = indicator['sma_over'] * 100 + indicator['momentum'] * 10 + indicator['bb']
        #print state
        
        # set up the Q_frame to train the Qlearner
        self.learner = ql.QLearner(num_states= 1000, num_actions = 3, alpha = 0.2, gamma = 0.9, rar = 0.5, radr = 0.99, dyna = 0, verbose = False)
        Q_frame = pd.DataFrame(data = 0.00, index = price.index, columns = ['Hold', 'Price', 'Cash', 'Portfolio']);
        Q_frame.ix[:, 'Price'] = price.ix[:, syms]
        Q_frame['Cash'][0] = sv
        Q_frame['Portfolio'][0] = sv
        state = state.astype(int)
        for i in range (0, 13):
            s = state.ix[0, syms]
            a = self.learner.querysetstate(s)
            holding = 0
            for j in range (1, state.size):
                number = np.absolute(Q_frame.ix[j, 'Hold'])
                rate = Q_frame.ix[j, 'Price']
                if holding == 0 and a == 1:
                    holding = 1
                    Q_frame.ix[j, 'Hold'] = -1000
                    Q_frame.ix[j, 'Cash'] = Q_frame.ix[j-1, 'Cash'] - Q_frame.ix[j, 'Price'] * Q_frame.ix[j, 'Hold'] - self.impact * (number * rate)
                elif holding == 0 and a == 2:
                    holding = 2
                    Q_frame.ix[j, 'Hold'] = 1000
                    Q_frame.ix[j, 'Cash'] = Q_frame.ix[j-1, 'Cash'] - Q_frame.ix[j, 'Price'] * Q_frame.ix[j, 'Hold'] - self.impact * (number * rate)
                elif holding == 1 and a == 2:
                    holding = 2
                    Q_frame.ix[j, 'Hold'] = 1000
                    Q_frame.ix[j, 'Cash'] = Q_frame.ix[j-1, 'Cash'] - Q_frame.ix[j, 'Price'] * Q_frame.ix[j, 'Hold'] * 2 - self.impact * (2 * number * rate)
                elif holding == 2 and a == 1:
                    holding = 1
                    Q_frame.ix[j, 'Hold'] = -1000
                    Q_frame.ix[j, 'Cash'] = Q_frame.ix[j-1, 'Cash'] - Q_frame.ix[j, 'Price'] * Q_frame.ix[j, 'Hold'] * 2 - self.impact * (2 * number * rate)
                else:
                    Q_frame.ix[j, 'Hold'] = Q_frame.ix[j-1, 'Hold']
                    Q_frame.ix[j, 'Cash'] = Q_frame.ix[j-1, 'Cash']

                Q_frame.ix[j, 'Portfolio'] = Q_frame.ix[j, 'Cash'] + Q_frame.ix[j, 'Price'] * Q_frame.ix[j, 'Hold']
                reward = Q_frame.ix[j, 'Portfolio'] / Q_frame.ix[j-1, 'Portfolio'] - 1
                s = state.ix[j, syms]
                a = self.learner.query(s, reward)

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # here we build a fake set of trades
        # your code should return the same sort of data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        trades = prices_all[[symbol,]]  # only portfolio symbols
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later
        
        if self.verbose: print trades
        if self.verbose: print prices_all

        # calculate the indicators.py to get the state
        syms = [symbol]
        price = prices_all
        lookback = 14
        sma = price.rolling(window=lookback, min_periods=lookback).mean()
        bb_std = price.rolling(window=lookback, min_periods=lookback).std()
        top_band = sma + bb_std*2
        bottom_band = sma - bb_std*2
        bb = (price - bottom_band) / (top_band - bottom_band)
        sma_over = sma / price
        momentum = (price / price.shift(lookback - 1)) - 1

        price = price.ix[:, syms]
        sma = sma.ix[:, syms]
        sma_over = sma_over.ix[:, syms]
        bb_std = bb_std.ix[:, syms]
        top_band = top_band.ix[:, syms]
        bottom_band = bottom_band.ix[:, syms]
        bb = bb.ix[:, syms]
        momentum = momentum.ix[:, syms]
        sma_over = sma_over.fillna(method='bfill')
        bb = bb.fillna(method='bfill')
        momentum = momentum.fillna(method='bfill')
        indicator = pd.concat([sma_over, momentum, bb], keys=['sma_over', 'momentum', 'bb'], axis=1)
        state = indicator['sma_over'] * 100 + indicator['momentum'] * 10 + indicator['bb']
        state = state.astype(int)

        # construct a trades dataframe for record shares
        trades = pd.DataFrame(data = 0, index = prices_all.index, columns = ['value']);

        # start hold = 0, decide buy or sell depends on holdings
        holding = 0
        for i in range(1, state.size):
            s = state.ix[i-1, [symbol]]
            a = self.learner.querysetstate(s)
            if holding == 0 and a == 1:
                holding = 1
                trades.ix[i, 'value'] = -1000
            elif holding == 0 and a == 2:
                holding = 2
                trades.ix[i, 'value'] = 1000
            elif holding == 2 and a == 1:
                holding = 1
                trades.ix[i, 'value'] = -2000
            elif holding == 1 and a == 2:
                holding = 2
                trades.ix[i, 'value'] = 2000
            else:
                holding = holding

        return trades

    def author():
        return 'jzhang950'

if __name__=="__main__":
    print "One does not simply think up a strategy"
    print author()
    learner = StrategyLearner(verbose = False, impact=0.0)
    learner.addEvidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
    learner.testPolicy(symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000)