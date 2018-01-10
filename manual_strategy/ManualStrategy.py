import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import matplotlib.pyplot as plt
import marketsimcode as ms
import indicators as ind


def author():
        return 'jzhang950'

def testPolicy(symbol = "AAPL", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000):
        symbols = [symbol];
        prices, sma, sma_over, bb_std, top_band, bottom_band, bb, momentum = ind.compute_indicators(start_date = sd, end_date = ed, symbols = symbols, lookback = 14);        prices = prices.ix[:, ['JPM']];
        sma = sma.ix[:, ['JPM']];
        sma_over = sma_over.ix[:, ['JPM']];
        bb_std = bb_std.ix[:, ['JPM']];
        top_band = top_band.ix[:, ['JPM']];
        bottom_band = bottom_band.ix[:, ['JPM']];
        bb = bb.ix[:, ['JPM']];
        momentum = momentum.ix[:, ['JPM']];

        orders = prices.copy();
        orders.ix[:, :] = np.NaN;

        sma_cross = pd.DataFrame(0, index=sma_over.index, columns=sma_over.columns);
        sma_cross[sma_over >= 1] = 1;
        sma_cross[1:] = sma_cross.diff();
        sma_cross.ix[0] = 0;


        orders[(sma_over < 0.85)] = 1;
        orders[(sma_over > 1.25)] = -1;
        orders[(bb < -0.4)] = 1;
        orders[(bb > 1.4)] = -1;
        orders[(momentum < -0.03)] = 1;
        orders[(momentum > 0.08)] = -1;

        orders[(sma_cross != 0)] = 0;

        orders.ffill(inplace=True);
        orders.fillna(0, inplace=True);

        orders[1:] = orders.diff();
        orders.ix[0] = 0;

        order_list = pd.DataFrame(data = 'JPM', index = orders.index, columns = ['Symbol', 'Order', 'Shares']);
        holds = 0;

        length = len(prices.index);
        for i in range(0, length-1):
                if (orders.ix[i, 'JPM'] > 0) and (holds == 0):
                        order_list.ix[i, "Order"] = 'BUY';
                        order_list.ix[i, "Shares"] = 1000;
                        holds = holds + order_list.ix[i, "Shares"];
                elif (orders.ix[i, 'JPM'] > 0) and (holds == 1000):
                        order_list.ix[i, "Order"] = 'HOLD';
                        order_list.ix[i, "Shares"] = 0; 
                        holds = holds + order_list.ix[i, "Shares"];
                elif (orders.ix[i, 'JPM'] > 0) and (holds == -1000):
                        order_list.ix[i, "Order"] = 'BUY';
                        order_list.ix[i, "Shares"] = 2000;  
                        holds = holds + order_list.ix[i, "Shares"];
                elif (orders.ix[i, 'JPM'] < 0) and (holds == 0):
                        order_list.ix[i, "Order"] = 'SELL';
                        order_list.ix[i, "Shares"] = 1000;
                        holds = holds - order_list.ix[i, "Shares"];
                elif (orders.ix[i, 'JPM'] < 0) and (holds == 1000):
                        order_list.ix[i, "Order"] = 'SELL';
                        order_list.ix[i, "Shares"] = 2000;
                        holds = holds - order_list.ix[i, "Shares"];
                elif (orders.ix[i, 'JPM'] < 0) and (holds == -1000):
                        order_list.ix[i, "Order"] = 'HOLD';
                        order_list.ix[i, "Shares"] = 0;
                        holds = holds - order_list.ix[i, "Shares"];
                else :
                        order_list.ix[i, "Order"] = 'HOLD';

        order_list = order_list[order_list.Order != 'HOLD'];
        order_list = order_list[order_list.Order != 'JPM'];
        return order_list

  

def test_code():
        df_trades = testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
        result = ms.compute_portvals(orders = df_trades, start_val = 100000, commission = 9.95, impact = 0.005, symbols = "JPM", start_date=dt.datetime(2008,1,1), end_date=dt.datetime(2009,12,31))
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

        symbols = ['JPM'];
        prices = get_data(symbols, pd.date_range(dt.datetime(2008,1,1), dt.datetime(2009,12,31)));
        orders = pd.DataFrame(data = 'JPM', index = prices.index, columns = ['Symbol', 'Order', 'Shares']);
        orders.ix[0, "Order"] = 'BUY';
        orders.ix[0, "Shares"] = 1000;
        orders = orders[orders.Order != 'HOLD'];
        orders = orders[orders.Order != 'JPM'];
        benchmark = ms.compute_portvals(orders = orders, start_val = 100000, commission = 9.95, impact = 0.005, symbols = "JPM", start_date=dt.datetime(2008,1,1), end_date=dt.datetime(2009,12,31))
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
        ax = df_temp.plot(color = ['black', 'blue'], title = "Best Possible Portfolio vs Benchamark")

        long_entry = []
        short_entry = []
        length = len(df_trades);
        for i in range(0, length):
            if df_trades.ix[i, 'Order'] == 'BUY':
                long_entry.append(df_trades.index[i])
            elif df_trades.ix[i, 'Order'] == 'SELL':
                short_entry.append(df_trades.index[i])

        for xp in long_entry:
            ax.axvline(x=xp, color='green', linestyle='-')
        for xp in short_entry:
            ax.axvline(x=xp, color='red', linestyle='-')
        plt.show()


if __name__ == "__main__":
        test_code()
        print author()

