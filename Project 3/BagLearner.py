import numpy as np
from numpy import nan
import random
import DTLearner as dt
import RTLearner as rt
import InsaneLearner as it


class BagLearner(object):

    def __init__(self, learner, kwargs, bags, boost, verbose):
        self.kwargs = kwargs
        self.bags = bags
        self.verbose = verbose
        self.learners = []
        for mode in range(0, self.bags):
            self.learners.append(learner(**self.kwargs))
        pass # move along, these aren't the drones you're looking for

    def author(self):
        return 'jzhang950' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        for mode in self.learners:
            split = np.random.randint(len(dataX),size=len(dataY))
            resultX = dataX[split,:]
            resultY = dataY[split]
            mode.addEvidence(resultX, resultY)


    def query(self, testX):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        preY = []
        for mode in self.learners:
            result = mode.query(testX)
            preY.append(result)
        return np.mean(preY, axis = 0)


if __name__=="__main__":
    print "the secret clue is 'zzyzx'"