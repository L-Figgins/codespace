from flask import Blueprint, g, redirect, request, session, url_for, jsonify, abort
# from .db import get_db
from .queries.users import get_user_by_id
from .auth import login_required


user = Blueprint("user", __name__)

@user.route('/user', methods=["GET"] )
@login_required
def get_user():
    id = session["user_id"]
    print(id)
    user = get_user_by_id(id)
    print(user)
    if not user:
        abort(404,"user not found")
    return {"payload": user} , 200



