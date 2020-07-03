#!/usr/bin/env python3

from flask import Flask, jsonify, render_template
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
    name            = db.Column(db.String(50), nullable=False)

class Progression(db.Model):
    __tablename__   = "progressions"

    id              = db.Column(db.Integer, primary_key=True)
    user            = db.Column(db.Integer, db.ForeignKey('users.id'))
    game            = db.Column(db.Integer, db.ForeignKey('games.id'))
    difficulty      = db.Column(db.Integer, db.ForeignKey('difficulties.id'))

class Event(db.Model):
    __tablename__   = "events"

    id              = db.Column(db.Integer, primary_key=True)
    user            = db.Column(db.Integer, db.ForeignKey('users.id'))
    game            = db.Column(db.Integer, db.ForeignKey('games.id'))
    event_type      = db.Column(db.String(50), nullable=False)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
