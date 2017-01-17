'''
Created January 16, 2017
@author: Carl Schoonover
Strip Blackrock ns* headers and concatenate
'''

from os import getenv
from os.path import isfile, splitext, basename, dirname, sep
from sys import argv, exit
from numpy import fromfile, uint8, uint32
from subprocess import Popen

class HeaderMagic():

    def __init__(self,argv):

        self.filenames = []
        self.filenamesdat = []
        self.filebasenames = ''

        for file in argv:

            # Make sure the file is what we think it is
            self.filenames.append(file.replace('~',getenv('HOME')))
            self.filenamesdat.append(self.filenames[-1]+'.dat')
            self.filebasenames = self.filebasenames + basename(splitext(self.filenames[-1])[0]) + '-'
            if not isfile(self.filenames[-1]):
                print 'ERROR:', self.filenames[-1], 'does not exist'
                exit(0)
            if not (self.filenames[-1].endswith('.ns4') or self.filenames[-1].endswith('.ns5')):
                print 'ERROR:', self.filenames[-1], 'does not appear to be a Blackrock ns* file.'
                exit(0)
            self.f = open(self.filenames[-1], 'rb')
            if self.f.read(8) != 'NEURALCD':
                print 'ERROR:', self.filenames[-1], 'is not a NEURALCD file; need to implement script for other formats.'
                exit(0)

            # Loop up the header size
            basicHeader = fromfile(self.f, uint8, 306)
            dataHeaderBytes = 9
            headerBytes = int(basicHeader[2:6].view(uint32) + dataHeaderBytes)
            self.f.close()

            # Copy file and chop off first N bytes
            cmd_list = ['time', 'dd', 'bs='+str(headerBytes), 'skip=1', 'if='+self.filenames[-1], 'of='+self.filenamesdat[-1]]
            a = Popen(cmd_list)
            a.communicate()
            print 'Removed header from', self.filenames[-1], 'and copied to', self.filenamesdat[-1]


        # Concatenate files
        if self.filenames.__len__() > 1:
            concatfilename = dirname(self.filenamesdat[0]) + sep + self.filebasenames[0:-1] + splitext(self.filenames[0])[1] + '.dat'
            cmd_list = ['cat']
            for datfile in self.filenamesdat:
                cmd_list.append(datfile)
            cmd_list.append('>')
            cmd_list.append(concatfilename)
            print ' '.join(cmd_list)
            p = Popen(' '.join(cmd_list), shell=True)
            p.wait()
            print 'Concatenated', self.filenames.__len__(), 'files, saving to', concatfilename


"""
Main module
"""

if __name__ == '__main__':
    if argv.__len__() < 2:
        print 'HeaderMagic removes the header of Blackrock ns* file.'
        print 'It can optionally concatenate multiple Blackrock ns* file.'
        print 'Usage: python HeaderMagic.py file1 [file2, file 3, ...]'
        exit(0)
    hm = HeaderMagic(argv[1:])
