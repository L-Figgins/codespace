from os import getenv
import redis

from flask import g


def get_db():
    if "db" not in g:
        g.db = redis.Redis(
            host=getenv("REDIS_HOST", ""),
            port=getenv("REDIS_PORT", "6379"),
            password=getenv("REDIS_PW", "devpassword")
        )

    return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_con():
    db = get_db

def init_app(app):
    app.teardown_appcontext(close_db)