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

    from .test_api import test_bp
    app.register_blueprint(test_bp)

    @app.route('/test/counter')
    @as_json
    def test_cnt():
        return {'counter': randint(0, 100)}


    @app.route('/test/fakenews')
    @as_json
    def test_fakenews():
        return {
           'fakenews': [
                {
                    "url": "/blabla",
                    "counter": "10",
                    "$uri": "/",
                    "users": ["gmacario", "ludusrusso"],
                    "$date": "timestamp"
                },
                {
                    "url": "/blabla",
                    "counter": "10",
                    "$uri": "/",
                    "users": ["gmacario", "ludusrusso"],
                    "$date": "timestamp"
                }
            ]
        }

    @app.route('/test/users')
    @as_json
    def test_users():
        return {
           'users': [
                {
                    "user": "gmacario",
                    "counter": "10",
                    "urls": ["url", "url"] 
                },
                {
                    "user": "ludusrusso",
                    "counter": "7",
                    "urls": ["url", "url"] 
                }
            ]
        }

    return app