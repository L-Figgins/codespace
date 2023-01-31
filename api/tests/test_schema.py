import pytest
from marshmallow import ValidationError
from codespace_backend.queries.schemas import ArticleSchema, UserSchema


class TestArticleSchema:
    def test_load(self, mocker, mock_article, mock_uuid, serialized_article, mock_created_at):
        mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)
        mocker.patch("codespace_backend.queries.schemas.get_utc_timestamp", return_value=mock_created_at)
        
        schema = ArticleSchema()
        mock_article["owner_id"] = mock_uuid
        art = schema.load(mock_article)

        assert art.get("created_at") == str(mock_created_at)
        assert serialized_article == art


    def test_dump(self, mocker,mock_article, mock_uuid, mock_created_at, deserialized_article):
        mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)
        mocker.patch("codespace_backend.queries.schemas.get_utc_timestamp", return_value=mock_created_at)
        schema = ArticleSchema()
        mock_article["owner_id"] = mock_uuid

        art = schema.load(mock_article)
        assert schema.dump(art) == deserialized_article


    def test_dump_many(self, mocker,client_serialized_art_out, mock_uuid, mock_created_at, mock_article_list):
        mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)
        mocker.patch("codespace_backend.queries.schemas.get_utc_timestamp", return_value=mock_created_at)

        schema = ArticleSchema(many=True)
        arts = schema.dump(mock_article_list, many=True)

        assert arts == client_serialized_art_out

        
class TestUserSchema:
    def test_load(self, mocker, mock_uuid, mock_user, serialized_user):
        mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)
        schema = UserSchema()

        expected = {**serialized_user, "phone": "", "image_url": ""}
        user = schema.load(mock_user)

        assert user == expected

    def test_load_failure(self):
        bad_data = {
            "username": "Logan",
        }

        with pytest.raises(ValidationError):
            schema = UserSchema()
            schema.load(bad_data)
        
    def test_email_validation(self, mock_user):
        #set invailid email
        mock_user["contactInfo"]["email"] = "notanemail"

        with pytest.raises(ValidationError):
            schema = UserSchema()
            schema.load(mock_user)

    def test_dump(self, mocker, mock_user, mock_uuid):
        mocker.patch("codespace_backend.queries.schemas.gen_id", return_value=mock_uuid)
        schema = UserSchema()
        user = schema.load(mock_user)
        print(mock_user)
        expected = {
            "id": mock_uuid,
            "username": "mock_username",
            "name": "mock_name",
            "contactInfo": {
                "email": "mock@email.com",
                "github": "https://github.com/L-Figgins",
                "phone": "",
                "imageURL": ""
            }
        }
        out_schema = UserSchema(exclude={"password"})
        assert out_schema.dump(user) == expected

