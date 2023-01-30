from ..db import get_db
from .keys import articles_key, article_by_create_at_key
from .schemas import ArticleSchema

def create_article(article: dict, user_id: str) -> int:
    # redis
    r = get_db()
    # article id
    # article_id = gen_id()
    # ts = get_utc_timestamp()
    # serialized = serialize(article, created_at=ts, user_id=user_id, art_id=article_id)
    article["owner_id"] = user_id
    schema = ArticleSchema()
    art = schema.load(article)
    pipe = r.pipeline()
    pipe.hset(
        articles_key(art.get("id")),
        mapping=art,
    )
    print(art.get('created_at'))
    #redis sorted set for mapping uuid ("member") to "created_at" score
    zset_mapping = {art.get("id"): int(art.get('created_at'))}

    pipe.zadd(article_by_create_at_key(), mapping=zset_mapping)
    pipe.execute()

    return art.get("id")


# since this app's MVP only expects a single user we do not yet need define
# data structures for queriying them by username, only by creation date for now
def get_articles_by_creation_date(offset=0, count=10, desc=False):
    r = get_db()
    get = [
        "#",
        f"{articles_key('*')}->title",
        f"{articles_key('*')}->description",
        f"{articles_key('*')}->owner_id",
        f"{articles_key('*')}->created_at",
        f"{articles_key('*')}->code",
        f"{articles_key('*')}->lang",
    ]
    ouput = r.sort(
        article_by_create_at_key(),
        start=offset,
        num=count,
        by="nosort",
        get=get,
        groups=True,
    )
    results = [
        deserialize(
            {
                "id": id,
                "title": title,
                "description": description,
                "owner_id": owner_id,
                "created_at": created_at,
                "code": code,
                "lang": lang,
            }
        )
        for id, title, description, owner_id, created_at, code, lang in ouput
    ]

    return results


def serialize(article: dict, created_at: int, user_id: str, art_id: str):
    # don't mute article
    result = article.copy()
    code, lang = result.pop("codeSnippet").values()
    result["id"] = art_id
    result["code"] = code
    result["lang"] = lang
    result["owner_id"] = user_id
    result["created_at"] = str(created_at)

    return result


def deserialize(article: dict) -> dict:
    result = {"code_snippet": {}}
    SNIPPET_KEYS = {"code", "lang"}
    INT_KEYS = {"created_at"}

    for k, v in article.items():
        if k in INT_KEYS:
            v = int(v)
        if k in SNIPPET_KEYS:
            result["code_snippet"][k] = v
            continue
        result[k] = v

    return result
