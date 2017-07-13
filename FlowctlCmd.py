'''

© 2017 The Trustees of Columbia University in the City of New York. All Rights Reserved.

Created Jan 27, 2014
@author: All
'''
from __future__ import division
import numpy
import time
from PyDAQmx import *

class FlowCTL2():

    global DAQmx_Val_Volts, DAQmx_Val_Rising, DAQmx_Val_ContSamps, DAQmx_Val_GroupByChannel

    def __init__(self,MFCmaxRate):
        self.MFCmaxRate = MFCmaxRate
        self.MFCmaxVoltage = 5 # V
        self.MFCVoltFactor = []
        for x in self.MFCmaxRate:
            self.MFCVoltFactor.append(self.MFCmaxVoltage/x)
        self.numMFCs = self.MFCmaxRate.__len__()
        self.rt = 100 # Hz
        self.numsamples = 1
        self.write = int32()
        self.timeout = 10.0 # s
        self.autostart = 0
        self.initDAQ()

    def initDAQ(self):
        self.ao = Task()
        devStr = "dev2/ao0:" + str(self.numMFCs-1)
        self.ao.CreateAOVoltageChan(devStr,"Voltage",-10.0,10.0,DAQmx_Val_Volts,None)
        self.ao.CfgSampClkTiming("",self.rt,DAQmx_Val_Rising,DAQmx_Val_ContSamps,self.numsamples)
        self.ao.StartTask()
        self.updateDAQoutput([0]*self.numMFCs)

    def updateDAQoutput(self,newState):
        newStateScaled = [a*b for a,b in zip(newState,self.MFCVoltFactor)]
        self.data2Write  = numpy.array(newStateScaled, dtype=float64)
        self.ao.WriteAnalogF64(self.numsamples,self.autostart,self.timeout,DAQmx_Val_GroupByChannel,self.data2Write,self.write,None)

    def stopDAQ(self):
        self.updateDAQoutput([0]*self.numMFCs)
        self.ao.StopTask()
        self.ao.ClearTask()

class FlowCTL():

    global DAQmx_Val_Volts, DAQmx_Val_Rising, DAQmx_Val_ContSamps, DAQmx_Val_GroupByChannel
    
    def __init__(self,MFC_0vac_MaxFlow,MFC_1odor_MaxFlow,MFC_2air_MaxFlow):
        self.rt = 100 # Hz
        self.numsamples = 1
        self.write = int32()
        self.timeout = 10.0 # s
        self.autostart = 0
        self.maxVoltage = 5 # V
        self.MFC_0vac_MaxFlow = MFC_0vac_MaxFlow # L/mn
        self.MFC_0vac_factor = self.maxVoltage / self.MFC_0vac_MaxFlow
        self.MFC_1odor_MaxFlow = MFC_1odor_MaxFlow # L/mn
        self.MFC_1odor_factor = self.maxVoltage / self.MFC_1odor_MaxFlow
        self.MFC_2air_MaxFlow = MFC_2air_MaxFlow # L/mn
        self.MFC_2air_factor = self.maxVoltage / self.MFC_2air_MaxFlow
        
    def initDAQ(self):               
        self.ao = Task()
        self.ao.CreateAOVoltageChan("dev2/ao0,dev2/ao1,dev2/ao2","Voltage",-10.0,10.0,DAQmx_Val_Volts,None)
        self.ao.CfgSampClkTiming("",self.rt,DAQmx_Val_Rising,DAQmx_Val_ContSamps,self.numsamples)
        self.ao.StartTask()
        
    def stopDAQ(self):
        self.updateDAQoutput(0,0,0)
        self.ao.StopTask()
        self.ao.ClearTask()
    
    def updateDAQoutput(self,vacVal_0,odorVal_1,airVal_2):
        self.data2Write  = numpy.array([vacVal_0*self.MFC_0vac_factor, odorVal_1*self.MFC_1odor_factor, airVal_2*self.MFC_2air_factor], dtype=float64)
        self.ao.WriteAnalogF64(self.numsamples,self.autostart,self.timeout,DAQmx_Val_GroupByChannel,self.data2Write,self.write,None)
        # print "vacVal_0: ", vacVal_0, "L/mn        odorVal_1: ", odorVal_1, "L/mn        airVal_2: ", airVal_2, "L/mn"
        
if __name__ == "__main__":

    flowRate = [0.2] + [0.6]*4
    MFCmaxRate = [5] + [2]*4
    flow = FlowCTL2(MFCmaxRate)
    flow.updateDAQoutput([0.5]*5)
    flow.stopDAQ()


    quit()


    flow = FlowCTL()
    flow.initDAQ()
    vacVal_0 = 0.6
    odorVal_1 = 0.79
    airVal_2 = 0.785
    flow.updateDAQoutput(vacVal_0, odorVal_1, airVal_2) # L/mn
    raw_input("Press Enter to quit")
    flow.stopDAQ()
