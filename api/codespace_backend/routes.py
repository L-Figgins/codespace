from flask import current_app as app
from flask import request, jsonify, abort
from marshmallow import ValidationError
from .queries.articles import get_articles_by_creation_date, create_article

# from flask_json_schema import JsonSchema, JsonValidationError
# from .request_schema import register_schema

# from .db import get_db
from .util import get_utc_timestamp

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(403)
def bad_request(e):
    return jsonify(error=str(e)), 403



@app.route("/articles", methods=["GET"])
def get_articles():
    """
    Get a list of articles.

    :queryparam count: Maximum number of articles to return (default is 10).
    :queryparam desc: Sort articles descending if true (by creation_date).
    :queryparam offset: article offest for paring.
    :return: List of articles.
    """
    offsett = request.args.get("offset", 0)
    count = request.args.get("count", 10)
    desc = request.args.get("desc", False)
    results = get_articles_by_creation_date(offset=offsett, count=count, desc=desc)

    return {"payload": results}, 200


@app.route("/articles", methods=["POST"])
def create_articles():
    """
    Create an Article
    """
    # hardcore user_id for now
    user_id = "cce8594a-0e36-467d-9dd3-efe9c8376c94"
    data = request.get_json()
    ## TODO: add validations with json schema and other sanitation things
    try:
        art_id = create_article(data["payload"], user_id)
    except ValidationError as e:
        abort(e, 400)

    return {"payload": art_id}, 200
