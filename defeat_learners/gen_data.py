"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=1489683273):
    np.random.seed(seed)
    X = np.random.random_sample((100, 3))
    Y = X[:,0] + X[:,1]**2 + X[:,2]**3
    return X, Y

def best4DT(seed=1489683273):
    np.random.seed(seed)
    X = np.random.random_sample((100, 3))
    Y = np.sin(X[:,0])**2 + 3.14 + np.sin(X[:,1])**4 + 5.5 + np.log(X[:,2])**3 +  np.cos(X[:,2])**3
    return X, Y

def author():
    return 'jzhang950' #Change this to your user ID

if __name__=="__main__":
    print "they call me Tim."
