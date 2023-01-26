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
