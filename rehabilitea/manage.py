#!/usr/bin/env python3

from flask.cli import FlaskGroup

from user_management import app, db, User

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def create_db():
    db.session.add(User())
    db.session.commit()

if __name__ == "__main__":
    cli()