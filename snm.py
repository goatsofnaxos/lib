#!/usr/bin/env python

'''

(c) 2017 The Trustees of Columbia University in the City of New York. All Rights Reserved.

Created January 16, 2017
@author: Carl Schoonover
snm stands for strip and merge
- Strip Blackrock ns* headers
- Merge .dat files
'''

from os import getenv
from os.path import isfile, splitext, basename, dirname, sep, join
from sys import argv, exit
from numpy import fromfile, uint8, uint32
from subprocess import Popen

class SNM():

    def __init__(self,output,action,filenames):
        # Make sure there's no garbage coming in
        self.output = output
        self.filenames = filenames
        extentions = []

        for file in self.filenames:
            if not isfile(file):
                print('ERROR: ' + file + ' does not exist')
                exit(0)
            extentions.append(splitext(file)[1])
        if not all(x == extentions[0] for x in extentions):
            print('ERROR: ' + self.filenames + ' do not all have the same file extention.')
        if (action == '-s' or action == '-n') and extentions[0][0:3] != '.ns':
            print('ERROR: stripping only possible on .ns* files.')
            exit(0)
        if action == '-m' and extentions[0] != '.dat':
            print('ERROR: merging only possible on .dat files.')
            exit(0)
        # Now strip and/or merge
        if action == '-s':
            self.strip()
        if action == '-m' or action == '-n':
            if self.filenames.__len__() < 2:
                print('ERROR: merging requires >1 file.')
                exit(0)
            if action == '-m':
                self.merge()
            elif action == '-n':
                self.strip()
                self.filenames = [s + '.dat' for s in self.filenames]
                self.merge()

    def strip(self):
        for file in self.filenames:
            f = open(file, 'rb')
            if f.read(8).decode('UTF-8') != 'NEURALCD':
                print('ERROR: ' + file + ' is not a NEURALCD file; need to implement script for other formats.')
                f.close()
                exit(0)
            # Loop up the header size
            basicHeader = fromfile(f, uint8, 306)
            dataHeaderBytes = 9
            headerBytes = int(basicHeader[2:6].view(uint32) + dataHeaderBytes)
            f.close()
            # Copy file and chop off first N bytes
            filenamesdat = file+'.dat'
            cmd_list = ['time', 'dd', 'bs='+str(headerBytes), 'skip=1', 'if='+file, 'of='+filenamesdat]
            a = Popen(cmd_list)
            a.communicate()
            print('Removed header from ' + file + ' and copied to ' + filenamesdat)

    def merge(self):
        #mergefilename = ''
        cmd_list = ['cat']
        for file in self.filenames:
            #mergefilename = mergefilename + file.split('.')[0].split('/')[-1].split('_')[0] + '-'
            cmd_list.append(file)
        #mergefilename = dirname(filenames[0]) + '/' + mergefilename[:-1] + '.dat'
        #mergefilename = join(dirname(filenames[0]), 'snm-merge.dat')
        mergefilename = self.output
        cmd_list.append('>')
        cmd_list.append(mergefilename)
        p = Popen(' '.join(cmd_list), shell=True)
        p.wait()
        print('Merged ' + str(self.filenames.__len__()) + ' files, saving to ' + mergefilename)


"""
Main module
"""

if __name__ == '__main__':

    inputerrorstr = 'Usage: snm.py outputfile [-smn] file1 [file2, file 3, ...]\n' \
                    '  -s  strip the header of Blackrock ns* file\n' \
                    '  -m  merge (concatenate) .dat files in this order\n' \
                    '  -n  strip the header, then merge'

    if argv.__len__() < 3:
        print(inputerrorstr)
        exit(0)
    output = argv[1]
    action = argv[2]
    filenames = argv[3:]

    if action == '-s' or action=='-m' or action=='-n':
        snm = SNM(output, action, filenames)
    else:
        print(inputerrorstr)
        exit(0)
