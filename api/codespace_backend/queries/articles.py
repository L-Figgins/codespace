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
            {
                "id": id,
                "title": title,
                "description": description,
                "owner_id": owner_id,
                "created_at": created_at,
                "code": code,
                "lang": lang,
            }
        for id, title, description, owner_id, created_at, code, lang in ouput
    ]
    schema = ArticleSchema(many=True)
    results = schema.dump(results)

    return results
