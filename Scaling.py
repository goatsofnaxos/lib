'''

© 2017 The Trustees of Columbia University in the City of New York. All Rights Reserved.

Created December 2, 2016
@author: Carl Schoonover
Scale DAQ signals
Input should be scalar or numpy array
'''

from __future__ import division

class Scaling():

    def __init__(self,actual,signal,unit):
        self.actual = actual
        self.signal = signal
        self.unit   = unit
        self.computeScaling()

    def computeScaling(self):
        self.slope = (self.signal[1]-self.signal[0]) / (self.actual[1]-self.actual[0])
        self.offset =  self.signal[1] - (self.slope*self.actual[1])

    def sig2act(self,input):
        return (input - self.offset) / self.slope

    def act2sig(self,input):
        return (input * self.slope) + self.offset