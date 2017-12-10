#!/usr/bin/python
# -*- coding: utf-8 -*-
#Author : Kuari <www.justmylife.cc>
#Mail : kuari@justmylife.cc

import urllib
import urllib2
import os
import json
import time
import sys


class Con:

    def __init__(self, username, password):
        self.log_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.username = username
        self.password = password

    def login(self):
        headers = {
            'Host':'10.10.10.52',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Accept':'*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding':'gzip, deflate',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://10.10.10.52/eportal/index.jsp?wlanuserip=7234a00cb40ffd689b117330fd412618&wlanacname=5fcbc245a7ffdfa4&ssid=&nasip=80b4f717eedd90b8eb2de8bfc5e1582c&snmpagentip=&mac=1d13613c012dea9a4fe5a5bde72ff163&t=wireless-v2&url=2c0328164651e2b4f13b933ddf36628bea622dedcc302b30&apmac=&nasid=5fcbc245a7ffdfa4&vid=adfe73f03d20ff05&port=768b7f1f2cedfe5f&nasportid=5b9da5b08a53a540871303b4f6662eb2b663e1ab8381d3e0269b994c9923c94d2e6ed5063571156f',
            'Content-Length':'593',
            'Cookie':'EPORTAL_COOKIE_USERNAME='+ self.username +'; EPORTAL_COOKIE_PASSWORD='+ self.password +'; EPORTAL_COOKIE_SERVER=; EPORTAL_COOKIE_SERVER_NAME=%E8%AF%B7%E9%80%89%E6%8B%A9%E6%9C%8D%E5%8A%A1; EPORTAL_COOKIE_OPERATORPWD=; EPORTAL_COOKIE_DOMAIN=; EPORTAL_COOKIE_SAVEPASSWORD=true; EPORTAL_AUTO_LAND=; JSESSIONID=A268D99F2AB443ED9984B65589772160',
            'Connection':'keep-alive',
            'Pragma':'no-cache',
            'Cache-Control':'no-cache'
            }
        post_data = 'userId='+ self.username +'&password='+ self.password +'&service=&queryString=wlanuserip%253D7234a00cb40ffd689b117330fd412618%2526wlanacname%253D5fcbc245a7ffdfa4%2526ssid%253D%2526nasip%253D80b4f717eedd90b8eb2de8bfc5e1582c%2526snmpagentip%253D%2526mac%253D1d13613c012dea9a4fe5a5bde72ff163%2526t%253Dwireless-v2%2526url%253D2c0328164651e2b4f13b933ddf36628bea622dedcc302b30%2526apmac%253D%2526nasid%253D5fcbc245a7ffdfa4%2526vid%253Dadfe73f03d20ff05%2526port%253D768b7f1f2cedfe5f%2526nasportid%253D5b9da5b08a53a540871303b4f6662eb2b663e1ab8381d3e0269b994c9923c94d2e6ed5063571156f&operatorPwd=&operatorUserId=&validcode='
        url = 'http://10.10.10.52/eportal/InterFace.do?method=login'
        request = urllib2.Request(url, post_data, headers)
        response = urllib2.urlopen(request)
        return response.read()

    def run(self):
        results = json.loads(self.login())['message']
        if results:
            print self.log_time + ' ---------- ' + results
        else: 
            print self.log_time + ' ---------- 连接网络'


def Start(username, password, pattern, timeout):
    conn = Con(username, password)
    if pattern:
        if pattern == '1':
            conn.run()
        elif pattern == '2': 
            while True:
                conn.run()
                time.sleep(int(timeout))
    else:
        conn.run()


def getFile(filename):
    with open(filename, 'r+') as f:
        lines = f.readlines()
        L = []
        data = {}
        for line in lines:
            if "=" in line and '#' not in line:
                L.append(line.strip())
        if len(L) < 5:
            for i in L:
                i = i.split('=')
                data[i[0]]=i[1]
            return data
        else:
            return 'error'


def main():
    import optparse

    parser = optparse.OptionParser('usage %prog -u <target username> -p <target password> [options]',version="%prog 2.3")
    parser.add_option('-u', '--username', dest='tgtusername', type='string', help='specify target username')
    parser.add_option('-p', '--password', dest='tgtpassword', type='string', help='specify target password')
    parser.add_option('-m', '--model', dest='tgtpattern', type='string', help='specify target pattern, 1:connect once, 2:Automatic reconnection(default)',default="2")
    parser.add_option('-t', '--timeout', dest='tgttimeout', type='int', help='specify target timeout, the default is 300', default=300)
    parser.add_option('-f', '--file', dest='tgtfile', type='string', help='specify target file,use the template file "example.conf" and please use this parameter individually')

    (options, args) = parser.parse_args()

    tgtusername = options.tgtusername
    tgtpassword = options.tgtpassword
    tgtpattern = options.tgtpattern
    tgttimeout = options.tgttimeout
    tgtfile = options.tgtfile

    if tgtfile == None:
        if tgtusername == None or tgtpassword == None:
            print(parser.usage)
            exit(0)
    
    if tgtfile:
        data = getFile(tgtfile)
        if data == 'error':
            print "File format error"
        else:
            username = data['username']
            password = data['password']
            timeout = data['timeout']
            pattern = data['model']
            Start(username, password, pattern, timeout)
    else:
        Start(tgtusername, tgtpassword, tgtpattern, tgttimeout)


if __name__ == '__main__':
    main()
