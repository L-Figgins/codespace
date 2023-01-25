from ..db import get_db
from ..util import generate_user_id
from .keys import usernames_unique_key, usernames_key, users_key


def create_user(user: dict):
    """
    Creates a new user with the given information and stores it in redis as a
    series of data structures to fascilitate queries.

    :param user: A dictionary containing the user's information, including
                 'username', 'name', 'password', and 'contactInfo'
    :return: A string representing the user's unique ID generated with uiid4

    :raises ValueError: if the provided username is already taken
    """

    def create_user_txn(pipe):
        exists = pipe.sismember(usernames_unique_key(), user["username"])
        if exists:
            raise ValueError("Username is taken")

        pipe.multi()
        user_id = generate_user_id()
        # user id is defined in the other function since redis.py transactions do not allow for
        pipe.hset(users_key(user_id), serialize(user))
        pipe.sadd(usernames_unique_key(), user["username"])
        pipe.zadd(usernames_key(), {user["username"]: user_id})
        return user_id

    # r = redis
    r = get_db()
    user_id = r.transaction(
        create_user_txn, usernames_unique_key(), value_from_callable=True
    )

    return user_id


def serialize(user: dict) -> dict:
    """
    Serializes the user information into a dictionary of specific fields.

    :param user: A dictionary containing the user's information
    :return: A dictionary containing the 'username', 'name', 'password', and 'email' fields

    """
    hash = {
        "username": user["username"],
        "name": user["name"],
        "password": user["password"],
        "email": user["contactInfo"]["email"],
    }

    return hash
