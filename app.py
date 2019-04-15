from flask import (Flask, request, jsonify,
					render_template, g, redirect,
					abort)
from flask_restful import Resource, Api, reqparse
from webargs import fields, validate
from webargs.flaskparser import use_args, parser

import sqlite3

from backend import *


APP_CONFIG = {
	"ENV": "development",
	"DEBUG": True,
	"JSON_SORT_KEYS": False
}

# Create the application instance
app = Flask(__name__, template_folder="templates")
app.config.update(APP_CONFIG)
api = Api(app)

# Manage database connection
def connect_db():
	connection = sqlite3.connect('data/geonames.db')
	return connection

connection = connect_db()

def get_db():
	if not hasattr(g, 'db'):
		g.db = connect_db()
	return g.db

@app.teardown_appcontext
def teardown_db(error):
	if hasattr(g, 'db'):
		g.db.close()


# Create a URL route in our application for "/"
@app.route('/')
def home():
	"""
	This function just responds to the browser URL
	localhost:5000/

	:return:		the rendered template 'home.html'
	"""
	return render_template('home.html')

suggestions_args = {
	'q': fields.Str(required=True),
	'latitude': fields.Float(required=False),
	'longitude': fields.Float(required=False)
}

# REST endpoint page
@app.route('/suggestions', methods=['GET'])
@use_args(suggestions_args)
def suggestions_endpoint(args):
	"""

	:return: 		the JSON string with the suggestion
	"""
	conn = get_db()

	q = args['q']
	latitude = None
	longitude = None
	if 'latitude' in args:
		latitude = args['latitude']
	if 'longitude' in args:
		longitude = args['longitude']

	result = get_autocomplete(conn, q, latitude, longitude)

	return jsonify(result)		

# Run the app
if __name__ == '__main__':
	app.run()
