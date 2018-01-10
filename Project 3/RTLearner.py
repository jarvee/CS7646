import numpy as np
from numpy import nan
import random

class RTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        pass # move along, these aren't the drones you're looking for

    def author(self):
        return 'jzhang950' # replace tb34 with your Georgia Tech username

    def build_tree(self, data):
        if data.shape[0] <= self.leaf_size:
            leaf = np.array([[-1, data[:,-1].mean(), nan, nan]])
            return leaf
        if np.std(data[:,-1]) == 0:
            leaf = np.array([[-1, data[0,-1], nan, nan]])
            return leaf
        else:
            i = random.randint(0,data.shape[1]-2)
            SplitVal = np.median(data[:,i])

            lefttree = data[data[:,i] <= SplitVal]
            if lefttree.shape == data.shape:
                return np.array([[-1, data[:,-1].mean(), nan, nan]])
            righttree = data[data[:,i] > SplitVal]

            left_tree = np.array(self.build_tree(lefttree))
            right_tree = np.array(self.build_tree(righttree))

            root = np.array([[i, SplitVal, 1, left_tree.shape[0]+1]])
            return (np.vstack([root, left_tree, right_tree]))


    def addEvidence(self, trainX, trainY):
        dataSet = np.column_stack((trainX, trainY))
        self.result = self.build_tree(dataSet)

    def query(self, testX):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        resultY = []
        for i  in range(0, testX.shape[0]):
            row_num = testX[i]
            j = 0
            k = 0
            while (k != -1):
                k = self.result[j][0]
                k = int(k)
                predictY = self.result[j][1]
                if (k != -1):
                    if (testX[i][k] <= self.result[j][1]):
                        j = j + self.result[j][2]
                        j = int(j)
                    else:
                        j = j + self.result[j][3]
                        j = int(j)

            resultY = np.append(resultY, predictY)
        return resultY

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"