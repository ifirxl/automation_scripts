#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import ftplib
      

class OpFtp:
    def __init__(self):
        self.ftp = ftplib.FTP()  
        self.timeout = 30
        self.port = 21

    def login(self, username, password):
        self.ftp.connect('192.168.30.130',self.port,self.timeout)  
        self.ftp.login(username, password) 
        return self.ftp.getwelcome()    

    def ftpquit(self):
        self.ftp.quit()                   

if __name__ == '__main__':
    t = OpFtp()
    print t.login('tom','heihei')
