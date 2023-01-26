import pytest

from codespace_backend.queries.keys import article_by_create_at_key, articles_key
from codespace_backend.queries.articles import (
    serialize,
    deserialize,
    create_article,
    get_articles_by_creation_date,
)


@pytest.fixture()
def serialized_article(mock_created_at, mock_uuid):
    yield {
        "id": mock_uuid,
        "title": "title",
        "description": "html code",
        "owner_id": mock_uuid,
        "created_at": str(mock_created_at),
        "code": "<div><div>",
        "lang": "HTML",
    }


@pytest.fixture()
def deserialized_article(mock_created_at, mock_uuid):
    yield {
        "id": mock_uuid,
        "title": "title",
        "description": "html code",
        "owner_id": mock_uuid,
        "created_at": mock_created_at,
        "code_snippet": {"code": "<div><div>", "lang": "HTML"},
    }


@pytest.fixture()
def mock_article():
    yield {
        "description": "html code",
        "title": "title",
        "codeSnippet": {"code": "<div><div>", "lang": "HTML"},
    }


@pytest.fixture()
def mock_uuid_list():
    yield [
        "678fd3c1-5e75-419c-ac25-c0af12f9cf12",
        "a05f45b3-a606-4636-b001-3875f49c5d85",
        "e6c9baff-1d83-467c-b982-b02f059e882a",
        "b114aae1-5c5e-4ad7-910f-4f302535dfcb",
        "1e03273d-32f3-49e1-aa4e-15e03a24049e",
    ]


@pytest.fixture()
def mock_article_list(serialized_article, mock_uuid_list):
    articles = []
    KEY_ORDER = [
        "id",
        "title",
        "description",
        "owner_id",
        "created_at",
        "code",
        "lang",
    ]

    for i in range(5):
        # do not mutate fixture
        copy = serialized_article.copy()
        copy["created_at"] = str(int(copy["created_at"]) + i * 100)
        copy["id"] = mock_uuid_list[i]
        # due to the way dictionaries, tuple unpacking,
        # and the declared order of the sort command,
        # ONLY when mocking i must reorder the keys

        ordered = {k: copy[k] for k in KEY_ORDER}
        articles.append(ordered)

    print("articles", articles)

    # due to the way dictionaries, tuple unpacking, and the declared order of the sort command, ONLY when mocking i must reorder the keys

    yield articles


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
