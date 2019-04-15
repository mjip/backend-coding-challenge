# my-autocomplete

http://autocomplete-mjip-challenge.me 

My submission of the backend challenge for Coveo.
- Author: Marie Payne

Table of Contents
=================
* [The Framework](#the-framework)
* [How It Works](#how-it-works)
	* [The Endpoint](#the-endpoint)
	* [Examples](#examples)
	* [Scoring Metrics](#scoring-metrics)
* [Installation](#installation)
* [Ideas for Future Features](#ideas-for-future-features)


## The Framework
I choose to deploy the REST endpoint as a Flask app, a Python web framework I'm already familiar with. Flask doesn't validate queries out-of-the-box, so I also employed Flask-RESTful and webargs. The data is stored in a PostgreSQL database.
I deployed it through the free-tier of AWS EC2 and grabbed a free domain through the student benefits pack on Namecheap.

## How It Works
The landing page links back to the Github repository, https://github.com/mjip/backend-coding-challenge. 

### The Endpoint
I've created a REST API endpoint that will provide autocomplete suggestions in JSON format, exposed at `/suggestions`. 
Simply pass the partial search term through the query parameter `q` and a list of possible locations will be returned with a score based on how likely it read your mind. Location coordinates can be optionally passed with `latitude` and `longitude` parameters. 

### Examples
`GET /suggestions?q=abb`

```JSON
{
  "suggestions": [
    {
      "name": "Abbotsford, BC, CA", 
      "longitude": -122.25256999999999, 
      "latitude": 49.05798, 
      "population": 151683, 
      "score": "0.90"
    }, 
    {
      "name": "Abbeville, LA, US", 
      "longitude": -92.13429000000001, 
      "latitude": 29.97465, 
      "population": 12257, 
      "score": "0.07"
    }, 
    {
      "name": "Abbeville, SC, US", 
      "longitude": -82.37901, 
      "latitude": 34.17817, 
      "population": 5237, 
      "score": "0.03"
    }
  ]
}
```

`GET /suggestions?q=columbus&longitude=-88`

```JSON
{
  "suggestions": [
    {
      "name": "Columbus, MS, US", 
      "longitude": -88.42726, 
      "latitude": 33.495670000000004, 
      "population": 23640, 
      "score": "0.96"
    }, 
    {
      "name": "Columbus, IN, US", 
      "longitude": -85.92138, 
      "latitude": 39.201440000000005, 
      "population": 44061, 
      "score": "0.80"
    }, 
    {
      "name": "Columbus, GA, US", 
      "longitude": -84.98770999999999, 
      "latitude": 32.46098, 
      "population": 189885, 
      "score": "0.71"
    }, 
    {
      "name": "Columbus, OH, US", 
      "longitude": -82.99879, 
      "latitude": 39.96118, 
      "population": 787033, 
      "score": "0.52"
    }
  ]
}
```

If no results are returned, it also searches among alternative names in the database.

`GET /suggestions?q=YXX`

```JSON
{
  "suggestions": [
    {
      "alt_name": "Abbotsford,YXX,Абботсфорд", 
      "latitude": 49.05798, 
      "score": "1.00", 
      "longitude": -122.25256999999999, 
      "name": "Abbotsford, BC, CA", 
      "population": 151683
    }
  ]
}
```

### Scoring Metrics
Each suggestion is scored according to a simple metric based on how likely the location is what you meant. For queries without location parameters, it will calculate the score as a weight of the suggestion's population (a weighted probability). For queries with latitude and longitude specified, it will calculate the Euclidean distance and use the inverse weighted probability (so smaller distances will rank higher). 

## Installation
My application was developed on a Ubuntu 18.04 machine. I'm using pipenv to manage packages and manipulate the virtual environment, but I've included a `requirements.txt` with package versions for the uninitiated.
To install pipenv, run:
```bash
# Installing pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py

# Installing pipenv
sudo pip install pipenv
```

To run the app on your localhost, clone this repository, launch pipenv and run `app.py` within its shell:
```bash
git clone https://github.com/mjip/backend-coding-challenge
cd backend-coding-challenge

pipenv install
pipenv shell

python app.py
```
Navigate to the address it outputs after launching to view the landing page.

## Ideas for Future Features
Since I deployed it on AWS, I could have also used the database to track how many times a particular result is queried and performed some analytics to better serve my endpoint userbase (i.e. pretty much just me). I could keep track of query results over time to evaluate trends and learn user behaviour to better evaluate suggestions. 
