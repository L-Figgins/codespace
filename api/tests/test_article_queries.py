import pytest

from codespace_backend.queries.keys import article_by_create_at_key, articles_key
from codespace_backend.queries.articles import (
    serialize,
    deserialize,
    create_article,
    get_articles_by_creation_date,
)


@pytest.mark.integration
@pytest.fixture(name="redis_with_data")
def redis_with_article_data(redis, mock_article_list, mock_uuid_list):
    for i, article in enumerate(mock_article_list):
        redis.hset(articles_key(mock_uuid_list[i]), mapping=article)
        redis.zadd(
            article_by_create_at_key(),
            mapping={mock_uuid_list[i]: int(article["created_at"])},
        )

    yield redis


class TestGetArticles:
    @pytest.mark.integration
    def test_success_int(
        self, mocker, redis_with_data, mock_article_list, mock_uuid_list
    ):
        mocker.patch(
            "codespace_backend.queries.articles.get_db", return_value=redis_with_data
        )

        articles = get_articles_by_creation_date()
        deserialized = list(map(deserialize, mock_article_list))
        assert articles == deserialized

        articles = get_articles_by_creation_date(offset=1, count=2)
        assert articles == deserialized[1:3]

    def test_success(
        self,
        mocker,
        mock_r,
        mock_article_list,
    ):
        mocker.patch("codespace_backend.queries.articles.get_db", return_value=mock_r)
        mock_r.sort.return_value = [d.values() for d in mock_article_list]
        print("mock_art_list", mock_article_list)
        get = [
            "#",
            f"{articles_key('*')}->title",
            f"{articles_key('*')}->description",
            f"{articles_key('*')}->owner_id",
            f"{articles_key('*')}->created_at",
            f"{articles_key('*')}->code",
            f"{articles_key('*')}->lang",
        ]

        deserialized = list(map(deserialize, mock_article_list))

        articles = get_articles_by_creation_date()
        assert articles == deserialized

        mock_r.sort.assert_called_with(
            article_by_create_at_key(),
            start=0,
            num=10,
            by="nosort",
            get=get,
            groups=True,
        )


class TestCreateArticle:
    def test_success(
        self,
        mocker,
        mock_r,
        mock_uuid,
        mock_created_at,
        mock_pipe,
        mock_article,
        serialized_article,
    ):
        mocker.patch("codespace_backend.queries.articles.get_db", return_value=mock_r)
        mocker.patch(
            "codespace_backend.queries.articles.get_utc_timestamp",
            return_value=mock_created_at,
        )
        mocker.patch(
            "codespace_backend.queries.articles.gen_id", return_value=mock_uuid
        )

        result = create_article(mock_article, mock_uuid)
        assert result == mock_uuid

        mock_r.pipeline.return_value = mock_pipe
        mock_r.pipeline.assert_called()

        mock_pipe.hset.assert_called_with(
            articles_key(mock_uuid), mapping=serialized_article
        )

        mock_pipe.zadd.assert_called_with(
            article_by_create_at_key(), mapping={mock_uuid: mock_created_at}
        )

        mock_pipe.execute.assert_called()

    @pytest.mark.integration
    def test_success_int(
        self,
        mocker,
        redis,
        mock_article,
        mock_uuid,
        serialized_article,
        mock_created_at,
    ):
        mocker.patch("codespace_backend.queries.articles.get_db", return_value=redis)
        mocker.patch(
            "codespace_backend.queries.articles.gen_id", return_value=mock_uuid
        )
        mocker.patch(
            "codespace_backend.queries.articles.get_utc_timestamp",
            return_value=mock_created_at,
        )

        article_id = create_article(article=mock_article, user_id=mock_uuid)
        assert article_id == mock_uuid

        hash = redis.hgetall(articles_key(mock_uuid))
        assert hash == serialized_article


class TestSerializers:
    def test_serialize(
        self, serialized_article, mock_article, mock_uuid, mock_created_at
    ):
        assert serialized_article == serialize(
            mock_article,
            created_at=mock_created_at,
            user_id=mock_uuid,
            art_id=mock_uuid,
        )

    def test_deserialize(self, deserialized_article, serialized_article):
        assert deserialized_article == deserialize(serialized_article)
