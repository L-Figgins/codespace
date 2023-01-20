register_schema = {
    "$schema": "https://json-schema.org/draft/2019-09/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "default": {},
    "title": "Root Schema",
    "required": [
        "username",
        "password",
        "name",
        "imageUrl",
        "contactInfo"
    ],
    "properties": {
        "username": {
            "type": "string",
            "default": "",
            "title": "The username Schema",
            "examples": [
                "ausername"
            ]
        },
        "password": {
            "type": "string",
            "default": "",
            "title": "The password Schema",
            "examples": [
                "pass123"
            ]
        },
        "name": {
            "type": "string",
            "default": "",
            "title": "The name Schema",
            "examples": [
                "Mike Jones"
            ]
        },
        "imageUrl": {
            "type": "string",
            "default": "",
            "title": "The imageUrl Schema",
            "examples": [
                ""
            ]
        },
        "contactInfo": {
            "type": "object",
            "default": {},
            "title": "The contactInfo Schema",
            "required": [
                "email",
                "github",
                "phone",
                "linkedin"
            ],
            "properties": {
                "email": {
                    "type": "string",
                    "default": "",
                    "title": "The email Schema",
                    "examples": [
                        "email@gmail.com"
                    ]
                },
                "github": {
                    "type": "string",
                    "default": "",
                    "title": "The github Schema",
                    "examples": [
                        "github.com"
                    ]
                },
                "phone": {
                    "type": "string",
                    "default": "",
                    "title": "The phone Schema",
                    "examples": [
                        "62655555555"
                    ]
                },
                "linkedin": {
                    "type": "string",
                    "default": "",
                    "title": "The linkedin Schema",
                    "examples": [
                        "linkedin"
                    ]
                }
            },
            "examples": [{
                "email": "email@gmail.com",
                "github": "github.com",
                "phone": "62655555555",
                "linkedin": "linkedin"
            }]
        }
    },
    "examples": [{
        "username": "ausername",
        "password": "pass123",
        "name": "Mike Jones",
        "imageUrl": "",
        "contactInfo": {
            "email": "email@gmail.com",
            "github": "github.com",
            "phone": "62655555555",
            "linkedin": "linkedin"
        }
    }]
}