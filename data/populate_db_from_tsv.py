import csv
import pandas as pd
import sqlite3

"""
	Basic script to import data from tsv file into sqlite db.
"""

INSERT_STATEMENT = "INSERT INTO geonames (id, name, ascii_name, alt_name, latitude, longitude, feat_class, feat_code, country, cc2, admin1, admin2, admin3, admin4, population, elevation, dem, tz, modified_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"

string_attribs = ['name', 'ascii', 'alt_name', 'feat_class', 'feat_code', 'country', 'cc2', 'admin1', 'admin2', 'admin3', 'admin4', 'tz', 'modified_at']

try:
	conn = sqlite3.connect('geonames.db')
	c = conn.cursor()
	with open('cities_canada-usa.tsv', 'rb') as tsvin:
		df = pd.read_csv(tsvin, sep='\t')
	
		for index, row in df.iterrows():
			for key in row.keys():
				if row[key] == "nan": row[key] = None

			r = c.execute(INSERT_STATEMENT, ((row['id'], row['name'], row['ascii'], row['alt_name'], row['lat'], row['long'], row['feat_class'], row['feat_code'], row['country'], row['cc2'], row['admin1'], row['admin2'], row['admin3'], row['admin4'], row['population'], row['elevation'], row['dem'], row['tz'], row['modified_at'])))
			conn.commit()
			print(r)

except:
	print(c.execute("SELECT * FROM geonames;").fetchall())
	conn.close()
	
