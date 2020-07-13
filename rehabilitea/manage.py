#!/usr/bin/env python3

from flask.cli import FlaskGroup

from user_management import app, db, User, Difficulty, Game, Progression

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def create_db():
    db.session.add(User(id = 0, birth_day = "1996/08/01"))

    db.session.add(Difficulty(id = 0, name = "Easy"))
    db.session.add(Difficulty(id = 1, name = "Medium"))
    db.session.add(Difficulty(id = 2, name = "Hard"))

    db.session.add(Game(id = 0, name = "Memory"))
    db.session.add(Game(id = 1, name = "Bubbles"))
    db.session.add(Game(id = 2, name = "HideAndSeek"))

    db.session.commit()

    db.session.add(Progression(user = 0, game = 0, difficulty = 0))
    db.session.add(Progression(user = 0, game = 1, difficulty = 0))
    db.session.add(Progression(user = 0, game = 2, difficulty = 0))

    db.session.commit()

if __name__ == "__main__":
    cli()