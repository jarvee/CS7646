"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
def author():
    return 'jzhang950'

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
    # read csv files
    df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan']);

    # prices dataframe
    symbols = [];
    start_date = df.index.min();
    end_date = df.index.max();
    for i, row in df.iterrows():
        symbol = row['Symbol'];
        if symbol not in symbols:
            symbols.append(symbol);

    prices = get_data(symbols, pd.date_range(start_date, end_date));
    prices['Cash'] = 1.00;
    #print prices;

    # trades dataframe
    trades = pd.DataFrame(data = 0.00, index = prices.index, columns = symbols);
    trades['Cash'] = 0.00;

    for i, row in df.iterrows():
        company = row['Symbol'];
        number = row['Shares'];
        if row['Order'] == 'BUY':
                trades.ix[i, company] = trades.ix[i, company] + number;
                trades.ix[i, 'Cash'] = trades.ix[i, 'Cash'] - number * prices.ix[i, company] - commission - impact * (number * prices.ix[i, company]);
        if row['Order'] == 'SELL':
                trades.ix[i, company] = trades.ix[i, company] - number;
                trades.ix[i, 'Cash'] = trades.ix[i, 'Cash'] +  number * prices.ix[i, company] - commission - impact * (number * prices.ix[i, company]);
    #print trades;

    # holdings dataframe
    holdings = pd.DataFrame(data = 0.00, index = trades.index, columns = symbols);
    holdings['Cash'] = 0.00;
    holdings['Cash'][0] = start_val + trades['Cash'][0];
    len_symbol = len(symbols);
    length = len(prices.index);
    #for i, row in df.iterrows():
        #company = row['Symbol'];
        #number = row['Shares'];
        #holdings.ix[i:, company] = holdings.ix[i, company] + trades.ix[i, company];
        #holdings.ix[i:, 'Cash'] = holdings.ix[i, 'Cash'] + trades.ix[i, 'Cash'];

    for i in range(0, len_symbol): 
        for j in range(0, length):
            previous = holdings[symbols[i]][j - 1];
            traVal = trades[symbols[i]][j];
            holdings[symbols[i]][j] = previous + traVal;
    for i in range(1, length):
        preCash = holdings['Cash'][i - 1];
        traCash = trades['Cash'][i];
        holdings['Cash'][i] = preCash + traCash;
    #print holdings;

    # values dataFrame
    values = pd.DataFrame(data = 0.00, index = trades.index, columns = symbols);
    values['Cash'] = 0.00;
    for i, row in df.iterrows():
    	company = row['Symbol'];
        number = row['Shares'];
        values.ix[i:, company] = holdings.ix[i:, company] * prices.ix[i:, company];
        values.ix[i:, 'Cash'] = holdings.ix[i:, 'Cash'];
    #print values;

    portvals = values.sum(axis = 1);
    #print portvals;

    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-01.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
    print author()

