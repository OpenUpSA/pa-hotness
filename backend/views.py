from flask import Flask, jsonify
import json

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py', silent=True)

with app.open_instance_resource('mp_details.json') as f:
    mp_details = json.loads(f.read())

@app.route('/')
def root():

    return jsonify(mp_details)

