import pytest
from os import getenv
from codespace_backend.queries.users import (
    create_user,
    get_user_by_username,
)
from codespace_backend.queries.keys import (
    usernames_unique_key,
    usernames_key,
    users_key,
)



@pytest.mark.integration
def test_create_user_int(mocker, redis, mock_user, mock_uuid, serialized_user):
    mocker.patch("codespace_backend.queries.users.get_db", return_value=redis)
    mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)

    user_id = create_user(mock_user)
    user = redis.hgetall(users_key(mock_uuid))
    assert user == {**serialized_user, "phone":"", "image_url":""}

    exists = redis.sismember(usernames_unique_key(), mock_user["username"])
    assert exists == True

    uid = redis.get(usernames_key(mock_user["username"]))
    assert uid == mock_uuid
    assert user_id == mock_uuid


@pytest.mark.integration
def test_create_user_username_taken_int(mocker, redis, mock_user, mock_uuid):
    mocker.patch("codespace_backend.queries.users.get_db", return_value=redis)
    mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)

    redis.sadd(usernames_unique_key(), mock_user["username"])

    # Assert that calling create_user function raises ValueError
    with pytest.raises(ValueError):
        create_user(mock_user)


def test_create_user_success(mocker, mock_r, mock_user, mock_pipe, mock_uuid, serialized_user):
    mock_r.sismember.return_value = False
    mock_pipe.sismember.return_value = False
    # Patch the get_db function to return the mock redis object
    mocker.patch("codespace_backend.queries.users.get_db", return_value=mock_r)
    # Patch the gen_id function to return a fixed value
    mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)

    mock_r.transaction.return_value = mock_uuid

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
        users_key(mock_uuid), mapping={**serialized_user, "phone":"", "image_url": ""}
    )
    mock_pipe.sadd.assert_called_with(usernames_unique_key(), "mock_username")
    mock_pipe.set.assert_called_with(usernames_key("mock_username"), mock_uuid)
    # Assert that the execute method was called on the pipeline object
    mock_pipe.multi.assert_called()
    # Assert that the returned user_id is the expected value
    assert user_id == mock_uuid


def test_create_user_username_taken(mocker, mock_r, mock_pipe, mock_user, mock_uuid):
    # Patch the get_db function to return the mock redis object
    mocker.patch("codespace_backend.queries.users.get_db", return_value=mock_r)
    # Patch the gen_id function to return a fixed value
    mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)

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
    def test_sucesss_int(self, mocker, redis, mock_user, mock_uuid, serialized_user):
        mocker.patch("codespace_backend.queries.users.get_db", return_value=redis)

        redis.set(usernames_key(mock_user["username"]), mock_uuid)
        redis.hset(users_key(mock_uuid), mapping={**serialized_user, "phone": "", "image_url":""})

        result = get_user_by_username(mock_user["username"])
        # deserialzation adds id and removes password
        mock_user["id"] = mock_uuid
        mock_user.pop("password")

        expected = {**mock_user}
        expected["contactInfo"]["imageURL"] = ""
        expected["contactInfo"]["phone"] = ""

        assert mock_user == result

    def test_success(self, mocker, mock_user, mock_r, mock_uuid, serialized_user):
        # Patch the get_db function to return the mock redis object
        mocker.patch("codespace_backend.queries.users.get_db", return_value=mock_r)
        mock_r.get.return_value = mock_uuid
        mock_r.hgetall.return_value = serialized_user

        result = get_user_by_username(mock_user["username"])

        mock_r.get.assert_called_with(usernames_key(mock_user["username"]))
        mock_r.hgetall.assert_called_with(users_key(mock_uuid))

        mock_user["id"] = mock_uuid
        mock_user.pop("password")
        expected = {**mock_user}
        expected["contactInfo"]["imageURL"] = ""
        expected["contactInfo"]["phone"] = ""
        assert result == expected

    def test_user_not_found(self, mocker, mock_user, mock_r, mock_uuid):
        mocker.patch("codespace_backend.queries.users.get_db", return_value=mock_r)
        mock_r.get.return_value = None

        with pytest.raises(KeyError):
            get_user_by_username(mock_user["username"])


