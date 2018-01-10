"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0
        self.Q = np.zeros((num_states, num_actions))
        #print self.Q
        self.rar = rar
        self.radr = radr
        self.alpha = alpha
        self.gamma = gamma
        self.dyna = dyna

        #construct T, Tc and R for dyna
        self.Tc = np.zeros((num_states, num_actions, num_states))
        self.R = np.zeros((num_states, num_actions))
        self.T = np.zeros((num_states, num_actions, num_states))

        self.num_states = num_states

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        action = np.argmax(self.Q[self.s, :])
        if self.verbose: print "s =", s,"a =",action
        self.a = action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        
        self.Q[self.s, self.a] = (1-self.alpha)*self.Q[self.s, self.a]+self.alpha*(r+self.gamma*self.Q[s_prime, np.argmax(self.Q[s_prime, :])])
        #copy s_prime since if not dyna we will use the origin value for next action
        origin_s_prime = s_prime
        origin_r = r
        if self.dyna != 0:
             self.Tc[self.s, self.a, s_prime] = self.Tc[self.s, self.a, s_prime] + 1
             self.T[self.s, self.a, :] = self.Tc[self.s, self.a, :] / self.Tc[self.s, self.a, :].sum()
             self.R[self.s, self.a] = (1-self.alpha)*self.R[self.s, self.a] + r * self.alpha

             #Repeat N times
             for i in range(0, self.dyna - 1):
             	self.s = rand.randint(0, self.num_states-1)
             	self.a = rand.randint(0, self.num_actions-1)
             	s_prime = np.argmax(self.T[self.s, self.a, :])
             	r = self.R[self.s, self.a]
             	self.Q[self.s, self.a] = (1-self.alpha)*self.Q[self.s, self.a]+self.alpha*(r+self.gamma*self.Q[s_prime, np.argmax(self.Q[s_prime, :])])

        ranNum = rand.randint(1, 10)
        ranNum = 0.1*ranNum
        if ranNum < self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.Q[origin_s_prime, :])
        self.rar = self.rar * self.radr
        self.s = origin_s_prime
        self.a = action
        if self.verbose: print "s =", origin_s_prime,"a =",action,"r =",origin_r
        return action

    def author(self):
        return 'jzhang950'

if __name__=="__main__":
    print author()
    print "Remember Q from Star Trek? Well, this isn't him"
