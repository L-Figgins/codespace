from ..db import get_db
from ..util import get_utc_timestamp, gen_id
from .keys import articles_key, article_by_create_at_key


def create_article(article: dict, user_id: str) -> int:
    # redis
    r = get_db()
    # article id
    article_id = gen_id()
    ts = get_utc_timestamp()
    serialized = serialize(article, created_at=ts, user_id=user_id)
    pipe = r.pipeline()
    pipe.hset(
        articles_key(article_id),
        mapping=serialized,
    )
    pipe.zadd(article_by_create_at_key(), mapping=(article_id, ts))
    pipe.execute()

    return article_id


def serialize(article: dict, created_at: int, user_id: str):
    # don't mute article
    result = article.copy()
    code, lang = result.pop("codeSnippet").values()

    result["code"] = code
    result["lang"] = lang
    result["owner_id"] = user_id
    result["created_at"] = created_at

    return result


def deserialize(article: dict) -> dict:
    result = {"code_snippet": {}}
    SNIPPET_KEYS = {"code", "lang"}

    for k, v in article.items():
        if k in SNIPPET_KEYS:
            result["code_snippet"][k] = v
            continue
        result[k] = v

    return result
