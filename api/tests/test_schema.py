import pytest
import json
from codespace_backend.queries.schemas import ArticleSchema

def test_article_load(mocker, mock_article, mock_uuid, serialized_article, mock_created_at):
    mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)
    mocker.patch("codespace_backend.queries.schemas.get_utc_timestamp", return_value=mock_created_at)
    
    schema = ArticleSchema()
    mock_article["owner_id"] = mock_uuid
    art = schema.load(mock_article)

    assert serialized_article == art


def test_article_dump(mocker,mock_article, mock_uuid, mock_created_at, deserialized_article):
    mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)
    mocker.patch("codespace_backend.queries.schemas.get_utc_timestamp", return_value=mock_created_at)
    schema = ArticleSchema()
    mock_article["owner_id"] = mock_uuid

    art = schema.load(mock_article)
    assert schema.dump(art) == deserialized_article


def test_articles_dump(mocker,client_serialized_art_out, mock_uuid, mock_created_at, mock_article_list):
    mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)
    mocker.patch("codespace_backend.queries.schemas.get_utc_timestamp", return_value=mock_created_at)

    schema = ArticleSchema(many=True)
    arts = schema.dump(mock_article_list, many=True)

    assert arts == client_serialized_art_out

    

