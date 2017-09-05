#!/usr/bin/python
# -*- coding: utf-8 -*-
# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from option import Option
from  getIp import *

# configuration
DATABASE = '/home/kuari/DHCP/information.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'
gi = GetIp()

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()


@app.route('/')
def show_entries():
    if not session.get('logged_in'):
#        abort(401)
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_entry():
    username = request.form['username']
    ip = request.form['ip']
    mac = request.form['mac']
    option = request.form['option']
    if not ip:
        ip = None
    elif not username:
        username = None
    elif not mac:
        mac = None
    if str(ip) == '99':
        ip = gi.ip99()     
        print ip
    elif str(ip) == '100':
        ip = gi.ip100()
    elif ip == '102':
        ip = gi.ip102()
    elif ip == '110':
        ip = gi.ip110()
    elif ip == '120':
        ip = gi.ip120()
    if option == 'add':
        if username and ip and mac:
            themessage  = Option(username,ip,mac).addAll()
            if themessage == 'ok':
                flash('Successfully added!')
            else:
                flash(themessage)
        else:
            flash('[Warning] Check your input !!!')
    elif option == 'change':
        Option(username,ip,mac).changeInfo()
        flash('Successfully change !')
    elif  option == 'delete':
        Option(username,ip,mac).deleteInfo()
        flash('Successfully delete !')
    elif  option == 'search':
        for ii in Option(username,ip,mac).findInfo():
            flash('USER:'+str(ii['username'])+' | IP:'+str(ii['ip'])+' | MAC:'+str(ii['mac'])+'\n')
    return redirect(url_for('show_entries'))

@app.route('/list')
def list():
    cur = g.db.execute('select username,department,ip,mac from exits order by department')
    contents = [dict(username=row[0],department=row[1],ip=row[2],mac=row[3]) for row in cur.fetchall()]
    return render_template('list.html',contents=contents)

@app.route('/log')
def log():
    cur = g.db.execute('select time,option from logs order by time desc limit 50')
    contents = [dict(time=row[0],option=row[1]) for row in cur.fetchall()]
    return render_template('log.html',contents=contents)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            Option().exitsInsert()
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))



if __name__ == '__main__':
    app.run()
