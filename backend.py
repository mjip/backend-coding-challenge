"""
	Contains all the backend functions that retrieve and compute autocomplete
	suggestions from the geonames database.
"""
import sqlite3, math
from collections import OrderedDict


def get_autocomplete(conn, q:str, qlatitude:float, qlongitude:float):
	"""

	:return: autocomplete suggestion in a dict
	"""
	try:
		c = conn.cursor()
		c.execute("SELECT name, alt_name, admin1, latitude, longitude, country, population FROM geonames WHERE name LIKE ?", (q+'%',))
		result = c.fetchall()

		c.execute("SELECT name, alt_name, admin1, latitude, longitude, country, population FROM geonames WHERE alt_name LIKE ?", ('%'+q+'%',))
		alt_result = c.fetchall()

	except:
		c.close()
		return {"suggestions":[]}		

	c.close()

	alt_results_used = False
	if not result and alt_result:
		result = alt_result
		alt_results_used = True
	elif not result and not alt_result:
		return {"suggestions":[]} 

	suggestion_entities = []
	for tupl in result:
		name = tupl[0]
		alt_name = tupl[1]
		admin1 = tupl[2]
		latitude = float(tupl[3])
		longitude = float(tupl[4])
		country = tupl[5]
		population = tupl[6]
		score = 0.0

		# Convert numbers to Canada's province codes
		if str.isdigit(admin1):
			admin1 = convert_to_province_code(admin1)

		if alt_results_used:
			suggestion_entity = OrderedDict({'name': name + ', ' + admin1 + ', ' + country, 'alt_name': alt_name, 'latitude': latitude, 'longitude': longitude, 'population': population, 'score': score})
		else:
			suggestion_entity = OrderedDict({'name': name + ', ' + admin1 + ', ' + country, 'latitude': latitude, 'longitude': longitude, 'population': population, 'score': score})

		suggestion_entities.append(suggestion_entity)

	if qlatitude or qlongitude:
		suggestion_entities = compute_loc_score_metric(suggestion_entities, qlatitude, qlongitude)
	else:
		suggestion_entities = compute_pop_score_metric(suggestion_entities)

	return {"suggestions": suggestion_entities}


def convert_to_province_code(admin1:str):
	"""
	Converts int to two-letter Canadian province code

	:return: two-letter province code 
	"""
	prov_codes = ["AB", "BC", "MB", "NB", "NL", "", "NS", "ON", "PE", "QC", "SK", "YT", "NT", "NU"]
	digits = int(admin1)
	return prov_codes[digits-1]


def compute_pop_score_metric(suggestion_entities):
	"""
	 Score is given based on the population proportional to the total population:
	score = population / sum of all populations

	:return: list of dictionaries representing suggestion entities, with the score computed
	"""

	populations = [se['population'] for se in suggestion_entities]
	total_pop = sum(populations)

	for se in suggestion_entities:
		pop = se['population']
		score = pop / total_pop
		se['score'] = format(score, '.2f')

	suggestion_entities = sorted(suggestion_entities, key=lambda k: k['score'], reverse=True)

	return suggestion_entities


def compute_loc_score_metric(suggestion_entities, lat_center, long_center):
	"""
	Score is given based on the inverse Euclidean distance

	:return: list of dictionaries representing suggestion entities, with the score computed
	"""

	latitudes = [se['latitude'] for se in suggestion_entities]
	longitudes = [se['longitude'] for se in suggestion_entities]
	distances = []	

	# Compute scores even if one of latitude/longitude wasn't specified.
	# Populate suggestion_entities scores after all Euclidean distances have
	# been calculated
	for i in range(len(latitudes)):
		if not long_center and lat_center:
			dist = abs(latitudes[i] - lat_center)
		elif not lat_center and long_center:
			dist = abs(longitudes[i] - long_center)
		else:
			dist = math.sqrt(math.pow(abs(latitudes[i] - lat_center),2) + math.pow(abs(longitudes[i] - long_center), 2))
		distances.append(dist)

	total_distance = sum(distances)

	for i in range(len(suggestion_entities)):
		if len(suggestion_entities) == 1:
			score = 1.0
		else:
			score = 1.0 - (distances[i] / total_distance)
		suggestion_entities[i]['score'] = format(score, '.2f')

	suggestion_entities = sorted(suggestion_entities, key=lambda k: k['score'], reverse=True)

	return suggestion_entities
	
