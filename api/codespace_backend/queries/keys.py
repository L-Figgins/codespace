# redis keys


def usernames_unique_key() -> str:
    """
    redis Set key for determining uniqueness of username
    """
    return "usernames:unique"


def users_key(user_id: str) -> str:
    """
    redis hash key containing all user information
    :param user_id: user id
    """
    return f"users#{user_id}"


def usernames_key(name) -> str:
    """
    redis usersnames sorted set key. The score is the user id.
    """
    return f"usernames#{name}"
