'''
Created December 13, 2016
@author: Carl Schoonover
Set up automated email alerts
'''

from requests import post

class EmailAlert():

    def __init__(self,key,toAddress,fromAddress,URL):
        self.verbose = True
        self.key = key
        self.URL = URL
        self.toAddress   = toAddress #"Goats Alert <goatsalert@mailgun.myneurosciencebet.com>"
        self.fromAddress = fromAddress #"Goats Alert <goatsalert@mailgun.myneurosciencebet.com>"

    def sendEmail(self, subject, text):
        self.postStatus = post(
            self.URL, #"https://api.mailgun.net/v3/mailgun.myneurosciencebet.com/messages",
            auth=("api", self.key),
            data={"from": self.fromAddress,
                  "to": self.toAddress,
                  "subject": subject,
                  "text": text
                  }
        )
        if self.postStatus.status_code == 200:
            if self.verbose:
                print 'Email sent'
            return 1
        else:
            if self.verbose:
                print 'Email failed to send'
                print '  ', self.postStatus.status_code
                print '  ', self.postStatus.content
            return 0

"""
Main module
"""

if __name__ == '__main__':
    emailAlert = EmailAlert(key="",toAddress="",fromAddress="",URL="")
    emailStatus = emailAlert.sendEmail(subject='TEST',text='THIS IS A TEST')