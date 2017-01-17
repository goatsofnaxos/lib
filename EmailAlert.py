'''
Created December 13, 2016
@author: Carl Schoonover
Set up automated email alerts
'''

from requests import post
from time import sleep, strftime
from FuncThread import FuncThread
from numpy.random import normal

class EmailAlert():

    def __init__(self,key,toAddress,fromAddress,url):
        self.verbose = True
        self.key = key
        self.url = url
        self.toAddress   = toAddress
        self.fromAddress = fromAddress

    def sendEmail(self, subject, text):
        self.postStatus = post(
            self.url,
            auth=("api", self.key),
            data={"from": self.fromAddress,
                  "to": self.toAddress,
                  "subject": subject,
                  "text": text
                  }
        )
        if self.postStatus.status_code == 200:
            if self.verbose:
                cnfrmStr = 'Email sent at ' + strftime("%H:%M:%S")
                print cnfrmStr
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

    def harassMeEvery(self,mu_sigma_num,subjStr,bodyStr):
        self.harassMeEveryThreadObj = FuncThread(self.harassMeEveryThread,mu_sigma_num,subjStr,bodyStr)
        self.harassMeEveryThreadObj.start()

    def emailMeInThread(self,waitTime):
        waitTimeSec = round(waitTime * 60)
        sleep(waitTimeSec)
        subjStr = 'Email timer'
        bodyStr = strftime("%H:%M:%S") + ' / ' + str(waitTime) + ' mn have elapsed.'
        self.sendEmail(subjStr,bodyStr)
        if self.verbose:
            print 'Sent email after', waitTime, 'mn.'

    def harassMeEveryThread(self,mu_sigma_num,subjStr,bodyStr):
        muPeriod = mu_sigma_num[0]    # hours
        sigmaPeriod = mu_sigma_num[1] # hours
        numEmails = mu_sigma_num[2]
        for x in range(0,numEmails):
            self.sendEmail(subjStr,bodyStr)
            sleepTime = normal(muPeriod,sigmaPeriod,1) * 3600
            sleep(sleepTime)

"""
Main module
"""

if __name__ == '__main__':
    emailAlert = EmailAlert(key="",toAddress="",fromAddress="",URL="")
    emailAlert.sendEmail(subject='TEST EMAIL',text='This is a test.')
    emailAlert.emailMeIn(1.5)
