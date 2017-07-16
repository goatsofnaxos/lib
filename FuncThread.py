'''

(c) 2017 The Trustees of Columbia University in the City of New York. All Rights Reserved.

Created March 26, 2016
Simple threading with arguments and ability to halt thread before it has completed execution
@author: Carl Schoonover
'''

import threading

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
        super(FuncThread, self).__init__()
        self._stop = threading.Event()

    def run(self):
        self._target(*self._args)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

"""
Main module
"""
if __name__ == '__main__':

    def fooFunction(arg1,arg2):
        print 'Foo!', arg1, arg2

    # Define thread and pass arguments
    fooThread = FuncThread(fooFunction,'Bar','Bla bla bla')

    # When desired, launch thread
    fooThread.start()

    # Halt thread before it completes execution
    # fooThread.stop()

    # Wait until thread has completed execution before proceeding
    fooThread.join()
