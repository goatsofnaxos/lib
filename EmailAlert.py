'''
Created December 13, 2016
@author: Carl Schoonover
Set up automated email alerts
'''

from requests import post
from time import sleep
from FuncThread import FuncThread

class EmailAlert():

    def __init__(self,key,toAddress,fromAddress,URL):
        self.verbose = True
        self.key = key
        self.URL = URL
        self.toAddress   = toAddress
        self.fromAddress = fromAddress

    def sendEmail(self, subject, text):
        self.postStatus = post(
            self.URL,
            auth=("api", self.key),
            data={"from": self.fromAddress,
                  "to": self.toAddress,
                  "subject": subject,
                  "text": text
                  }
        )
        if self.postStatus.status_code == 200:
            if self.verbose:
                print 'Email sent.'
            return 1
        else:
            if self.verbose:
                print 'Email failed to send.'
                print '  ', self.postStatus.status_code
                print '  ', self.postStatus.content
            return 0

    def emailMeIn(self,waitTime):
        self.emailMeInThreadObj = FuncThread(self.emailMeInThread,waitTime)
        self.emailMeInThreadObj.start()

    def emailMeInThread(self,waitTime):
        waitTimeSec = round(waitTime * 60)
        sleep(waitTimeSec)
        textStr = str(waitTime) + ' mn have elapsed.'
        self.sendEmail('Email timer',textStr)
        if self.verbose:
            print 'Sent email after', waitTime, 'mn.'

"""
Main module
"""

if __name__ == '__main__':
    emailAlert = EmailAlert(key="",toAddress="",fromAddress="",URL="")
    emailStatus = emailAlert.sendEmail(subject='TEST EMAIL',text='This is a test.')