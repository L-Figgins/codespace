import pytest
from codespace_backend import create_app

@pytest.fixture()
def app():
    app = create_app()
    # this may cause problems i might want to pass test config directly
    # once I actually do a deep dive on flask configs 
    app.config.update({
        "TESTING":True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_get_articles(client):
    with client:
        response = client.get("/articles")
        assert response.json["payload"][0]["title"] == "Title Stub"
