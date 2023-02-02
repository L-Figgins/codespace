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
def app(redis,mock_article_list, mock_uuid_list):
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

    
    print("url map", app.url_map)
    yield app


@pytest.mark.integration
@pytest.fixture(scope="function")
def client(app):
    client = app.test_client()
    yield client

@pytest.mark.integration
class TestArticlesEndpoint:
    def test_get_articles(self,client, client_serialized_art_out):
        with client:
            response = client.get("/articles")
            assert response.status_code == 200
            assert response.json["payload"] == client_serialized_art_out

    def test_create_article(self, client, auth, redis, mock_article):
        with client:
            register_response = auth.register()
            assert register_response.status_code == 200
            #login to create session
            #TODO refactor to use session transaction for testing
            _ = auth.login()
            assert _.status_code == 200
            response = client.post("/articles", json={"payload":mock_article})
            print(response)
            assert response.status_code == 200
            article_id =  response.get_json()["payload"]

            article = redis.hgetall(articles_key(article_id))
            uid = register_response.get_json()["payload"]
            assert article["owner_id"] == uid

    def test_create_401(self, client, mock_article):
        # there is no g.user or session[user_id]
        response = client.post("/articles", json={"payload":mock_article})
        assert response.status_code == 401

    def test_create_400(self, client, auth):
        with client:
            _ = auth.register()
            _ = auth.login()
            response = client.post('/articles', json={"payload":{"username": "foo"}})
            assert response.status_code == 400




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

    def test_incorrect_password(self, client, auth):
        with client:
            _ = auth.register()
            login_res = auth.login(password="wrong password")
            assert login_res.status_code == 401

    def test_bad_request(self, client, auth):
        with client:
            _ = auth.register()
            login_res = client.post("/auth/login", json={"payload":{"username":"usrname"}})
            assert login_res.status_code == 400
        
    def test_logout(self, client, auth):
        with client:
            register_res = auth.register()
            _ = auth.login()
            assert _.status_code == 200

            uid = register_res.get_json()["payload"]
            assert session["user_id"] == uid

            _ = client.get("/auth/logout")
            assert session.get("user_id", None) == None


