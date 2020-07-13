#!/usr/bin/env python3

import datetime 

from flask import Flask, jsonify, render_template, abort, request, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("user_management.config.Config")

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__   = "users"

    id              = db.Column(db.Integer, primary_key=True)
    birth_day       = db.Column(db.Date)

class Difficulty(db.Model):
    __tablename__   = "difficulties"

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(10), nullable=False)

class Game(db.Model):
    __tablename__   = "games"

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(50), nullable=False, unique=True)

class Progression(db.Model):
    __tablename__   = "progressions"

    id              = db.Column(db.Integer, primary_key=True)
    user            = db.Column(db.Integer, db.ForeignKey('users.id'))
    game            = db.Column(db.Integer, db.ForeignKey('games.id'))
    difficulty      = db.Column(db.Integer, db.ForeignKey('difficulties.id'))
    date_achieved   = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Event(db.Model):
    __tablename__   = "events"

    id              = db.Column(db.Integer, primary_key=True)
    user            = db.Column(db.Integer, db.ForeignKey('users.id'))
    game            = db.Column(db.Integer, db.ForeignKey('games.id'))
    time_produced   = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    event_type      = db.Column(db.String(50), nullable=False)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/ping")
def ping():
    return jsonify(status=200)

@app.route("/difficulty/<int:id>/<string:game_name>", methods = ["GET", "POST"])
@app.route("/difficulty/<string:game_name>/<int:id>", methods = ["GET", "POST"])
def difficulty(id, game_name):
    def get_difficulty(id, game_name):
        game = Game.query.filter_by(name=game_name).first()
        if not game:
            abort(404)

        progression = Progression.query.filter_by(user=id, game=game.id).order_by(Progression.date_achieved.desc()).first()
        if not progression:
            abort(404)
            
        difficulty = Difficulty.query.filter_by(id = progression.difficulty).first()
        if not difficulty:
            abort(404)

        return jsonify(difficulty=difficulty.name)
    
    def post_difficulty(id, game_name):
        game = Game.query.filter_by(name=game_name).first()

        if not request.json or not 'difficulty' in request.json or not game:
            return make_response(400, jsonify(error=400, message="malformed request"))

        if request.json['difficulty'] < 0 or request.json['difficulty'] > 2:
            return make_response(401, jsonify(error=400, message="malformed request"))

        db.session.add(Progression(user = id, game = game.id, difficulty = request.json['difficulty']))
        db.session.commit()

        return jsonify(status=200)

    if request.method == 'GET':
        return get_difficulty(id, game_name)
    elif request.method == 'POST':
        return post_difficulty(id, game_name)

if __name__ == "__main__":
    app.run()
