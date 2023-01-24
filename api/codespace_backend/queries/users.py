from ..db import get_db
from ..util import generate_user_id
from .keys import usernames_unique_key, usernames_key, users_key

def create_user(user:dict):
    # r = redis
    r = get_db()

    user_id = generate_user_id()

    exists = r.sismember(usernames_unique_key(),user["username"])

    if exists:
        raise ValueError("Username is taken")


    pipe = r.pipeline()
    pipe.hset(users_key(id),serialize(user))
    pipe.sadd(usernames_unique_key(), user["username"])
    pipe.zadd(usernames_key(),{[user["username"]]: id} )

    _ = pipe.execute()

    return user_id


def serialize(user:dict):
    hash = {
        "username": user["username"],
        "name": user["name"],
        "password": user["password"],
        "email": user["contactInfo"]["email"]
    }

    return hash
