import pytest
from flask import g, session
from codespace_backend import create_app
from codespace_backend.queries.keys import (
    articles_key,
    article_by_create_at_key,
    usernames_unique_key,
    users_key,
    usernames_key
)


@pytest.mark.integration
@pytest.fixture()
def app(redis, mock_article_list, mock_uuid_list, mock_uuid, serialized_user):
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    for i, article in enumerate(mock_article_list):
        redis.hset(articles_key(mock_uuid_list[i]), mapping=article)
        redis.zadd(
            article_by_create_at_key(),
            mapping={mock_uuid_list[i]: int(article["created_at"])},
        )

    

    yield app


@pytest.mark.integration
@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.mark.integration
def test_get_articles(client, client_serialized_art_out):
    with client:
        response = client.get("/articles")
        assert response.json["payload"] == client_serialized_art_out


@pytest.mark.integration
class TestAuthEndpoints:
    def test_register(self,mocker,redis, client, mock_user, mock_uuid):
        mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)
        with client:
            response = client.post("/auth/register", json={"payload":mock_user})
            print(response)
            uid = response.get_json()["payload"]
            
            assert uid == mock_uuid
            # assert session["user_id"] == mock_uuid
            from_db = redis.hgetall(users_key(mock_uuid))
            assert from_db["id"] == uid == mock_uuid

    def test_login(self, mocker, auth, client, mock_uuid):
        mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)
        # redis.sadd(usernames_unique_key(),"mock_username")
        # redis.hset(users_key(mock_uuid),mapping={**serialized_user, "phone": "", "image_url": ""})
        # redis.set(usernames_key("mock_username"), mock_uuid)
        with client:
            _ = auth.register()
            response = auth.login()
            assert response.status_code == 200
            assert response.get_json()["payload"] == "success"
            assert session["user_id"] == mock_uuid
            
