from flask import Flask, jsonify, request
from distutils.log import debug
from flask_cors import CORS
import pandas as pd
import os
import csv
import json

# creating a Flask app
app = Flask(__name__)
CORS(app)
# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/getRententionStrategy', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):

        data = "Your Retention Strategy is here"
        return jsonify({'data': data})

@app.route('/llm', methods = ['GET', 'POST'])
def llm():
    if(request.method == 'GET'):

        data = "LLM Success"
        return jsonify({'data': data})
# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):

    return jsonify({'data': num**2})

# @app.route('/upload', methods=["GET", "POST"])
# def upload():
#     data = []
#     with open('user_data.csv', 'r') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for row in csv_reader:
#             strategy = generate_retention_strategy(row)
#             data.append(strategy)
#     return jsonify({'data': data})

# driver function
if __name__ == '__main__':

    app.run(debug = True)