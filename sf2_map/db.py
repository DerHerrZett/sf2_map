import sqlite3
from datetime import datetime

import click
import flask
from flask import current_app, g

sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


def init_db():
    """
    Initialize an empty sqlite3 database file. Drops all previous data. Only use when really necessary.
    """
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def get_db():
    """
    Looks for the sqlite3 database instance.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    If connections to the database were created, they are closed here.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app: flask.Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")
