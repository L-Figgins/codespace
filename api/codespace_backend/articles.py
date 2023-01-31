from flask import Blueprint
from flask import request, jsonify, abort, session
from marshmallow import ValidationError
from .queries.articles import get_articles_by_creation_date, create_article

from .auth import login_required
from .util import get_utc_timestamp

articles = Blueprint("articles", __name__)


@articles.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@articles.errorhandler(403)
def forbidden(e):
    return jsonify(error=str(e)), 403

@articles.route("/articles", methods=["GET"])
def articles_route():
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



@articles.route('/articles', methods=["POST"])
@login_required
def create_articles():
    """
    Create an Article
    """
    # hardcore user_id for now
    user_id = session["user_id"]
    data = request.get_json()
    ## TODO: add validations with json schema and other sanitation things
    try:
        art_id = create_article(data["payload"], user_id)
    except ValidationError as e:
        abort(e, 400)

    return {"payload": art_id}, 200
