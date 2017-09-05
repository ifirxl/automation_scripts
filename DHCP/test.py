#!/usr/bin/python
# -*- coding: utf-8 -*-
nn = 0
L = []
with open('dhcpd.conf') as f:
    filelines = [line.strip() for line in f.readlines()]
for line in filelines: 
    if nn < 117:
        nn += 1
        L.append(line)
for i in L:
    print i

