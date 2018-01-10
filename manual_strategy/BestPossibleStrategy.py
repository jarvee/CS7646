import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import matplotlib.pyplot as plt
import marketsimcode as ms


def author():
        return 'jzhang950'

def testPolicy(symbol = "AAPL", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000):
        symbols = [symbol];
        price = get_data(symbols, pd.date_range(sd, ed));
        prices = price.copy();
        orders = pd.DataFrame(data = 'JPM', index = prices.index, columns = ['Symbol', 'Order', 'Shares']);
        holds = 0;

        length = len(prices.index);
        for i in range(0, length-1):
                if (prices.ix[i+1, symbol] - prices.ix[i, symbol] > 0) and (holds == 0):
                        orders.ix[i, "Order"] = 'BUY';
                        orders.ix[i, "Shares"] = 1000;
                        holds = holds + orders.ix[i, "Shares"];
                elif (prices.ix[i+1, symbol] - prices.ix[i, symbol] > 0) and (holds == 1000):
                        orders.ix[i, "Order"] = 'HOLD';
                        orders.ix[i, "Shares"] = 0; 
                        holds = holds + orders.ix[i, "Shares"];
                elif (prices.ix[i+1, symbol] - prices.ix[i, symbol] > 0) and (holds == -1000):
                        orders.ix[i, "Order"] = 'BUY';
                        orders.ix[i, "Shares"] = 2000;  
                        holds = holds + orders.ix[i, "Shares"];
                elif (prices.ix[i+1, symbol] - prices.ix[i, symbol] < 0) and (holds == 0):
                        orders.ix[i, "Order"] = 'SELL';
                        orders.ix[i, "Shares"] = 1000;
                        holds = holds - orders.ix[i, "Shares"];
                elif (prices.ix[i+1, symbol] - prices.ix[i, symbol] < 0) and (holds == 1000):
                        orders.ix[i, "Order"] = 'SELL';
                        orders.ix[i, "Shares"] = 2000;
                        holds = holds - orders.ix[i, "Shares"];
                elif (prices.ix[i+1, symbol] - prices.ix[i, symbol] < 0) and (holds == -1000):
                        orders.ix[i, "Order"] = 'HOLD';
                        orders.ix[i, "Shares"] = 0;
                        holds = holds - orders.ix[i, "Shares"];
                else :
                        orders.ix[i, "Order"] = 'HOLD';

        orders = orders[orders.Order != 'HOLD'];
        orders = orders[orders.Order != 'JPM'];
        return orders
  

def test_code():
        df_trades = testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000) 
        result = ms.compute_portvals(orders = df_trades, start_val = 100000, commission = 0, impact = 0, symbols = "JPM", start_date=dt.datetime(2008,1,1), end_date=dt.datetime(2009,12,31))
        cr = result[-1] / result[0] - 1
        daily_rets = (result / result.shift(1)) - 1
        daily_rets = daily_rets[1:]
        avg_daily_ret = daily_rets.mean()
        std_daily_ret = daily_rets.std()
        sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret
        print "Cumulative Return:", cr
        print "Average Daily Return:", avg_daily_ret
        print "Standard Deviation Daily Return:", std_daily_ret

        symbols = ['JPM'];
        prices = get_data(symbols, pd.date_range(dt.datetime(2008,1,1), dt.datetime(2009,12,31)));
        orders = pd.DataFrame(data = 'JPM', index = prices.index, columns = ['Symbol', 'Order', 'Shares']);
        orders.ix[0, "Order"] = 'BUY';
        orders.ix[0, "Shares"] = 1000;
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
        df_temp = pd.concat([normed_pors, normed_bench], keys=['portvals', 'benchmark'], axis=1)
        df_temp.plot(color = ['black', 'blue'], title = "Best Possible Portfolio vs Benchamark")
        plt.show()

if __name__ == "__main__":
        test_code()
        print author()

