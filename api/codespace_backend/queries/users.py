from ..db import get_db
from .keys import usernames_unique_key, usernames_key, users_key

from .schemas import UserSchema


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
        username = user.get("username")
        exists = pipe.sismember(usernames_unique_key(), user.get("username"))
        if exists:
            raise ValueError("Username is taken")

        pipe.multi()
        user_id = user.get("id")
     
        # user id is defined in the other function since redis.py transactions do not allow for
        pipe.hset(users_key(user_id), mapping=user)
        pipe.sadd(usernames_unique_key(), username)
        # set doesnt need an encoded uuid, but hset does
        pipe.set(usernames_key(username), user_id)
        return user_id

    # r = redis
    r = get_db()
    schema = UserSchema()
    user = schema.load(user)
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
    
    schema = UserSchema()
    return schema.dump(r.hgetall(users_key(uid)))

def get_user_by_id(id:str)-> dict:
    r = get_db()
    schema = UserSchema()
    user = r.hgetall(users_key(id))
    if not user:
        return None

    return schema.dump(user)
   