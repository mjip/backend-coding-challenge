from flask import (Flask, request, jsonify,
					render_template, g, redirect,
					abort)

from backend import *


APP_CONFIG = {
	"ENV": "development",
	"DEBUG": True,
	"IMAGE_FOLDER": 'static/img'
}

# Create the application instance
app = Flask(__name__, template_folder="templates")
app.config.update(APP_CONFIG)

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
@app.route("/suggestions", methods=["GET", "POST"])
def suggestions_controller():
	"""
	
	:return:		the JSON string with the suggestion
	"""
	pass


if __name__ == '__main__':
	app.run()
