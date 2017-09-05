#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('information.db')
print "Opened database successfully!"

conn.execute('''
create table exits(
id integer primary key autoincrement,
username    text,
department   text,
ip    text,
mac    text
);''')

conn.execute('''
create table logs(
id integer primary key autoincrement,
time    text,
option   text
);''')

conn.execute('''
create table ips(
id integer primary key autoincrement,
ip    text,
type   text
);''')


print "Table created successfully!";


