#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3


class GetIp:

    def __init__(self):
        self.key99 = []
        self.key100 = []
        self.key102 = []
        self.key110 = []
        self.key120 = []
        self.conn = sqlite3.connect('/home/kuari/DHCP/information.db',check_same_thread = False)

    def handle(self):
        for theip in [row for row in self.conn.execute('select ip from exits').fetchall()]:
            ip = str(theip[0].split('.')[2])
            ipp = str(theip[0].split('.')[3])
            if ip == '99':
                self.key99.append(int(ipp))
            elif ip == '100':
                self.key100.append(int(ipp))
            elif ip == '102':
                self.key102.append(int(ipp))
            elif ip == '110':
                self.key110.append(int(ipp))
            elif ip == '120':
                self.key120.append(int(ipp))
            else:
                pass
            self.conn.commit()
    
    def ip99(self):
        self.handle()
        return '10.23.99.' + str([i for i in range(1,255) if i not in self.key99][0])

    def ip100(self):
        self.handle()
        return '10.23.100.' + str([i for i in range(1,255) if i not in self.key100][0])

    def ip102(self):
        self.handle()
        return '10.23.102.' + str([i for i in range(1,255) if i not in self.key102][0])

    def ip110(self):
        self.handle()
        return '10.23.110.' + str([i for i in range(1,255) if i not in self.key110][0])

    def ip120(self):
        self.handle()
        return '10.23.120.' + str([i for i in range(1,255) if i not in self.key120][0])

    def test(self):
        self.handle()
        print self.key99
        print self.key100
        print self.key102
        print self.key110
        print self.key120


if __name__ == '__main__':
    print GetIp().ip120()
    print ''
    GetIp(). test()
