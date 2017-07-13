'''

© 2017 The Trustees of Columbia University in the City of New York. All Rights Reserved.

Created September 29, 2015
@author: Carl Schoonover
Load and save user-defined parameters
'''

from os import path
import cPickle as pickle

class Empty():
    pass

class ParamLoad():

    def __init__(self,pythonScriptFile):
        self.userParamsFile = 'userParamsFile.dat'
        self.pythonScriptFilePath = path.dirname(path.realpath(pythonScriptFile))
        self.userParamsFileFullPath = self.pythonScriptFilePath + '\\' + self.userParamsFile

    def userParamFileExists(self):
        return path.isfile(self.userParamsFileFullPath)

    def loadUserParams(self):
        if self.userParamFileExists():
            with open(self.userParamsFileFullPath, 'rb') as input:
                returnObject = pickle.load(input)
                returnObject.loadedOldParams = 1
        else:
            returnObject = Empty()
            returnObject.loadedOldParams = 0
        return returnObject

    def saveUserParams(self,newUserParams):
        with open(self.userParamsFileFullPath, 'wb') as output:
            pickler = pickle.Pickler(output, -1)
            pickler.dump(newUserParams)

""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':
    paramLoad = ParamLoad(__file__)