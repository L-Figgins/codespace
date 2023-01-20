from flask import current_app as app
from flask import request, jsonify

from flask_json_schema import JsonSchema,  JsonValidationError
from .request_schema import register_schema
# from .db import get_db
from .util import get_utc_timestamp

schema = JsonSchema()

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]})
    

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


@app.route("/auth/register", methods=["POST"])
# @schema.validate(register_schema)
def register_admin_user():
    request_data = request.get_json()
    return {"payload": request_data}, 200