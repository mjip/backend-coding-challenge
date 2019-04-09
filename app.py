from flask import (Flask, request, jsonify,
					render_template, g, redirect,
					abort)
from flask_restful import Resource, Api, reqparse
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser

import sqlite3

from backend import *


APP_CONFIG = {
	"ENV": "development",
	"DEBUG": True,
	"IMAGE_FOLDER": 'static/img'
}

# Create the application instance
app = Flask(__name__, template_folder="templates")
app.config.update(APP_CONFIG)
api = Api(app)

# Manage database connection
def connect_db():
	connection = sqlite3.connect('geonames.db')
	return connection

connection = connect_db()

def get_db():
	if not hasattr(g, 'db'):
		g.db = connect_db()
	return g.db

@app.teardown_appcontext
def teardown_db(error):
	if hasattr(g, 'db'):
		db.close()


# Create a URL route in our application for "/"
@app.route('/')
def home():
	"""
	This function just responds to the browser URL
	localhost:5000/

	:return:		the rendered template 'home.html'
	"""
	return render_template('home.html')


# REST endpoint page
@app.route('/suggestions', methods=['GET'])
def suggestions_endpoint():
	"""

	:return: 		the JSON string with the suggestion
	"""
	conn = get_db()

	args = request.args

	# If query not specified, return empty dict with no suggestions key
	if 'q' not in args:	return {}

	query = args['q']
	if 'lat' in args: 
		latitude = args['lat'] 
	else: 
		latitude = None
	if 'long' in args: 
		longitude = args['long'] 
	else: 
		longitude = None

	print(query)
	print(latitude)
	print(longitude)

	result = {"suggestions": []}
	return jsonify(result)		

# Run the app
if __name__ == '__main__':
	app.run()
