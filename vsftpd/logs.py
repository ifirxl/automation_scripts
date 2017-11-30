#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Logs:
    
    def __init__(self):
        self.logtime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.conn = sqlite3.connect('theoption.db',check_same_thread = False)

    def addlog(self,option):
        self.conn.execute('insert into logs (options, time) values ("%s", "%s")'%(option, self.logtime))
        self.conn.commit()

    def adduser(self,jobnum, zh_username, username, password, department):
        self.conn.execute('insert into users (jobnum, zh_username, username, password, department, time) values ("%s", "%s", "%s", "%s", "%s", "%s")'%(jobnum, zh_username, username, password, department, self.logtime))
        self.conn.commit()

if __name__ == '__main__':
    Logs().addlog('just a try!')

