from flask import Flask
from flask_cors import CORS

from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from .configs import configs

from random import randint

from flask_json import as_json, FlaskJSON
db = MongoEngine()

def create_app(confname='default'):
    app = Flask(__name__)
    app.config.from_object(configs[confname])

    db.init_app(app)

    JWTManager(app)
    CORS(app)
    FlaskJSON(app)

    from .apis import api
    api.init_app(app)


    return app