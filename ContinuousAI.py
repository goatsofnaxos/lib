'''

(c) 2017 The Trustees of Columbia University in the City of New York. All Rights Reserved.

Created March 26, 2016
Implements continuous (callback-based) analog input using the PyDAQmx wrapper
Future versions can implement this as a thread with a signal emitted to main thread from EveryNCallback
@author: Carl Schoonover
'''

import threading
from time import sleep
from PyDAQmx import *

class ContinuousAI(Task):

    def __init__(self,aiChannels,aiChannelsNum,aiBufferSize,aiRt):
        Task.__init__(self)
        self.aiChannelsNum = aiChannelsNum
        self.aiBufferSize  = aiBufferSize
        self.aiRead        = int32()
        self.timeout       =  10.0 # s
        self.Vrange        = [-10.0, 10.0]
        self.aiBufferData  = numpy.tile(numpy.zeros((aiBufferSize,), dtype=numpy.float64),(aiChannelsNum,1)) # Time column-wise
        self.CreateAIVoltageChan(aiChannels,"Analog inputs",DAQmx_Val_RSE,self.Vrange[0],self.Vrange[1],DAQmx_Val_Volts,None)
        self.CfgSampClkTiming("",aiRt,DAQmx_Val_Rising,DAQmx_Val_ContSamps,aiBufferSize)
        self.AutoRegisterEveryNSamplesEvent(DAQmx_Val_Acquired_Into_Buffer,aiBufferSize,0,name='EveryNCallback')
        self.AutoRegisterDoneEvent(0,name='DoneCallback')
        self.StartTask()

    def EveryNCallback(self):
        self.ReadAnalogF64(self.aiBufferSize,self.timeout,DAQmx_Val_GroupByChannel,self.aiBufferData,self.aiBufferSize*self.aiChannelsNum,byref(self.aiRead),None)
        return 0 # The function should return an integer

    def DoneCallback(self, status):
        print "Status",status.value
        return 0 # The function should return an integer


"""
Main module
"""
if __name__ == '__main__':

    # Parameters for analog inputs
    aiChannels       = "dev1/ai0:1"
    aiChannelsNum    = 2
    aiBufferSize     = 100
    aiRt             = 1000

    # Instantiate ContinuousAI, launch, aquire for 1 second, the stop and clean up
    ai = ContinuousAI(aiChannels,aiChannelsNum,aiBufferSize,aiRt)
    sleep(1)
    ai.StopTask()
    ai.ClearTask()


