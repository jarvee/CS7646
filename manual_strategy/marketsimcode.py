"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
def author():
    return 'jzhang950'

def compute_portvals(orders = file, start_val = 1000000, commission=9.95, impact=0.005, symbols = "JPM", start_date=dt.datetime(2008,1,1), end_date=dt.datetime(2009,12,31)):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
    # read csv files

    df = orders;
    symbols = [symbols];
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


