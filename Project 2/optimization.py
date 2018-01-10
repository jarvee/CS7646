"""MC1-P2: Optimize a portfolio."""

import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as spo
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def sddr_func(allocs, normed):
    alloced = normed * allocs
    pos_vals = alloced * 1
    port_vals = np.sum(pos_vals, axis = 1)
    addr = (port_vals / port_vals.shift(1)) -1
    dr = addr[1:]
    sddr= dr.std()
    return sddr


def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    allocs = np.asarray([0.2, 0.2, 0.3, 0.3]) # add code here to find the allocations
    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats

    allocs = np.array([1./len(syms)] * len(syms))
    normed = prices / prices.ix[0,:]
    bos = ((0.,1.),) * len(syms)
    cons = ({ 'type': 'eq', 'fun': lambda inputs: 1. - np.sum(inputs) })
    result = spo.minimize(sddr_func, allocs, args=(normed,), method = 'SLSQP', bounds = bos, constraints = cons, options={'disp': True})
    allocs = result.x

    alloced = normed * allocs
    pos_vals = alloced * 1
    port_vals = np.sum(pos_vals, axis = 1)

    cr = port_vals[-1] / port_vals[0] - 1
    addr = (port_vals / port_vals.shift(1)) -1
    dr = addr[1:]
    adr = dr.mean()
    sddr = dr.std()

    sr = ((252)**(.5))*((adr)/sddr)

    # Get daily portfolio value
    port_val = prices_SPY # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_vals, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        norme = df_temp / df_temp.ix[0,:]

        norme.plot()
        plt.title("Daily Portfolio Value and SPY")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid()
        plt.show()
        pass

    return allocs, cr, adr, sddr, sr


def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()

