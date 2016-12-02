'''
Created December 2, 2016
@author: Carl Schoonover
Scale DAQ signals
Input should be scalar or numpy array
'''

from __future__ import division

class Scaling():

    def __init__(self,actual,signal):
        self.computeScaling(actual,signal)

    def computeScaling(self,actual,signal):
        self.slope = (signal[1]-signal[0]) / (actual[1]-actual[0])
        self.offset =  signal[1] - (self.slope*actual[1])

    def scale(self,input):
        return (input - self.offset) / self.slope