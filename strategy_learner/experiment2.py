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
import marketsimcode as ms
import indicators as ind
import StrategyLearner as sl
import ManualStrategy as man


def author():
        return 'jzhang950'

def test_code():
        # Strategy Learner plots for JPM in sample and benchmark no impact
        learner1 = sl.StrategyLearner(verbose=False,impact=0)
        learner1.addEvidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
        frame1 = learner1.testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
        # change the format of the result of the strategy learner to make as input for marketsim
        Qframe1 = pd.DataFrame(index = frame1.index, columns = ['Symbol', 'Order', 'Shares']);
        Qframe1.ix[0:, 'Symbol'] = "JPM"
        for i in range (0, len(frame1)):
                if frame1.ix[i, 'value'] < 0:
                        Qframe1.ix[i, 'Order'] = "SELL"
                        Qframe1.ix[i, 'Shares'] = np.absolute(frame1.ix[i, 'value'])
                else:
                        Qframe1.ix[i, 'Order'] = "BUY"
                        Qframe1.ix[i, 'Shares'] = np.absolute(frame1.ix[i, 'value'])
        Qframe1 = Qframe1[Qframe1.Shares != 0]

        # use marketsim to calculate portfolio and compare to plot with benchmark
        goal1 = ms.compute_portvals(orders = Qframe1, start_val = 100000, commission = 0, impact = 0, symbols = "JPM", start_date=dt.datetime(2008,1,1), end_date=dt.datetime(2009,12,31))
        goal1 = goal1[goal1 != 0];
        cr = goal1[-1] / goal1[0] - 1
        daily_rets = (goal1 / goal1.shift(1)) - 1
        daily_rets = daily_rets[1:]
        avg_daily_ret = daily_rets.mean()
        std_daily_ret = daily_rets.std()
        sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret
        print "Cumulative Return:", cr
        print "Average Daily Return:", avg_daily_ret
        print "Standard Deviation Daily Return:", std_daily_ret


        # Strategy Learner plots for JPM in sample and benchmark, impact = 0.005
        learner2 = sl.StrategyLearner(verbose=False,impact=0.2)
        learner2.addEvidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
        frame2 = learner2.testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
        # change the format of the result of the strategy learner to make as input for marketsim
        Qframe2 = pd.DataFrame(index = frame2.index, columns = ['Symbol', 'Order', 'Shares']);
        Qframe2.ix[0:, 'Symbol'] = "JPM"
        for i in range (0, len(frame2)):
                if frame2.ix[i, 'value'] < 0:
                        Qframe2.ix[i, 'Order'] = "SELL"
                        Qframe2.ix[i, 'Shares'] = np.absolute(frame2.ix[i, 'value'])
                else:
                        Qframe2.ix[i, 'Order'] = "BUY"
                        Qframe2.ix[i, 'Shares'] = np.absolute(frame2.ix[i, 'value'])
        Qframe2 = Qframe2[Qframe2.Shares != 0]

        # use marketsim to calculate portfolio and compare to plot with benchmark
        goal2 = ms.compute_portvals(orders = Qframe2, start_val = 100000, commission = 0, impact = 0, symbols = "JPM", start_date=dt.datetime(2008,1,1), end_date=dt.datetime(2009,12,31))
        goal2 = goal2[goal2 != 0];
        cr = goal2[-1] / goal2[0] - 1
        daily_rets = (goal2 / goal2.shift(1)) - 1
        daily_rets = daily_rets[1:]
        avg_daily_ret = daily_rets.mean()
        std_daily_ret = daily_rets.std()
        sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret
        print "Cumulative Return:", cr
        print "Average Daily Return:", avg_daily_ret
        print "Standard Deviation Daily Return:", std_daily_ret


        # Strategy Learner plots for JPM in sample and benchmark, impact = 0.008
        learner3 = sl.StrategyLearner(verbose=False,impact=0.4)
        learner3.addEvidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
        frame3 = learner3.testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
        # change the format of the result of the strategy learner to make as input for marketsim
        Qframe3 = pd.DataFrame(index = frame3.index, columns = ['Symbol', 'Order', 'Shares']);
        Qframe3.ix[0:, 'Symbol'] = "JPM"
        for i in range (0, len(frame3)):
                if frame3.ix[i, 'value'] < 0:
                        Qframe3.ix[i, 'Order'] = "SELL"
                        Qframe3.ix[i, 'Shares'] = np.absolute(frame3.ix[i, 'value'])
                else:
                        Qframe3.ix[i, 'Order'] = "BUY"
                        Qframe3.ix[i, 'Shares'] = np.absolute(frame3.ix[i, 'value'])
        Qframe3 = Qframe3[Qframe3.Shares != 0]

        # use marketsim to calculate portfolio and compare to plot with benchmark
        goal3 = ms.compute_portvals(orders = Qframe3, start_val = 100000, commission = 0, impact = 0, symbols = "JPM", start_date=dt.datetime(2008,1,1), end_date=dt.datetime(2009,12,31))
        goal3 = goal3[goal3 != 0];
        cr = goal3[-1] / goal3[0] - 1
        daily_rets = (goal3 / goal3.shift(1)) - 1
        daily_rets = daily_rets[1:]
        avg_daily_ret = daily_rets.mean()
        std_daily_ret = daily_rets.std()
        sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret
        print "Cumulative Return:", cr
        print "Average Daily Return:", avg_daily_ret
        print "Standard Deviation Daily Return:", std_daily_ret

        # Strategy Learner plots for JPM in sample and benchmark, impact = 0.01
        learner4 = sl.StrategyLearner(verbose=False,impact=0.6)
        learner4.addEvidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
        frame4 = learner4.testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
        # change the format of the result of the strategy learner to make as input for marketsim
        Qframe4 = pd.DataFrame(index = frame4.index, columns = ['Symbol', 'Order', 'Shares']);
        Qframe4.ix[0:, 'Symbol'] = "JPM"
        for i in range (0, len(frame4)):
                if frame4.ix[i, 'value'] < 0:
                        Qframe4.ix[i, 'Order'] = "SELL"
                        Qframe4.ix[i, 'Shares'] = np.absolute(frame4.ix[i, 'value'])
                else:
                        Qframe4.ix[i, 'Order'] = "BUY"
                        Qframe4.ix[i, 'Shares'] = np.absolute(frame4.ix[i, 'value'])
        Qframe4 = Qframe4[Qframe4.Shares != 0]

        # use marketsim to calculate portfolio and compare to plot with benchmark
        goal4 = ms.compute_portvals(orders = Qframe4, start_val = 100000, commission = 0, impact = 0, symbols = "JPM", start_date=dt.datetime(2008,1,1), end_date=dt.datetime(2009,12,31))
        goal4 = goal4[goal4 != 0];
        cr = goal4[-1] / goal4[0] - 1
        daily_rets = (goal4 / goal4.shift(1)) - 1
        daily_rets = daily_rets[1:]
        avg_daily_ret = daily_rets.mean()
        std_daily_ret = daily_rets.std()
        sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret
        print "Cumulative Return:", cr
        print "Average Daily Return:", avg_daily_ret
        print "Standard Deviation Daily Return:", std_daily_ret



        # plot for StrategyLeaner
        normed_Q1 = goal1 / goal1.ix[0,:]
        normed_Q2 = goal2 / goal2.ix[0,:]
        normed_Q3 = goal3 / goal3.ix[0,:]
        normed_Q4 = goal4 / goal4.ix[0,:]
        df_temp = pd.concat([normed_Q1, normed_Q2, normed_Q3, normed_Q4], keys=['impact = 0', 'impact = 0.2', 'impact = 0.4', 'impact = 0.6'], axis=1)
        ax = df_temp.plot(color = ['black', 'blue', 'green', 'red'], title = "Impact Test for JPM")

        plt.show()

if __name__ == "__main__":
        test_code()
        print author()

