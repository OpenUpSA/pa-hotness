from flask import Flask, jsonify, abort
import json
from random import randint
from operator import itemgetter

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py', silent=True)

with app.open_instance_resource('mp_details.json') as f:
    mp_details = json.loads(f.read())

    mp_list = []
    for key, val in mp_details.iteritems():
        mp_list.append(key)


def save_data():

    file = open("instance/mp_details.json", "w")
    file.write(json.dumps(mp_details, indent=4))
    file.close()
    return


@app.route('/get_member/')
def get_member():
    """
    Return the details of a randomly selected member of parliament.
    """

    i = randint(0, len(mp_details)-1)
    return jsonify({"id": mp_list[i], "data": mp_details[mp_list[i]]})


@app.route('/hot/<mp_id>/')
def hot(mp_id):
    """
    Increment the score for an MP.
    """

    try:
        mp = mp_details[mp_id]
        if not mp.get('score'):
            mp['score'] = 0
        mp['score'] += 1
    except KeyError:
        abort(404)
    save_data()
    return jsonify({"id": mp_id, "data": mp})


@app.route('/not/<mp_id>/')
def not_hot(mp_id):
    """
    Decrement the score for an MP.
    """

    try:
        mp = mp_details[mp_id]
        if not mp.get('score'):
            mp['score'] = 0
        mp['score'] -= 1
    except KeyError:
        abort(404)
    save_data()
    return jsonify({"id": mp_id, "data": mp})


@app.route('/ranking/')
def ranking():
    """
    Return the 20 highest ranked MP's.
    """

    tmp = []
    for mp_id in mp_list:
        tmp.append({'mp_id': mp_id, 'score': mp_details[mp_id]['score']})
    tmp = sorted(tmp, key=itemgetter('score'))
    tmp.reverse()
    out = {}
    for i in range(min(tmp, 10)):
        rec = tmp[i]
        mp = {"id": rec['mp_id'], "data": mp_details[rec['mp_id']]}
        out[i+1] = mp
    print out
    return jsonify(out)