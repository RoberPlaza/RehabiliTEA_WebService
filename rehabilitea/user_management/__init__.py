#!/usr/bin/env python3

import datetime 

from flask import Flask, jsonify, render_template, abort, request
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

@app.route("/difficulty/<int:id>/<string:game>", methods = ["GET", "POST"])
@app.route("/difficulty/<string:game>/<int:id>", methods = ["GET", "POST"])
def difficulty(id, game):
    def get_difficulty(id, game):
        game_obj    = Game.query.filter_by(name=game).first()
        if not game_obj:
            abort(404)

        progression = Progression.query.filter_by(user=id, game=game_obj.id).order_by(Progression.date_achieved.desc()).first()
        if not progression:
            abort(404)
            
        difficulty  = Difficulty.query.filter_by(id = progression.difficulty).first()
        if not difficulty:
            abort(404)

        return jsonify(difficulty=difficulty.name)
    
    def post_difficulty(id, game):
        pass

    if request.method == 'GET':
        return get_difficulty(id, game)
    elif request.method == 'POST':
        return post_difficulty(id, game)

if __name__ == "__main__":
    app.run()
