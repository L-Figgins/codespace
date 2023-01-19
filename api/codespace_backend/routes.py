from flask import current_app as app
from flask import request
from .db import get_db
from .util import get_utc_timestamp



@app.route("/articles", methods=["GET"])
def get_articles():
    # db = get_db()
    #stub api
    now = get_utc_timestamp()
    ip_sum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt\
            ut labore et dolore magna aliqua. Ut enim ad minim veniam,\
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\
            aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. \
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    results = [{"title": "Title Stub", "description": ip_sum, "date": now}]

    return {"payload": results}, 200
