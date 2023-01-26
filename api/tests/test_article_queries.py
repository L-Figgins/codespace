import pytest

from codespace_backend.queries.keys import article_by_create_at_key, articles_key
from codespace_backend.queries.articles import serialize, deserialize, create_article


@pytest.fixture()
def serialized_article(mock_created_at, mock_uuid):
    yield {
        "created_at": mock_created_at,
        "owner_id": mock_uuid,
        "description": "html code",
        "title": "title",
        "code": "<div><div>",
        "lang": "HTML",
    }


@pytest.fixture()
def deserialized_article(mock_created_at, mock_uuid):
    yield {
        "created_at": mock_created_at,
        "owner_id": mock_uuid,
        "description": "html code",
        "title": "title",
        "contact_snippet": {"code": "<div><div>", "lang": "HTML"},
    }


@pytest.fixture()
def mock_article():
    yield {
        "description": "html code",
        "title": "title",
        "codeSnippet": {"code": "<div><div>", "lang": "HTML"},
    }


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
            article_by_create_at_key(), mapping=(mock_uuid, mock_created_at)
        )

        mock_pipe.execute.assert_called()


class TestSerializers:
    def test_serialize(
        self, serialized_article, mock_article, mock_uuid, mock_created_at
    ):
        assert serialized_article == serialize(
            mock_article, created_at=mock_created_at, user_id=mock_uuid
        )
