from flask import Flask, jsonify, abort
import json
from random import randint
from operator import itemgetter
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)

from models import MemberOfParliament


def send_api_response(data_dict):

    response = jsonify(data_dict)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


@app.route('/')
def route():
    links = [
        '<a href="/get_member/male/">/get_member/male/</a>',
        '<a href="/get_member/female/">/get_member/female/</a>',
        '<a href="/hot/pamela-tshwete/">/hot/pamela-tshwete/</a>',
        '<a href="/not/pamela-tshwete/">/not/pamela-tshwete/</a>',
        '<a href="/ranking/">/ranking/</a>'
    ]
    return "<br>".join(links)


@app.route('/get_member/<gender>/')
def get_member(gender):
    """
    Return the details of a randomly selected member of parliament.
    """

    if not gender.lower() in ["male", "female"]:
        abort(400)

    gender_key = "M"
    if gender.lower() == "female":
        gender_key = "F"


    mp = MemberOfParliament.query.filter_by(gender=gender_key).order_by(func.random()).first()
    return send_api_response(mp.as_dict())


@app.route('/hot/<mp_key>/')
def hot(mp_key):
    """
    Increment the score for an MP.
    """

    try:
        mp = MemberOfParliament.query.filter_by(key=mp_key).first()
        mp.score += 1
    except AttributeError:
        abort(404)
    db.session.add(mp)
    db.session.commit()
    return send_api_response(mp.as_dict())


@app.route('/not/<mp_key>/')
def not_hot(mp_key):
    """
    Decrement the score for an MP.
    """

    try:
        mp = MemberOfParliament.query.filter_by(key=mp_key).first()
        mp.score -= 1
    except AttributeError:
        abort(404)
    db.session.add(mp)
    db.session.commit()
    return send_api_response(mp.as_dict())

@app.route('/ranking/')
def ranking():
    """
    Return the 10 highest ranked MP's of each gender.
    """

    top_males = []
    top_females = []

    males = MemberOfParliament.query.filter_by(gender="M").order_by(MemberOfParliament.score.desc()).limit(10).all()
    for mp in males:
        top_males.append(mp.as_dict())
    females = MemberOfParliament.query.filter_by(gender="F").order_by(MemberOfParliament.score.desc()).limit(10).all()
    for mp in females:
        top_females.append(mp.as_dict())

    return send_api_response({"male": top_males, "female": top_females})