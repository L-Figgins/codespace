from marshmallow import Schema, fields, pre_load, post_dump, ValidationError
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
    markdown = fields.Str(required=False)
    code = fields.Str()
    lang = fields.Str()
    count = 0
    

    @pre_load
    def prepare_for_redis(self, data, **kwargs):
        # js uses camel case   
        code_snippet = data.pop("codeSnippet", {})
        data["code"] = code_snippet.get("code", "")
        data["lang"] = code_snippet.get("lang", "")
        data["created_at"] = str(get_utc_timestamp())
        return data

    @post_dump
    def serialze(self, data, many, **kwargs):
        code = data.pop("code")
        lang = data.pop("lang")
        data["codeSnippet"] = {"code": code, "lang": lang}
        
        created_at = data.pop("created_at")
        data["createdAt"] = int(created_at)

        owner_id = data.pop("owner_id")
        data["ownerId"] = owner_id

        return data

class UserSchema(Schema):
    id = fields.Str(load_default=lambda:gen_id())
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    name = fields.Str(required=True)
    image_url = fields.Str(required=False)
    email = fields.Email(required=True)
    github = fields.URL(required=True)
    #TODO validate its a valid phone number
    phone = fields.Str(required=False)
    linked_in = fields.URL(required=False)

    @pre_load
    def prepare_for_redis(self, data, **kwargs):
        try:
            contact_info = data.pop("contactInfo")
            data = {**data, **contact_info}
            # data["image_url"] = contact_info.get("imageURL", "")
            # data["email"] = contact_info.get("email")
            # data["github"] = contact_info.get("github", "")
            # data["phone"] = contact_info.get("phone", "")
            # data["linked_in"] = contact_info.get("linkedIn", "")
            return data
        except KeyError as e:
            raise ValidationError(str(e))
    
    @post_dump
    def serialize(self, data, **kwargs):
        contact_info = {
            "email": data.pop("email", ""),
            "imageURL": data.pop("image_url", ""),
            "github": data.pop("github", ""),
            "phone": data.pop("phone", ""),
            "linkedIn": data.pop("linked_in","")
        }
        data["contactInfo"] = contact_info

        return data
