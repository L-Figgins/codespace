# redis keys

# user keys
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
    redis usersnames key, the value is the uuid4 user id
    """
    return f"usernames#{name}"


# article keys


def articles_key(article_id):
    """
    redis hash containing article data
    """

    return f"articles#{article_id}"


def article_by_create_at_key():
    """
    Redis Sorted Set Key for retrieviing items in order of creation
    """

    return f"articles:created_at"
