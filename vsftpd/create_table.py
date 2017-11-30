#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('theoption.db')
print "Opened database successfully!"

conn.execute('''
create table users(
id integer primary key autoincrement,
jobnum      text,
zh_username text,
username    text,
password    text,
department  char(5),
time    time
);''')

conn.execute('''
create table logs(
id integer primary key autoincrement,
options    text,
time    time
);''')

conn.execute('''
create table departments(
id integer primary key autoincrement,
department    text
);''')

conn.execute('''
create table apply(
id integer primary key autoincrement,
jobnum      text,
zh_username text,
username    text,
password    text,
department  char(5),
time    time,
status  chat(2)
);''')

print "Table created successfully!";
