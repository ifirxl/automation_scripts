#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import time
import os



def ping():
    while True:
        if os.system('ping www.baidu.com -c 5 | grep ttl') == 0:
            login()
            print '登录成功。。。'
            time.sleep(1800)
        else:
            print 'Failed...'


def login():
        data = {
                'DDDDD':'myusername',
                'upass':'mypassword',
                '0MKKey':'(unable to decode value)'
        }
        headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Host':'10.10.0.228',
                'Referer':'http://10.10.0.228/',
                'Upgrade-Insecure-Requests':1,
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }
        post_data = urllib.urlencode(data)
        login_url = "http://10.10.0.228/"
        request = urllib2.Request(login_url, post_data, headers)
        response = urllib2.urlopen(request)
        result = response.read().decode('gbk')
#        print result
        


if __name__ == '__main__':
    ping()
