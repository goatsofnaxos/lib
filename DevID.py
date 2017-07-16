'''

(c) 2017 The Trustees of Columbia University in the City of New York. All Rights Reserved.

Created Dec 19, 2013

@author: All
'''
class DevID():
    def __init__(self):
        # Device 1 (PXI-6251)
        self.dev1aoCh = ["dev1/ao0",
                         "dev1/ao1"]
        self.dev1aiCh = ["dev1/ai0",
                         "dev1/ai1",
                         "dev1/ai2",
                         "dev1/ai3",
                         "dev1/ai4",
                         "dev1/ai5",
                         "dev1/ai6",
                         "dev1/ai7",
                         "dev1/ai8",
                         "dev1/ai9",
                         "dev1/ai10",
                         "dev1/ai11",
                         "dev1/ai12",
                         "dev1/ai13",
                         "dev1/ai14",
                         "dev1/ai15"]
        # Device 2 (PXI-6713)
        self.dev2aoCh = ["dev2/ao0",
                         "dev2/ao1",
                         "dev2/ao2",
                         "dev2/ao3",
                         "dev2/ao4",
                         "dev2/ao5",
                         "dev2/ao6",
                         "dev2/ao7"]
        self.dev2aiCh = [""]
        # Device 3 (PXI-6512)
        self.dev3aoP0 = ["dev3/port0/line0",
                         "dev3/port0/line1",
                         "dev3/port0/line2",
                         "dev3/port0/line3",
                         "dev3/port0/line4",
                         "dev3/port0/line5",
                         "dev3/port0/line6",
                         "dev3/port0/line7"]
        self.dev3aoP1 = ["dev3/port1/line0",
                         "dev3/port1/line1",
                         "dev3/port1/line2",
                         "dev3/port1/line3",
                         "dev3/port1/line4",
                         "dev3/port1/line5",
                         "dev3/port1/line6",
                         "dev3/port1/line7"]
        self.dev3aoP2 = ["dev3/port2/line0",
                         "dev3/port2/line1",
                         "dev3/port2/line2",
                         "dev3/port2/line3",
                         "dev3/port2/line4",
                         "dev3/port2/line5",
                         "dev3/port2/line6",
                         "dev3/port2/line7"]        
        self.dev3aiCh = [""]

        # OLD NOMENCALTURE--KEEP FOR BACK-COMPATIBILITY WITH OLD SCRIPTS
        self.outChannels = ["dev1/ao0",
                            "dev1/ao1",
                            "dev2/ao0",
                            "dev2/ao1",
                            "dev2/ao2",
                            "dev2/ao3",
                            "dev2/ao4",
                            "dev2/ao5",
                            "dev2/ao6",
                            "dev2/ao7"]
        self.inChannels =  ["dev1/ai0",
                            "dev1/ai1",
                            "dev1/ai2",
                            "dev1/ai3",
                            "dev1/ai4",
                            "dev1/ai5",
                            "dev1/ai6",
                            "dev1/ai7",
                            "dev1/ai8",
                            "dev1/ai9",
                            "dev1/ai10",
                            "dev1/ai11",
                            "dev1/ai12",
                            "dev1/ai13",
                            "dev1/ai14",
                            "dev1/ai15"]

    def channelsStrGen(self,channelList,channelRange):
        devChannelsIDstr = ""
        for i in range(channelRange[0],channelRange[1]+1):
            devChannelsIDstr += channelList[i] + ","
        return devChannelsIDstr
