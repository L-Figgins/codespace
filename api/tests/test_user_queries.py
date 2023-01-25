import pytest
import redis
from os import getenv
from codespace_backend.queries.users import (
    create_user,
    get_user_by_username,
    serialize,
    deserialize,
)
from codespace_backend.queries.keys import (
    usernames_unique_key,
    usernames_key,
    users_key,
)


@pytest.fixture(name="mock_user")
def mock_user():
    user = {
        "username": "mock_username",
        "name": "mock_name",
        "password": "mock_password",
        "contactInfo": {"email": "mock@email.com"},
    }
    yield user


# @pytest.mark.integration
# @pytest.fixture(name="redis")
# def real_redis():
#     r = redis.Redis(
#         host=getenv("REDIS_HOST", ""),
#         port=getenv("REDIS_PORT", "6379"),
#         password=getenv("REDIS_PW", "devpassword"),
#         decode_responses=True,
#     )

#     yield r
#     r.flushall()


# @pytest.fixture(name="mock_pipe")
# def mock_pipe(mocker):
#     mock_pipe = mocker.MagicMock()
#     yield mock_pipe


# @pytest.fixture(name="mock_r")
# def mock_redis(mocker, mock_pipe):
#     mock_r = mocker.MagicMock()
#     mock_r.pipeline.return_value = mock_pipe
#     yield mock_r


# @pytest.fixture(name="mock_user_id")
# def mock_user_id():
#     uid = "cce8594a-0e36-467d-9dd3-efe9c8376c94"
#     yield uid


@pytest.fixture()
def serialized_user(mock_user_id):
    expected_output = {
        "id": mock_user_id,
        "username": "mock_username",
        "name": "mock_name",
        "password": "mock_password",
        "email": "mock@email.com",
    }

    yield expected_output


@pytest.mark.integration
def test_create_user_int(mocker, redis, mock_user, mock_user_id, serialized_user):
    mocker.patch("codespace_backend.queries.users.get_db", return_value=redis)
    mocker.patch(
        "codespace_backend.queries.users.generate_user_id", return_value=mock_user_id
    )

    user_id = create_user(mock_user)
    user = redis.hgetall(users_key(mock_user_id))
    assert user == serialized_user

    exists = redis.sismember(usernames_unique_key(), mock_user["username"])
    assert exists == True

    uid = redis.get(usernames_key(mock_user["username"]))
    assert uid == mock_user_id
    assert user_id == mock_user_id


@pytest.mark.integration
def test_create_user_username_taken_int(mocker, redis, mock_user, mock_user_id):
    mocker.patch("codespace_backend.queries.users.get_db", return_value=redis)
    mocker.patch(
        "codespace_backend.queries.users.generate_user_id", return_value=mock_user_id
    )

    redis.sadd(usernames_unique_key(), mock_user["username"])

    # Assert that calling create_user function raises ValueError
    with pytest.raises(ValueError):
        create_user(mock_user)


def test_create_user_success(mocker, mock_r, mock_user, mock_pipe, mock_user_id):
    mock_r.sismember.return_value = False
    mock_pipe.sismember.return_value = False
    # Patch the get_db function to return the mock redis object
    mocker.patch("codespace_backend.queries.users.get_db", return_value=mock_r)
    # Patch the generate_user_id function to return a fixed value
    mocker.patch(
        "codespace_backend.queries.users.generate_user_id", return_value=mock_user_id
    )

    mock_r.transaction.return_value = mock_user_id

    def side_effect(func, *args, **kwargs):
        # call arg provided from fist call
        return func(mock_pipe)

    mock_r.transaction.side_effect = side_effect

    # Call the create_user function
    user_id = create_user(mock_user)

    # assert is Member is called with correct args
    mock_r.transaction.assert_called_with(
        mocker.ANY, usernames_unique_key(), value_from_callable=True
    )

    # Assert that the hset, sadd, and zadd methods were called on the pipeline object
    mock_pipe.hset.assert_called_with(
        users_key(mock_user_id), mapping=serialize(mock_user, mock_user_id)
    )
    mock_pipe.sadd.assert_called_with(usernames_unique_key(), "mock_username")
    mock_pipe.set.assert_called_with(usernames_key("mock_username"), mock_user_id)
    # Assert that the execute method was called on the pipeline object
    mock_pipe.multi.assert_called()
    # Assert that the returned user_id is the expected value
    assert user_id == mock_user_id


def test_create_user_username_taken(mocker, mock_r, mock_pipe, mock_user, mock_user_id):
    # Patch the get_db function to return the mock redis object
    mocker.patch("codespace_backend.queries.users.get_db", return_value=mock_r)
    # Patch the generate_user_id function to return a fixed value
    mocker.patch(
        "codespace_backend.queries.users.generate_user_id", return_value=mock_user_id
    )

    def side_effect(func, *args, **kwargs):
        # call arg provided from fist call
        return func(mock_pipe)

    mock_r.transaction.side_effect = side_effect
    # Set the sismember return value to True, indicating that the username is taken
    mock_pipe.sismember.return_value = True

    # Assert that calling create_user function raises ValueError
    with pytest.raises(ValueError):
        create_user(mock_user)
    # Assert that the hset, sadd, and zadd methods were not called
    mock_pipe.hset.assert_not_called()
    mock_pipe.sadd.assert_not_called()
    mock_pipe.set.assert_not_called()


class TestGetUserByUsername:
    @pytest.mark.integration
    def test_sucesss_int(self, mocker, redis, mock_user, mock_user_id):
        mocker.patch("codespace_backend.queries.users.get_db", return_value=redis)

        redis.set(usernames_key(mock_user["username"]), mock_user_id)
        redis.hset(users_key(mock_user_id), mapping=serialize(mock_user, mock_user_id))

        result = get_user_by_username(mock_user["username"])
        # deserialzation adds id and removes password
        mock_user["id"] = mock_user_id
        mock_user.pop("password")

        assert mock_user == result

    def test_success(self, mocker, mock_user, mock_r, mock_user_id):
        # Patch the get_db function to return the mock redis object
        mocker.patch("codespace_backend.queries.users.get_db", return_value=mock_r)
        mock_r.get.return_value = mock_user_id
        mock_r.hgetall.return_value = serialize(mock_user, mock_user_id)

        result = get_user_by_username(mock_user["username"])

        mock_r.get.assert_called_with(usernames_key(mock_user["username"]))
        mock_r.hgetall.assert_called_with(users_key(mock_user_id))

        mock_user["id"] = mock_user_id
        mock_user.pop("password")
        assert result == mock_user

    def test_user_not_found(self, mocker, mock_user, mock_r, mock_user_id):
        mocker.patch("codespace_backend.queries.users.get_db", return_value=mock_r)
        mock_r.get.return_value = None

        with pytest.raises(KeyError):
            get_user_by_username(mock_user["username"])


class TestUserSerializers:
    def test_serialize(self, mock_user, serialized_user, mock_user_id):
        assert serialize(mock_user, mock_user_id) == serialized_user

    def test_deserialize(self, mock_user, serialized_user, mock_user_id):
        mock_user["id"] = mock_user_id
        mock_user.pop("password")
        assert mock_user == deserialize(serialized_user)
