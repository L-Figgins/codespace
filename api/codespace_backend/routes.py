from flask import current_app as app
from flask import request, jsonify, request
from .queries.articles import get_articles_by_creation_date, create_article

# from flask_json_schema import JsonSchema, JsonValidationError
# from .request_schema import register_schema

# from .db import get_db
from .util import get_utc_timestamp

# schema = JsonSchema()


# @app.errorhandler(JsonValidationError)
# def validation_error(e):
#     return jsonify(
#         {
#             "error": e.message,
#             "errors": [validation_error.message for validation_error in e.errors],
#         }
#     )


@app.route("/articles", methods=["GET"])
def get_articles():
    # db = get_db()
    # stub api
    # now = get_utc_timestamp()
    # ip_sum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt\
    #         ut labore et dolore magna aliqua. Ut enim ad minim veniam,\
    #         quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\
    #         aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. \
    #         Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    # results = [{"title": "Title Stub", "description": ip_sum, "date": now}]

    offsett = request.args.get("offset", 0)
    count = request.args.get("count", 10)
    desc = request.args.get("desc", False)
    results = get_articles_by_creation_date(offset=offsett, count=count, desc=desc)

    return {"payload": results}, 200


@app.route("/articles", methods=["POST"])
def create_articles():
    # hardcore user_id for now
    user_id = "cce8594a-0e36-467d-9dd3-efe9c8376c94"
    data = request.get_json()
    ## TODO: add validations with json schema and other sanitation things
    art_id = create_article(data["payload"], user_id)

    return {"payload": art_id}, 200
