#app factory

import os
from flask import Flask


def create_app(test_config=None):
    """Application Factory Pattern"""
   
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('codespace_backend.config.Config')

    # from pattern_ag_backend.models import db, migrate
    

    with app.app_context():
        from . import routes
        from . import db
        db.init_app(app)
        return app