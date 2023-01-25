import pytest
from codespace_backend.queries.users import create_user, serialize
from codespace_backend.db import get_db
from codespace_backend.util import generate_user_id
from codespace_backend.queries.keys import (
    usernames_unique_key,
    usernames_key,
    users_key,
)


@pytest.fixture(name="mock_pipe")
def mock_pipe(mocker):
    mock_pipe = mocker.MagicMock()
    yield mock_pipe


@pytest.fixture(name="mock_r")
def mock_redis(mocker, mock_pipe):
    mock_r = mocker.MagicMock()
    mock_r.pipeline.return_value = mock_pipe
    yield mock_r


@pytest.fixture(name="mock_user_id")
def mock_user_id():
    uid = "cce8594a-0e36-467d-9dd3-efe9c8376c94"
    yield uid


@pytest.mark.dev
def test_create_user_success(mocker, mock_r, mock_pipe, mock_user_id):
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
        print(func)
        val = func(mock_pipe)
        print(val)
        return func(mock_pipe)

    mock_r.transaction.side_effect = side_effect

    user = {
        "username": "mock_username",
        "name": "mock_name",
        "password": "mock_password",
        "contactInfo": {"email": "mock@email.com"},
    }
    # Call the create_user function
    user_id = create_user(user)

    # assert is Member is called with correct args
    mock_r.transaction.assert_called_with(
        mocker.ANY, usernames_unique_key(), value_from_callable=True
    )

    # Assert that the hset, sadd, and zadd methods were called on the pipeline object
    mock_pipe.hset.assert_called_with(users_key(mock_user_id), serialize(user))
    mock_pipe.sadd.assert_called_with(usernames_unique_key(), "mock_username")
    mock_pipe.zadd.assert_called_with(usernames_key(), {"mock_username": mock_user_id})
    # Assert that the execute method was called on the pipeline object
    mock_pipe.multi.assert_called()
    # Assert that the returned user_id is the expected value
    assert user_id == mock_user_id


def test_create_user_username_taken(mocker, mock_r, mock_pipe, mock_user_id):
    # Patch the get_db function to return the mock redis object
    mocker.patch("codespace_backend.queries.users.get_db", return_value=mock_r)
    # Patch the generate_user_id function to return a fixed value
    mocker.patch(
        "codespace_backend.queries.users.generate_user_id", return_value=mock_user_id
    )
    # Set the sismember return value to True, indicating that the username is taken
    mock_r.sismember.return_value = True

    user = {
        "username": "mock_username",
        "name": "mock_name",
        "password": "mock_password",
        "contactInfo": {"email": "mock@email.com"},
    }

    # Assert that calling create_user function raises ValueError
    with pytest.raises(ValueError):
        create_user(user)
    # Assert that the hset, sadd, and zadd methods were not called
    mock_pipe.hset.assert_not_called()
    mock_pipe.sadd.assert_not_called()
    mock_pipe.zadd.assert_not_called()


def test_serialize():
    user = {
        "username": "mock_username",
        "name": "mock_name",
        "password": "mock_password",
        "contactInfo": {"email": "mock@email.com"},
    }
    expected_output = {
        "username": "mock_username",
        "name": "mock_name",
        "password": "mock_password",
        "email": "mock@email.com",
    }
    assert serialize(user) == expected_output
