import pytest
from codespace_backend import create_app
from codespace_backend.queries.keys import (
    articles_key,
    article_by_create_at_key,
)

from codespace_backend.queries.articles import deserialize as deserialize_articles


@pytest.mark.integration
@pytest.fixture()
def deserialized_article_list(mock_article_list):
    return list(map(deserialize_articles, mock_article_list.copy()))


@pytest.mark.integration
@pytest.fixture()
def app(redis, mock_article_list, mock_uuid_list):
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
def test_get_articles(client, deserialized_article_list):
    with client:
        response = client.get("/articles")
        assert response.json["payload"] == deserialized_article_list
