from marshmallow import Schema, fields, pre_load, post_dump
from ..util import gen_id, get_utc_timestamp


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class ArticleSchema(Schema):
    id = fields.Str(load_default=lambda:gen_id())
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    created_at = fields.Str(required=True)
    owner_id = fields.Str(required=True)
    code = fields.Str()
    lang = fields.Str()
    count = 0

    @pre_load
    def prepare_for_redis(self, data, **kwargs):
        # js uses camel case

        code_snippet = data.pop("codeSnippet")
        data["code"] = code_snippet.get("code", "")
        data["lang"] = code_snippet.get("lang", "")
        data["created_at"] = str(get_utc_timestamp())

        return data

    @post_dump()
    def serialze(self, data, many, **kwargs):
        code = data.pop("code")
        lang = data.pop("lang")
        data["codeSnippet"] = {"code": code, "lang": lang}
        
        created_at = data.pop("created_at")
        data["createdAt"] = int(created_at)

        owner_id = data.pop("owner_id")
        data["ownerId"] = owner_id

        return data
