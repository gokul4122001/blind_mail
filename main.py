import os
import base64
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
#import algm
from datetime import date
import datetime
import calendar
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import hashlib
#import xlrd 
from flask import send_file
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  use_pure=True,
  database="blind_mail"

)

#from store import *


app = Flask(__name__)
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####


@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""
    res=""
    st=""
    act = request.args.get('act')
    if request.method=='POST':
        res=request.form['res']
        if res=="login" or res=="Login." or res=="Log in.":
            print("login")
            return redirect(url_for('home'))
        elif res=="register" or res=="Register.":
            print("register")
            return redirect(url_for('reg1'))
        else:
            st="1"

    if res=="":
        st="1"
        
    return render_template('index.html',msg=msg,st=st)

@app.route('/reg1', methods=['GET', 'POST'])
def reg1():
    msg=""
    res=""
    st=""
    act = request.args.get('act')
    mycursor = mydb.cursor()
            
    if request.method=='POST':
        res=request.form['res']

        if res=="":
            st="1"
        else:
            name=res.lower()
            print(name)
            mycursor.execute("SELECT max(id)+1 FROM register")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
        
            sql = "INSERT INTO register(id,name,gender,contact,username,password,rdate) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,'','0','','',rdate)
            mycursor.execute(sql, val)
            mydb.commit()            
            
            result="success"
            return redirect(url_for('reg2',uid=str(maxid)))

    if res=="":
        st="1"
        
    return render_template('reg1.html',msg=msg,st=st)

@app.route('/reg2', methods=['GET', 'POST'])
def reg2():
    msg=""
    res=""
    st=""
    uid = request.args.get('uid')
    act = request.args.get('act')
    mycursor = mydb.cursor()
            
    if request.method=='POST':
        res=request.form['res']

        if res=="":
            st="1"
        else:
            name=res.lower()
            mycursor.execute("update register set gender=%s where id=%s",(name,uid))
            mydb.commit()            
            
            result="success"
            return redirect(url_for('reg3',uid=uid))

    if res=="":
        st="1"
        
    return render_template('reg2.html',msg=msg,st=st)

@app.route('/reg3', methods=['GET', 'POST'])
def reg3():
    msg=""
    res=""
    st=""
    uid = request.args.get('uid')
    act = request.args.get('act')
    mycursor = mydb.cursor()
            
    if request.method=='POST':
        res=request.form['res']

        if res=="":
            st="1"
        else:
            name=res.lower()
            mycursor.execute("update register set city=%s where id=%s",(name,uid))
            mydb.commit()            
            
            result="success"
            return redirect(url_for('reg4',uid=uid))

    if res=="":
        st="1"
        
    return render_template('reg3.html',msg=msg,st=st)

@app.route('/reg4', methods=['GET', 'POST'])
def reg4():
    msg=""
    res=""
    st=""
    uid = request.args.get('uid')
    act = request.args.get('act')
    mycursor = mydb.cursor()
            
    if request.method=='POST':
        res=request.form['res']

        if res=="":
            st="1"
        else:
            name=res.lower()
            mycursor.execute("update register set username=%s where id=%s",(name,uid))
            mydb.commit()            
            
            result="success"
            return redirect(url_for('reg5',uid=uid))

    if res=="":
        st="1"
        
    return render_template('reg4.html',msg=msg,st=st)

@app.route('/reg5', methods=['GET', 'POST'])
def reg5():
    msg=""
    res=""
    st=""
    uid = request.args.get('uid')
    act = request.args.get('act')
    mycursor = mydb.cursor()
            
    if request.method=='POST':
        res=request.form['res']

        if res=="":
            st="1"
        else:
            name=res.lower()
            mycursor.execute("update register set password=%s where id=%s",(name,uid))
            mydb.commit()            
            
            result="success"
            return redirect(url_for('home'))

    if res=="":
        st="1"
        
    return render_template('reg5.html',msg=msg,st=st)

@app.route('/home', methods=['GET', 'POST'])
def home():
    msg=""
    res=""
    st=""
    act = request.args.get('act')
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        res=request.form['res']
        if res=="":
            st="1"
        else:
            name=res.lower()
            mycursor.execute('SELECT * FROM register WHERE username = %s', (name, ))
            account = mycursor.fetchone()
            if account:
                ff=open("log.txt","w")
                ff.write(name)
                ff.close()
                return redirect(url_for('index2',uname=name))
            else:
                st="2"
                msg = 'Incorrect username/password!'
            
    if res=="":
        st="1"    
        
        
    return render_template('home.html',msg=msg,act=act,st=st)

@app.route('/index2', methods=['GET', 'POST'])
def index2():
    msg=""
    res=""
    st=""
    uname=request.args.get("uname")
    act = request.args.get('act')
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        res=request.form['res']
        if res=="":
            st="1"
        else:
            name=res.lower()
            mycursor.execute('SELECT * FROM register WHERE username = %s and password=%s', (uname, name))
            account = mycursor.fetchone()
            if account:
                session['username'] = uname
                return redirect(url_for('inbox'))
            else:
                st="2"
                msg = 'Incorrect username/password!'
            
    if res=="":
        st="1"    
        
        
    return render_template('index2.html',msg=msg,act=act,st=st)

@app.route('/inbox', methods=['GET', 'POST'])
def inbox():
    msg=""
    res=""
    rid=""
    st=""
    mess=""
    act = request.args.get('act')
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      charset="utf8",
      use_pure=True,
      database="blind_mail"

    )
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("log.txt","r")
    uname1=ff.read()
    ff.close()
    if uname is None:
        uname=uname1
    data1=[]
    data2=[]
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM register WHERE username = %s', (uname, ))
    data = mycursor.fetchone()

    mycursor.execute('SELECT * FROM receiver WHERE send_to = %s order by id desc', (uname, ))
    data2 = mycursor.fetchall()

    mycursor.execute("select count(*) from receiver where send_to=%s && view_st=0",(uname,))
    read_n = mycursor.fetchone()[0]

    mycursor.execute('SELECT count(*) FROM receiver WHERE uname = %s order by id desc', (uname, ))
    dd1 = mycursor.fetchone()[0]
    if dd1>0:
        mycursor.execute('SELECT * FROM receiver WHERE uname = %s order by id desc', (uname, ))
        dd = mycursor.fetchone()
        rid=dd[0]
            
    if request.method=='POST':
        res=request.form['res']
        
        if res=="compose" or res=="Compose.":
            
            return redirect(url_for('compose1'))
        elif res=="inbox" or res=="Inbox.":
            
            return redirect(url_for('inbox'))
        elif res=="sent" or res=="Send." or res=="Sent." or res=="Sent Box." or res=="Send Box.":
            
            return redirect(url_for('inbox_view2',rid=rid))
        elif res=="logout" or res=="Log out.":
            
            return redirect(url_for('logout'))
        elif res=="unread" or res=="Unread.":
            mycursor.execute('SELECT count(*) FROM receiver WHERE send_to = %s && view_st=0', (uname, ))
            d1 = mycursor.fetchone()[0]
            if d1>0:
                mycursor.execute('SELECT * FROM receiver WHERE send_to = %s && view_st=0', (uname, ))
                dd2 = mycursor.fetchone()
                return redirect(url_for('inbox_view',rid=str(dd2[0])))
                st="2"
            else:
                st="3"
                mess="No Unread Messages found"
            
        else:
            st="1"

    if res=="":
        st="1"
    return render_template('inbox.html',msg=msg,act=act,st=st,data=data,data2=data2,read_n=read_n,mess=mess)

@app.route('/compose1', methods=['GET', 'POST'])
def compose1():
    msg=""
    res=""
    st=""
    act = request.args.get('act')
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
            
    if request.method=='POST':
        res=request.form['res']

        if res=="":
            st="1"
        else:
            name=res.lower()
            print(name)
            mycursor.execute("SELECT max(id)+1 FROM receiver")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
        
            sql = "insert into receiver(id,uname,send_to,subject,message,rdate) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (maxid,uname,name,'','',rdate)
            mycursor.execute(sql, val)
            mydb.commit()            
            
            result="success"
            return redirect(url_for('compose2',uid=str(maxid)))

    if res=="":
        st="1"
        
    return render_template('compose1.html',msg=msg,st=st)

@app.route('/compose2', methods=['GET', 'POST'])
def compose2():
    msg=""
    res=""
    st=""
    uid = request.args.get('uid')
    act = request.args.get('act')
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
            
    if request.method=='POST':
        res=request.form['res']

        if res=="":
            st="1"
        else:
            name=res.lower()
            mycursor.execute("update receiver set subject=%s where id=%s",(name,uid))
            mydb.commit()            
            
            result="success"
            return redirect(url_for('compose3',uid=uid))

    if res=="":
        st="1"
        
    return render_template('compose2.html',msg=msg,st=st)

@app.route('/compose3', methods=['GET', 'POST'])
def compose3():
    msg=""
    res=""
    st=""
    uid = request.args.get('uid')
    act = request.args.get('act')
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
            
    if request.method=='POST':
        res=request.form['res']

        if res=="":
            st="1"
        else:
            name=res.lower()
            mycursor.execute("update receiver set message=%s where id=%s",(name,uid))
            mydb.commit()            
            
            result="success"
            return redirect(url_for('userhome'))

    if res=="":
        st="1"
        
    return render_template('compose3.html',msg=msg,st=st)

@app.route('/compose4', methods=['GET', 'POST'])
def compose4():
    msg=""
    res=""
    st=""
    uid = request.args.get('uid')
    act = request.args.get('act')
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
            
    if request.method=='POST':
        res=request.form['res']
        file=request.files['file']
        if res=="":
            st="1"
        elif res=="Inbox.":
            return redirect(url_for('inbox'))
        if file=="":
            print("")
        else:
            name=res.lower()

            fname = file.filename
            f1="C"+uid+fname
            filename = secure_filename(f1)
            file.save(os.path.join("static/upload/", filename))
        
            mycursor.execute("update receiver set pimage=%s where id=%s",(filename,uid))
            mydb.commit()            
            
            result="success"
            return redirect(url_for('userhome'))

    if res=="":
        st="1"
        
    return render_template('compose4.html',msg=msg,st=st)

@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    res=""
    st=""
    act = request.args.get('act')
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      charset="utf8",
      use_pure=True,
      database="blind_mail"

    )
    uname=""
    if 'username' in session:
        uname = session['username']
    data1=[]
    data2=[]
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM register WHERE username = %s', (uname, ))
    data = mycursor.fetchone()

    mycursor.execute('SELECT * FROM receiver WHERE uname = %s order by id desc', (uname, ))
    dd = mycursor.fetchone()
    rid=dd[0]
            
    if request.method=='POST':
        res=request.form['res']
        
        if res=="compose" or res=="Compose.":
            
            return redirect(url_for('compose1'))
        elif res=="inbox" or res=="Inbox.":
            
            return redirect(url_for('inbox'))
        elif res=="sent" or res=="Send." or res=="Sent." or res=="Sent Box." or res=="Send Box.":
            
            return redirect(url_for('inbox_view2',rid=rid))
        elif res=="logout" or res=="Log out.":
            
            return redirect(url_for('logout'))
        else:
            st="1"

    if res=="":
        st="1"
    return render_template('userhome.html',msg=msg,act=act,st=st,data=data)



@app.route('/sent', methods=['GET', 'POST'])
def sent():
    msg=""
    uname=""
    st=""
    res=""
    act = request.args.get('act')
    lat=""
    lon=""
    read_n=0
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM register where username=%s",(uname,))
    data = mycursor.fetchone()

    mycursor.execute('SELECT * FROM receiver WHERE uname = %s order by id desc', (uname, ))
    data2 = mycursor.fetchall()

    mycursor.execute('SELECT * FROM receiver WHERE uname = %s order by id desc', (uname, ))
    dd = mycursor.fetchone()
    rid=dd[0]

    if request.method=='POST':
        res=request.form['res']
        
        if res=="compose" or res=="Compose.":
            
            return redirect(url_for('compose1'))
        elif res=="inbox" or res=="Inbox.":
            
            return redirect(url_for('inbox'))
        elif res=="sent" or res=="Send." or res=="Sent." or res=="Sent Box." or res=="Send Box.":
            
            return redirect(url_for('inbox_view2',rid=rid))
        elif res=="logout" or res=="Log out.":
            
            return redirect(url_for('logout'))
        else:
            st="1"

    if res=="":
        st="1"

    return render_template('sent.html',msg=msg,st=st,act=act,data=data,data2=data2,read_n=read_n)

@app.route('/inbox_view', methods=['GET', 'POST'])
def inbox_view():
    msg=""
    uname=""
    st=""
    rid=request.args.get("rid")

    f2=open("result.txt",'r')
    res=f2.read()
    f2.close()
            
    
    if 'username' in session:
        uname = session['username']
        
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM register where username=%s",(uname,))
    data = mycursor.fetchone()


    mycursor.execute("select count(*) from receiver where send_to=%s && view_st=0",(uname,))
    read_n = mycursor.fetchone()[0]

    mycursor.execute("SELECT * FROM receiver where id=%s",(rid,))
    data2 = mycursor.fetchone()

    

    st="Message from "+data2[2]+", "+data2[4]+", "+data2[5]+", "+str(data2[7])

    mycursor.execute("update receiver set view_st=1 where id=%s",(rid,))
    mydb.commit()

    
    return render_template('inbox_view.html',msg=msg,data=data,read_n=read_n,data2=data2,st=st)

@app.route('/inbox_view2', methods=['GET', 'POST'])
def inbox_view2():
    msg=""
    uname=""
    st=""
    rid=request.args.get("rid")

    f2=open("result.txt",'r')
    res=f2.read()
    f2.close()
            
    
    if 'username' in session:
        uname = session['username']
        
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM register where username=%s",(uname,))
    data = mycursor.fetchone()


    mycursor.execute("select count(*) from receiver where send_to=%s && view_st=0",(uname,))
    read_n = mycursor.fetchone()[0]

    mycursor.execute("SELECT * FROM receiver where id=%s",(rid,))
    data2 = mycursor.fetchone()

    

    st="Message from "+data2[2]+", "+data2[4]+", "+data2[5]+", "+str(data2[7])

    #mycursor.execute("update receiver set view_st=1 where id=%s",(rid,))
    #mydb.commit()

    
    return render_template('inbox_view2.html',msg=msg,data=data,read_n=read_n,data2=data2,st=st)

@app.route('/down', methods=['GET', 'POST'])
def down():
    fn = request.args.get('fname')
    path="static/upload/"+fn
    return send_file(path, as_attachment=True)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
