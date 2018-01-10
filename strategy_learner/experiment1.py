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
        # Manual Strategy plots for JPM in sample and benchmark
        df_trades = man.testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
        result = ms.compute_portvals(orders = df_trades, start_val = 100000, commission = 0, impact = 0, symbols = "JPM", start_date=dt.datetime(2008,1,1), end_date=dt.datetime(2009,12,31))
        result = result[result != 0];
        cr = result[-1] / result[0] - 1
        daily_rets = (result / result.shift(1)) - 1
        daily_rets = daily_rets[1:]
        avg_daily_ret = daily_rets.mean()
        std_daily_ret = daily_rets.std()
        sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret
        print "Cumulative Return:", cr
        print "Average Daily Return:", avg_daily_ret
        print "Standard Deviation Daily Return:", std_daily_ret

        # benchmark for BestStrategy
        symbols = ['JPM'];
        prices = get_data(symbols, pd.date_range(dt.datetime(2008,1,1), dt.datetime(2009,12,31)));
        orders = pd.DataFrame(data = 'JPM', index = prices.index, columns = ['Symbol', 'Order', 'Shares']);
        orders.ix[0, "Order"] = 'BUY';
        orders.ix[0, "Shares"] = 1000;
        orders.ix[-1, "Order"] = 'SELL';
        orders.ix[-1, "Shares"] = 1000;
        orders = orders[orders.Order != 'HOLD'];
        orders = orders[orders.Order != 'JPM'];
        benchmark = ms.compute_portvals(orders = orders, start_val = 100000, commission = 0, impact = 0, symbols = "JPM", start_date=dt.datetime(2008,1,1), end_date=dt.datetime(2009,12,31))
        cr = benchmark[-1] / benchmark[0] - 1
        daily_rets = (benchmark / benchmark.shift(1)) - 1
        daily_rets = daily_rets[1:]
        avg_daily_ret = daily_rets.mean()
        std_daily_ret = daily_rets.std()
        sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret
        print "Cumulative Return:", cr
        print "Average Daily Return:", avg_daily_ret
        print "Standard Deviation Daily Return:", std_daily_ret

        normed_pors = result / result.ix[0,:]
        normed_bench = benchmark / benchmark.ix[0,:]

        # plot for BestStrategy
        df_temp = pd.concat([normed_pors, normed_bench], keys=['portvals', 'benchmark'], axis=1)
        ax = df_temp.plot(color = ['black', 'blue'], title = "Best Possible Portfolio vs Benchamark for JPM")


        # Strategy Learner plots for JPM in sample and benchmark
        learner = sl.StrategyLearner(verbose=False,impact=0)
        learner.addEvidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
        frame = learner.testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)

        # change the format of the result of the strategy learner to make as input for marketsim
        Qframe = pd.DataFrame(index = frame.index, columns = ['Symbol', 'Order', 'Shares']);
        Qframe.ix[0:, 'Symbol'] = "JPM"
        for i in range (0, len(frame)):
                if frame.ix[i, 'value'] < 0:
                        Qframe.ix[i, 'Order'] = 'SELL'
                        Qframe.ix[i, 'Shares'] = np.absolute(frame.ix[i, 'value'])
                else:
                        Qframe.ix[i, 'Order'] = 'BUY'
                        Qframe.ix[i, 'Shares'] = np.absolute(frame.ix[i, 'value'])
        Qframe = Qframe[Qframe.Shares != 0]

        # use marketsim to calculate portfolio and compare to plot with benchmark
        Qresult = ms.compute_portvals(orders = Qframe, start_val = 100000, commission = 0, impact = 0, symbols = "JPM", start_date=dt.datetime(2008,1,1), end_date=dt.datetime(2009,12,31))
        Qresult = Qresult[Qresult != 0];
        cr = Qresult[-1] / Qresult[0] - 1
        daily_rets = (Qresult / Qresult.shift(1)) - 1
        daily_rets = daily_rets[1:]
        avg_daily_ret = daily_rets.mean()
        std_daily_ret = daily_rets.std()
        sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret
        print "Cumulative Return:", cr
        print "Average Daily Return:", avg_daily_ret
        print "Standard Deviation Daily Return:", std_daily_ret

        # plot for StrategyLeaner
        normed_Q = Qresult / Qresult.ix[0,:]
        df_temp2 = pd.concat([normed_Q, normed_bench], keys=['portvals', 'benchmark'], axis=1)
        ax = df_temp2.plot(color = ['black', 'blue'], title = "StrategyLearner Portfolio vs Benchamark for JPM")

        plt.show()

if __name__ == "__main__":
        test_code()
        print author()

