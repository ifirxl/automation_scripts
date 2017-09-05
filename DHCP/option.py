#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import os
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Option:

    User = {} 
    Mac = {}
    Ip = {}
    num1 = 1
    num2 = 1
    num3 = 1

    def __init__(self, username=None, ip=None, mac=None):
        self.__user = username
        self.__ip = ip
        self.__mac = mac
        self.conn = sqlite3.connect('/home/kuar/DHCP/information.db',check_same_thread = False)
        self.__depart = {'99':'技术部','100':'研发部','102':'市场部','110':'行政部','120':'财务部'}
        self.logtime = time.strftime('%Y-%m-%d-%Hh%Mm%Ss')

    def fileLines(self):
        with open('/etc/dhcp/dhcpd.conf') as f:
            return [line.strip() for line in f.readlines() if "#" not in line]

    def diff(self):
        for i in self.fileLines():
            if 'host' in i:
                thename = i.split()[1]
                Option().User.update({self.num1:thename})
                self.num1 += 1
            elif 'hardware' in i:
                themac = i.split()[2].strip(';')
                Option().Mac.update({self.num2:themac})
                self.num2 += 1
            elif 'fixed-address' in i:
                theip = i.split()[1].strip(';')
                Option().Ip.update({self.num3:theip})
                self.num3 += 1

    def exitsInsert(self):
        self.diff()
        thecur = [cur[0] for cur in self.conn.execute('select ip from exits').fetchall()]
        for n in range(1,int(len(Option().User)+1)):
                if str(Option().Ip[n]) not in thecur:
                    print Option().Ip[n] + ' is adding...'
#                    self.conn.execute('insert into exits (username, department, ip, mac) values ("%s", "%s", "%s", "%s")'%(Option().User[n],self.__depart[Option().Ip[n].split('.')[2]], Option().Ip[n], Option().Mac[n]))
                    self.addInfo(Option().User[n], Option().Ip[n], Option().Mac[n])
                    self.conn.execute('insert into logs (time, option) values ("%s","%s")'%(self.logtime,'find the new information '+str(Option().Ip[n])))
        self.conn.commit()


    def addInfo(self, user, ip, mac):
        self.conn.execute('insert into exits (username, department, ip, mac) values ("%s", "%s", "%s", "%s")'%(user,self.__depart[ip.split('.')[2]],ip,mac))
        self.conn.commit()

    def date(self,user,ip,mac):
        return [
        'host ' + str(user) + ' {',
        ' hardware ethernet ' + str(mac) + ';',
        ' fixed-address ' + str(ip) + ';',
        '}'
        ]

    def fileHead(self):
        nn = 0
        L = []
        with open('dhcpd.conf') as f:
            filelines = [line.strip() for line in f.readlines()]
        for line in filelines: 
            if nn < 117:
                nn += 1
                L.append(line)
        return L

    def addAll(self):
        if self.__ip in [cur[0] for cur in self.conn.execute('select ip from exits').fetchall()]:
            return '[Warning]the ip %s already exists !!!'%self.__ip
        else:
            self.addInfo(self.__user, self.__ip, self.__mac)
            with open('dhcpd.conf','a') as f:
                for ff in [str(row)+'\n' for row in self.date(self.__user,self.__ip,self.__mac)]:
                    f.write(ff)
            self.conn.execute('insert into logs (time, option) values ("%s","%s")'%(self.logtime,'add '+str(self.__user)))
#            os.system('service dhcpd restart')
            self.conn.commit()
            return 'ok'



    def writeData(self):
        with open('2dhcpd.conf','a') as f:
            for x in self.fileHead():
                f.write(x+'\n')
            for theInfo in [row for row in self.conn.execute('select username,ip,mac from exits').fetchall()]:
                for message in self.date(theInfo[0],theInfo[1],theInfo[2]):
                    f.write(str(message)+'\n')
        isExists = os.path.exists('log')
        if not isExists:
            os.makedirs('log')
        try:
#            ret = os.system('mv /etc/dhcp/dhcpd.conf log/%s.conf && mv 2dhcpd.conf /etc/dhcp/dhcpd.conf && service dhcpd restart'%self.logtime)
            ret = os.system('mv dhcpd.conf log/%s.conf && mv 2dhcpd.conf dhcpd.conf'%self.logtime)
        except Exception,e:   
            print str(Exception)+':'+str(e) 


    def deleteInfo(self):
        if self.__user:
            self.conn.execute('delete from exits where username = "%s"'%self.__user)
            self.conn.execute('insert into logs (time, option) values ("%s","%s")'%(self.logtime,'delete '+str(self.__user)))
        elif self.__ip:
            self.conn.execute('delete from exits where ip = "%s"'%self.__ip)
            self.conn.execute('insert into logs (time, option) values ("%s","%s")'%(self.logtime,'delete '+str(self.__ip)))
        elif self.__mac:
            self.conn.execute('deltet from exits where mac = "%s"'%self.__mac)
            self.conn.execute('insert into logs (time, option) values ("%s","%s")'%(self.logtime,'delete '+str(self.__mac)))
        else:
            pass
        self.writeData()
        self.conn.commit()

    def changeInfo(self):
        if self.__ip and self.__mac:
            self.conn.execute('update exits set ip = "%s",mac="%s" where username = "%s"'%(self.__ip, self.__mac, self.__user))
            self.conn.execute('insert into logs (time, option) values ("%s","%s")'%(self.logtime,'change ' + str(self.__user) + 'ip --->>'+ str(self.__ip) +' mac --->>' +str(self.__mac)))
        elif self.__ip:
            self.conn.execute('update exits set ip = "%s" where username = "%s"'%(self.__ip, self.__user))
            self.conn.execute('insert into logs (time, option) values ("%s","%s")'%(self.logtime,'change ' + str(self.__user) + ' ip --->>' +str(self.__ip)))
        elif self.__mac:
            self.conn.execute('update exits set mac = "%s" where user = "%s"'%(self.__mac, self.__user))
            self.conn.execute('insert into logs (time, option) values ("%s","%s")'%(self.logtime,'change ' + str(self.__user) + ' ip --->>' +str(self.__mac)))
        else:
            pass
        self.writeData()
        self.conn.commit()

    def findInfo(self):
        if self.__ip:
            return [dict(username=row[0],ip=row[1],mac=row[2]) for row in  self.conn.execute('select username, ip, mac from exits where ip = "%s"'%(self.__ip))]
        elif self.__user:
            return [dict(username=row[0],ip=row[1],mac=row[2]) for row in self.conn.execute('select username,ip,mac from exits where username = "%s"'%(self.__user))]
        elif self.__mac:
            return [dict(username=row[0],ip=row[1],mac=row[2]) for row in self.conn.execute('select username,ip,mac from exits where mac="%s"'%(self.__mac))]
        self.conn.commit()


if __name__ == '__main__':
    op = Option()
    op.exitsInsert()
#    print op.User
#    print op.Ip
#    print op.Mac
#    conn = sqlite3.connect('information.db')
#    cur = conn.execute('select ip from exits')
#    print [i[0] for i in cur.fetchall()]
#    conn.commit()
    
