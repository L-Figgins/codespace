import functools
from flask import Blueprint, g, redirect, request, session, url_for, jsonify, abort
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

from .queries.users import create_user, get_user_by_username,get_user_by_id


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@bp.errorhandler(403)
def forbidden(e):
    return jsonify(error=str(e)), 403

@bp.errorhandler(401)
def unauthenticated(e):
    return jsonify(error=str(e)), 401


#this is straight from the docs, but feels like bad practice
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id == None:
        g.user = None
    else:
        g.user = get_user_by_id(user_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            abort(401, description="User Must log in")
        return view(**kwargs)

    return wrapped_view


@bp.route("/register", methods=["POST"])
# @schema.validate(register_schema)
def register_admin_user():
    # r = redis
    try:
        payload = request.get_json()["payload"]
        username = payload["username"]
        password = payload["password"]
    except KeyError:
        abort(
            400,
            description="Malformed request body. The payload must contain a username and password",
        )

    hash = generate_password_hash(password)
    payload["password"] = hash

    try:
        user_id = create_user(payload)
        # bp.logger.info(f"user_payload created with id:{user_id}")
    except ValidationError:
        abort(400, description="Validation Error")
        

    return {"payload": user_id}, 200

@bp.route("/login", methods=["POST"])
def login():
    try:
        user_payload = request.get_json()["payload"]
        username = user_payload["username"]
        password = user_payload["password"]

    except KeyError:
        abort(
            400,
            description="Malformed request body. The payload must contain a username and password",
        )

    user = get_user_by_username(username, only={"id","password"}, exclude=())
    is_valid = check_password_hash(user["password"], password)

    if not is_valid:
        abort(403, description="incorrect username or password")

    session.clear()
    session["user_id"] = user["id"]

    return {"payload": "success"}, 200
