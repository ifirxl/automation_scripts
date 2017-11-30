#!/usr/bin/python
# -*- coding:utf8 -*-
"""
作者: Kuari <www.justmylife.cc>
环境: Debian系,Python2.7,运行时需要用到root权限
"""
import os
import sys

try:
    import netifaces
except ImportError:
    try:
        command_to_execute = "sudo pip install netifaces || easy_install netifaces"
        os.system(command_to_execute)
    except OSError:
        print "Can NOT install netifaces, Aborted!"
        sys.exit(1)
    import netifaces

   
lines = os.popen('sudo dpkg -l | grep -i nmap')
if lines == "":
    print ('你未安装nmap,将为你安装nmap软件')
    os.system('sudo apt-get install nmap -y')

routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]

for interface in netifaces.interfaces():
    if interface == routingNicName:
        try:
            routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
            IPS = routingIPAddr.split(".")
            IPS[3] = "0"
            routingIPAddr = ".".join(IPS)

            exchange_mask = lambda mask: sum(bin(int(i)).count('1') \
                                 for i in mask.split('.'))

            routingIPNetmask = exchange_mask(routingIPNetmask)
        except KeyError:
            print ("[Warning!!!] 自动获取ip失败，请手动输入网段与子网掩码!")
            print ("样例为 : ip 192.168.1.0 mask 25")
            routingIPAddr = raw_input("网段 :")
            routingIPNetmask = raw_input("子网掩码 :")

print ("---"*10)
if routingNicName:
    print (u"网卡: %s"%routingNicName)
print (u"IP地址: %s"%routingIPAddr)
print (u"子网掩码: %s"%routingIPNetmask)
print ("---"*10)

IP = routingIPAddr + "/" + str(routingIPNetmask)
print ("正在扫描中...")
if os.system("sudo nmap -sP '%s'| grep Raspber -B 2"%IP) != 0:
    print ("局域网内未发现树莓派信息...")
