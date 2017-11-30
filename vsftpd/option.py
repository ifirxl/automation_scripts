#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from logs import Logs  


class Option():

    def __init__(self):
        self.log = Logs()

    def chpassword(self, username, password):
        return [i.strip() for i in os.popen('echo %s | passwd %s --stdin'%(password,username)).readlines()][0]

    def addUsers(self,jobnum, zh_username, username ,password, department):
#        result = [i.strip() for i in os.popen('useradd -d /var/ftp/%s -g ftp -s /sbin/nologin %s'%(username,username)).readlines()][0] 
        result = ''
        if result == '':
            self.log.adduser(jobnum, zh_username, username, password, department)
            results = '成功添加用户 %s'%zh_username
            self.log.addlog(results)
            return results        
        else:
            return result

    def delUsers(self,username):
#        result = [i.strip() for i in os.popen('userdel %s'%(username)).readlines()][0] 
#        if result == "":
#            self.log.addlog('成功删除用户 %s'%username)
#        else:
#            self.log.addlog(result)
        self.log.addlog('成功删除用户 %s'%username)


if __name__ == '__main__':
    pass
