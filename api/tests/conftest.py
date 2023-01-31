import pytest
import redis
from os import getenv


@pytest.mark.integration
@pytest.fixture(name="redis")
def real_redis():
    r = redis.Redis(
        host=getenv("REDIS_HOST", ""),
        port=getenv("REDIS_PORT", "6379"),
        password=getenv("REDIS_PW", "devpassword"),
        decode_responses=True,
    )

    yield r
    r.flushall()


@pytest.fixture(name="mock_pipe")
def mock_pipe(mocker):
    mock_pipe = mocker.MagicMock()
    yield mock_pipe


@pytest.fixture(name="mock_r")
def mock_redis(mocker, mock_pipe):
    mock_r = mocker.MagicMock()
    mock_r.pipeline.return_value = mock_pipe
    yield mock_r


@pytest.fixture(name="mock_uuid")
def mock_uuid():
    uid = "cce8594a-0e36-467d-9dd3-efe9c8376c94"
    yield uid


@pytest.fixture(name="mock_created_at")
def mock_created_at_ts():
    return 1674702339


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
        "ownerId": mock_uuid,
        "createdAt": mock_created_at,
        "codeSnippet": {"code": "<div><div>", "lang": "HTML"},
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
def client_serialized_art_out():
    yield  [
  {
    "id": "678fd3c1-5e75-419c-ac25-c0af12f9cf12",
    "title": "title",
    "description": "html code",
    "ownerId": "cce8594a-0e36-467d-9dd3-efe9c8376c94",
    "createdAt": 1674702339,
    "codeSnippet": { "code": "<div><div>", "lang": "HTML" }
  },
  {
    "id": "a05f45b3-a606-4636-b001-3875f49c5d85",
    "title": "title",
    "description": "html code",
    "ownerId": "cce8594a-0e36-467d-9dd3-efe9c8376c94",
    "createdAt": 1674702439,
    "codeSnippet": { "code": "<div><div>", "lang": "HTML" }
  },
  {
    "id": "e6c9baff-1d83-467c-b982-b02f059e882a",
    "title": "title",
    "description": "html code",
    "ownerId": "cce8594a-0e36-467d-9dd3-efe9c8376c94",
    "createdAt": 1674702539,
    "codeSnippet": { "code": "<div><div>", "lang": "HTML" }
  },
  {
    "id": "b114aae1-5c5e-4ad7-910f-4f302535dfcb",
    "title": "title",
    "description": "html code",
    "ownerId": "cce8594a-0e36-467d-9dd3-efe9c8376c94",
    "createdAt": 1674702639,
    "codeSnippet": { "code": "<div><div>", "lang": "HTML" }
  },
  {
    "id": "1e03273d-32f3-49e1-aa4e-15e03a24049e",
    "title": "title",
    "description": "html code",
    "ownerId": "cce8594a-0e36-467d-9dd3-efe9c8376c94",
    "createdAt": 1674702739,
    "codeSnippet": { "code": "<div><div>", "lang": "HTML" }
  }
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


# user fixtures

@pytest.fixture(name="mock_user")
def mock_user():
    user = {
        "username": "mock_username",
        "name": "mock_name",
        "password": "mock_password",
        "contactInfo": {"email": "mock@email.com", "github":"https://github.com/L-Figgins"},
    }
    yield user


@pytest.fixture()
def serialized_user(mock_uuid):
    redis_serialized = {
        "id": mock_uuid,
        "username": "mock_username",
        "name": "mock_name",
        "password": "mock_password",
        "email": "mock@email.com",
        "github": "https://github.com/L-Figgins"
    }

    yield redis_serialized


#auth fixtures
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='mock_username', password='mock_password'):
        return self._client.post(
            '/auth/login',
            json={"payload":{'username': username, 'password': password, }}
        )

    def register(self):
        payload = {
            "username": "mock_username",
            "name":"mock_name",
            "password": "mock_password",
            "contactInfo": {"email": "mock@email.com", "github":"https://github.com/L-Figgins"}
        }

        self._client.post("/auth/register", json={"payload":payload})
        
    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    yield AuthActions(client)
