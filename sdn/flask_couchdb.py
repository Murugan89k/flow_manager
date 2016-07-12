from flask import Flask, render_template, g, redirect, abort, request, Blueprint
from flask import Blueprint, g, request, session
from OpenSSL import SSL
from config import *
from flask_cors import cross_origin
#from couch import Couch
import json
from uuid import uuid4
import requests


app = Flask(__name__, static_folder='', static_url_path='')

app.secret_key = "opensdn"


@app.route('/')
def show_home():
	return redirect("index.html", code=302)


def connect_db():
	try:
		pass
		#server = couchdbkit.Server()
		#return server.get_or_create_db("sdnhackfest")
	except Exception as e:
		print e
		print "error"

@app.before_request
def db_connect():
	try:
		pass
		#g.db = connect_db()
		#Entry.set_db(g.db)
		#print g.db
	except Exception as e:
		print e
		print "error"

@app.route('/auth', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def auth():
	output = {}
	username = ''
	password = ''
	result = 0
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		login_url = rest_url + "user/_all_docs"
		test = requests.get("http://localhost:5984/user/_design/user/_view/user")
		user_data =  json.loads(test.text)
		for i in user_data["rows"]:
			tmp_user = i["value"]["username"]
			tmp_pass = i["value"]["password"]
			tmp_role = i["value"]["role"]
			if(tmp_user==username and tmp_pass==password):
				session['uid'] = str(uuid4())
				session['username'] = username
				session['logged_in'] = username
				output['logged_in'] = username
				output['username'] = username
				output['role'] = tmp_role
				output['status'] = "0"
				break;
			else:
				output['status'] = "1"
        print output
	return json.dumps(output)



@app.route('/get_all_users', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_all_users():
	output = {}
	tmp_list = []
	flows_url = "http://localhost:5984/user/_design/user/_view/user"
	r = requests.get(flows_url)
	flow_info =  json.loads(r.text)
	return json.dumps(flow_info)

@app.route('/get_toplogy', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_topology():
        output = {}
        tmp_list = []
        flows_url = "http://localhost:5984/flows_bak/_design/flows/_view/flow"
        r = requests.get(flows_url)
        flow_info =  json.loads(r.text)
        return json.dumps(flow_info)

@app.route('/get_switch_info', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_switch_info():
	output = {}
	tmp_list = []
	page = 1;
	page_size = 10;
	if request.method == 'POST':
		json_data = request.get_json()
                page = json_data.get("page", 1)
		page_size = json_data.get("size", 10)
	start = page_size*page
	start = start +1
	flows_url = "http://localhost:5984/flows_bak/_design/flows/_view/flow?skip="+str(start)+"&limit="+str(page_size)
	print flows_url
	r = requests.get(flows_url)
	flow_info =  json.loads(r.text)
	return json.dumps(flow_info)



@app.route('/get_switch', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_switch():
	output = {}
	tmp_list = []
	flows_url = "http://localhost:5984/switches_bak/_all_docs"
	r = requests.get(flows_url)
	flow_info =  json.loads(r.text)
	return json.dumps(flow_info)


@app.route('/delete_flow', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def delete_flow():
	output = {}
	if request.method == 'POST':
		json_data = request.get_json()
		id = json_data.get("id", "")
		rev = json_data.get("rev", "")
		del_id = "http://localhost:5984/flows_bak/"+id+"?rev="+rev
		r = requests.delete(del_id)
		flow_info =  json.loads(r.text)
		return json.dumps(flow_info)

@app.route('/delete_user', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def delete_user():
	output = {}
	if request.method == 'POST':
		json_data = request.get_json()
		id = json_data.get("id", "")
		rev = json_data.get("rev", "")
		del_id = "http://localhost:5984/user/"+id+"?rev="+rev
		r = requests.delete(del_id)
		flow_info =  json.loads(r.text)
		return json.dumps(flow_info)

@app.route('/get_all_flows', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_all_flows():
	output = {}
	tmp_list = []
	flows_url = "http://localhost:5984/flows_bak/_all_docs"
	r = requests.get(flows_url)
	flow_info =  json.loads(r.text)
	return json.dumps(flow_info)

@app.route('/get_flow_info', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_flow_info():
	if request.method == 'POST':
		json_data = request.get_json()
		flow_id = json_data.get("flow_id", "")
		url = "http://localhost:5984/flows_bak/"+flow_id
		print url
		r = requests.get(url)
		info = json.loads(r.text)
		return json.dumps(info)


@app.route('/register_user', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def register_user():
	output = {}
	if request.method == 'POST':
		json_data = request.get_json()
		username = json_data.get("username", "")
		password = json_data.get("password", "")
		role = json_data.get("role", "")
		url = "http://localhost:5984/user/"
		r = requests.post(url, json={"username": username,"password":password,"role":role})
		info = json.loads(r.text)
		return json.dumps(info)

@app.route('/check_session_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def check_session_data():
	try:
		if(session['uid']!=""):
			status = 0
		else:
			status = 1
	except KeyError:
		status = 1
	return str(status)

@app.route('/logout', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def logout():
	session['username'] = None
	session.clear()
	output = {}
	output['result'] = 'success'
	return json.dumps(output)

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")
