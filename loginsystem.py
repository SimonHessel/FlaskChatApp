import sys
sys.path.insert(0,"/var/www/FlaskApp/")
from FlaskApp import app
from FlaskApp import jsonify,request,render_template
from flask import Flask, session, redirect, url_for, escape, request, render_template
from database import *

global db
db = Database()

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username_form = request.form['username']
        password_form= request.form['password']
        if db.get("SELECT COUNT(*) FROM users WHERE username = %s AND password = %s", [username_form,password_form])[0][0] > 0:
            return '''
<!DOCTYPE html>
<html lang="de" dir="ltr">
<head>
<meta charset="utf-8">
</head>
<body>
<script type="text/javascript">
localStorage.setItem("username","'''+username_form+'''");
window.location.replace("http://facharbeit-app.ddns.net:5000/chat");
</script
</body>
</html>
            '''
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/register',methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        lastname_form = request.form['lastName']
        firstname_form= request.form['firstName']
        username_form = request.form['username']
        password_form= request.form['password']
        db.set("INSERT INTO users (lastName, firstName,username, password) VALUES (%s,%s,%s,%s)", (lastname_form,firstname_form,username_form,password_form))
        return render_template('login.html')
    else:
        return render_template('register.html')

@app.route('/forgot-password',methods = ['POST', 'GET'])
def forgot_password():
    if request.method == 'POST':
        lastname_form = request.form['email']
        return render_template('login.html')
    else:
        return render_template('forgot-password.html')
