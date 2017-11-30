#!/usr/bin/python
# -*- coding: utf-8 -*-
# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, json, jsonify
from contextlib import closing
from option import Option  
from logs import Logs
from theFtp import OpFtp
import json
import sys
import time
reload(sys)  
sys.setdefaultencoding('utf8')

# configuration
DEBUG = True
DATABASE = 'theoption.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'
op = Option()
ftp = OpFtp()
thelog = Logs()
Departments = {'jishu':'技术部','yanfa':'研发部','shichang':'市场部','xingzheng':'行政部','caiwu':'财务部'}
add_time = time.strftime('%Y-%m-%d %H:%M:%S')

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
def index():
    if not session.get('logged_in'):
        return redirect(url_for('userapply'))
    else:
        cur = g.db.execute('select id, jobnum, zh_username, username, password, department, time from users order by id')
        contents = [dict(id=row[0],jobnum=row[1], zh_username=row[2],username=row[3],password=row[4],department=row[5], time=row[6]) for row in cur.fetchall()]
        return render_template('index.html', contents=contents)


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/log')
def log():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    cur = g.db.execute('select * from logs order by id desc')
    contents = [dict(id=row[0],options=row[1],time=row[2]) for row in cur.fetchall()]
    return render_template('log.html', contents=contents)


@app.route('/option')
def option():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    return render_template('option.html')


@app.route('/add', methods=['POST'])
def add_user():
    user1=request.form['zh_username']
    user2=request.form['username']
    jobnum = request.form['jobnum']
    ps=request.form['password']
    de=request.form['options']
    department=Departments[de]
    flash(op.addUsers(jobnum, user1, user2, ps, department))
    return redirect(url_for('option'))


@app.route('/apply', methods=['POST'])
def apply_user():
    jobnum = request.form['jobnum']
    user1=request.form['zh_username']
    user2=request.form['username']
    ps=request.form['password']
    de=request.form['options']
    department=Departments[de]
    g.db.execute('insert into apply (jobnum, zh_username, username, password, department, time, status) values ("%s","%s","%s","%s","%s","%s","%s")'%(jobnum, user1, user2, ps, department, add_time,"n"))
    g.db.commit()
    flash("Submit the application successfully !")
    return redirect(url_for("index"))


@app.route('/userapply')
def userapply():
    return render_template('apply.html')


@app.route('/opa')
def option_apply():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    cur = g.db.execute('select * from apply where status = "n"')
    contents = [dict(id=row[0], jobnum=row[1], zh_username=row[2], username=row[3], password=row[4], department=row[5],time=row[6]) for row in cur.fetchall()]
    return render_template('option_apply.html', contents=contents)


@app.route('/user<int:id>')
def user(id):
    cur = g.db.execute('select id, zh_username, username, password, department, time from users order by id')
    contents = [dict(id=row[0],zh_username=row[1],username=row[2],password=row[3],department=row[4], time=row[5]) for row in cur.fetchall()]
    return render_template('user.html', contents=contents)

@app.route('/change<int:id>', methods=['POST'])
def change(id):
    zh_username = request.form['zh_username']
    username = request.form['username']
    password = request.form['password']
    department = request.form['department']
    logtime = time.strftime('%Y-%m-%d %H:%M:%S')
    g.db.execute('update users set zh_username = ?, username = ?, password = ?, department = ?, time = ? where id = ?',[zh_username,username,password,department,add_time,id])
    g.db.commit()
    return redirect(url_for('index'))

@app.route('/theuser<int:id>')
def theuser(id):
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    cur = g.db.execute('select * from users where id = ?',[id])
    contents = [dict(id=row[0],jobnum=row[1], zh_username=row[2],username=row[3],password=row[4],department=row[5], time=row[6]) for row in cur.fetchall()]
    user_id = contents[0]['id']
    return render_template('user.html',contents=contents,user_id=user_id)

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
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    #ftp.ftpquit()
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/remove', methods=['POST'])
def remove_id():
    data = request.get_data()
    theid = str(json.loads(data)['theid'])
    thestatus = str(json.loads(data)['status'])
    if thestatus == "apply":
        contents = [dict(jobnum=row[0], zh_username=row[1], username=row[2], password=row[3], department=row[4]) for row in g.db.execute('select jobnum,zh_username,username,password,department from apply where id = ?',[theid]).fetchall()][0]
        op.addUsers(contents['jobnum'], contents['zh_username'], contents['username'], contents['password'], contents['department'])
        g.db.execute('update apply set status = "y" where id = ?',[theid])
        g.db.commit()
        result = [i.strip() for i in os.popen('useradd -d /var/ftp/%s -g ftp -s /sbin/nologin %s'%(contents['username'],contents['username'])).readlines()][0] 
        if result == "":
#            os.system('echo %s | passwd %s --stdin'%(contents['password'],contents['username'])
            thelog.addlog('批准用户申请 %s'%(contents['zh_username']))
        else:
            thelog.addlog(result)
    elif thestatus == "removeapply":
        g.db.execute('update apply set status = "x" where id = ?',[theid])
        contents = [dict(zh_username=row[0]) for row in g.db.execute('select zh_username from apply where id = ?',[theid]).fetchall()][0]
        g.db.commit()
        thelog.addlog('驳回用户申请 %s'%(contents['zh_username']))
    elif thestatus == "option":
        cur = g.db.execute('select zh_username from users where id = ?',[theid])
        g.db.execute('delete from users where id = ?',[theid])
        g.db.commit()
        contents = [dict(zh_username=row[0]) for row in cur.fetchall()]
        op.delUsers(contents[0]['zh_username']) 
    return redirect(url_for('index'))

@app.route('/joy')
def joy():
    return render_template('joy.html')


@app.route('/num', methods=['POST'])
def num():
    contents = [row for row in g.db.execute('select id from apply where status = "n"').fetchall()][0]
    num = dict()
    info['num'] = str(len(contents))
    return jsonify(info)

if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True)
