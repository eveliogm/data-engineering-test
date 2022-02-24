
from flask import Flask, jsonify
from osmbigquery import get_restaurants_bq
from query import query_bq
import pathlib
import os

app = Flask(__name__)

@app.route('/getRestaurants', methods = ['GET'])
def get():
	return jsonify({"filename":get_restaurants_bq(query_bq)})

if __name__ == '__main__':
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(pathlib.Path().absolute())+'/gc_credentials.json'
	app.run(debug=True, host = '0.0.0.0',port=4000) 
