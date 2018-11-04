#!/usr/bin/python3
#PYTHON-MODULE-IMPORTS

#important -> SELECT * from (SELECT * from (SELECT id,sender, receiver, message FROM message WHERE message.sender='hessesim00' AND message.receiver = 'raspi' OR message.receiver = 'hessesim00' AND message.sender = 'raspi' order by id desc limit 32) as test ORDER by id asc limit 16) as test2 ORDER by id DESC
import sys
import logging
logging.basicConfig(filename="/var/www/FlaskApp/FlaskApp/log.log", format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)

from flask import Flask, request,jsonify,url_for,render_template
from flask import json
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#PYTHON-FILE-IMPORTS from /var/www/FlaskApp/FlaskApp/
sys.path.append("/var/www/FlaskApp/FlaskApp/")
from database import *
#from users import *
#from JMS import *
from loginsystem import *
from ED import *
from luca import *
from trash import *

#DATENBANK-OBJEKT
global db
db = Database()

users = {}

@app.route('/')
@app.route('/chat')
def index():
	return render_template('chat.html')

@socketio.on('my event')
def handle_my_custom_event(word):
	socketio.emit('message', 'message:'+word)

@app.route('/test')
def test():
	sender = 'hessesim00'
	receiver = 'raspi'
	response = json.dumps(db.get("SELECT sender, receiver, message FROM message WHERE message.sender=%s AND message.receiver = %s OR message.receiver = %s AND message.sender = %s ",[sender,receiver,sender,receiver]))
	return response

@socketio.on('username')
def receive_username(username):
	users[username] = request.sid
	print('Username added!')
	response = json.dumps(db.get("SELECT receiver FROM message WHERE sender = %s GROUP by receiver UNION SELECT sender FROM message WHERE receiver = %s GROUP by sender",[username,username]))
	socketio.emit('loadChats',response,json=True,room = request.sid)

@socketio.on('private_message')
def private_message(payload):
	recipient_session_id = users[payload['username']]
	message = payload['message']
	sender = payload['sender']
	db.set("INSERT INTO message(sender, receiver, message) VALUES (%s,%s,%s)",[sender,payload['username'],message])
	socketio.emit('new_private_message', {"sender":sender,"message":message}, room=recipient_session_id)

@socketio.on('fetchChat')
def fetchChat(sender,receiver):
	response = json.dumps(db.get("SELECT sender, receiver, message FROM message WHERE message.sender=%s AND message.receiver = %s OR message.receiver = %s AND message.sender = %s order by id desc limit 16",[sender,receiver,sender,receiver]))
	socketio.emit('fetchChatResponse',response,json=True,room = request.sid)



if __name__ == "__main__":
	socketio.run(app,debug=True)
