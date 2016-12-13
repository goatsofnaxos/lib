'''
Created December 2, 2016
@author: Carl Schoonover
Set up automated email alerts
'''

from requests import post

class EmailAlert():

    def __init__(self,key):
        self.key = key
        self.toAddress   = "Goats Alert <goatsalert@mailgun.myneurosciencebet.com>"
        self.fromAddress = "Goats Alert <goatsalert@mailgun.myneurosciencebet.com>"

    def sendEmail(self, subject, text):
        self.postStatus = post(
            "https://api.mailgun.net/v3/mailgun.myneurosciencebet.com/messages",
            auth=("api", self.key),
            data={"from": self.fromAddress,
                  "to": self.toAddress,
                  "subject": subject,
                  "text": text
                  }
        )
        if self.postStatus.status_code == 200:
            print 'Email sent'
            return 1
        else:
            print 'Email failed to send'
            return 0

"""
Main module
"""

if __name__ == '__main__':
    emailAlert = EmailAlert(key="key-TKkeynum")
    emailStatus = emailAlert.sendEmail(subject='TEST',text='THIS IS A TEST')