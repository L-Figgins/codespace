from ..db import get_db
from ..util import gen_id
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

    def create_user_txn(pipe) -> str:
        exists = pipe.sismember(usernames_unique_key(), user["username"])
        if exists:
            raise ValueError("Username is taken")

        pipe.multi()
        user_id = gen_id()
        username = user["username"]
        # user id is defined in the other function since redis.py transactions do not allow for
        pipe.hset(users_key(user_id), mapping=serialize(user, user_id))
        pipe.sadd(usernames_unique_key(), user["username"])
        pipe.set(usernames_key(username), user_id)
        return user_id

    # r = redis
    r = get_db()
    user_id = r.transaction(
        create_user_txn, usernames_unique_key(), value_from_callable=True
    )

    return user_id


def get_user_by_username(username: str) -> dict:
    """
    Retrieve a user's information from the database by their username.

    :param username: The username of the user to retrieve.
    :return: A dictionary containing the user's information.
    :raises KeyError: If the user does not exist in the database.
    """
    r = get_db()
    uid = r.get(usernames_key(username))

    if uid == None:
        raise KeyError("User does not exist")

    return deserialize(r.hgetall(users_key(uid)))


def serialize(user: dict, user_id: str) -> dict:
    """
    Serializes the user information into a dictionary of specific fields.

    :param user: A dictionary containing the user's information
    :return: A dictionary containing the 'username', 'name', 'password', and 'email' fields

    """
    hash = {
        "id": user_id,
        "username": user["username"],
        "name": user["name"],
        "password": user["password"],
        "email": user["contactInfo"]["email"],
    }

    return hash


def deserialize(data: dict) -> dict:
    # more to be added later
    CONTACT_INFO_KEYS = {"email"}
    EXCLUDE_KEYS = {"password"}
    result = {"contactInfo": {}}

    for k, v in data.items():
        if k in CONTACT_INFO_KEYS:
            result["contactInfo"][k] = v
            continue
        if k not in EXCLUDE_KEYS:
            result[k] = v

    return result
