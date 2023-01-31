from os import getenv

class Config:
    """
    Flask configuration object
    """
    SECRET_KEY = getenv('SECRET', "")
    FLASK_APP = getenv("codespace_backend", "")
