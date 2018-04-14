import pytest
from server import create_app

from flask import Response as BaseResponse, json
from flask.testing import FlaskClient
from werkzeug.utils import cached_property
# from server.models import User, Robot
import uuid


@pytest.fixture
def app():
    class Response(BaseResponse):
        @cached_property
        def json(self):
            return json.loads(self.data)

    class TestClient(FlaskClient):
        def open(self, *args, **kwargs):
            if 'json' in kwargs:
                kwargs['data'] = json.dumps(kwargs.pop('json'))
                kwargs['content_type'] = 'application/json'
            return super(TestClient, self).open(*args, **kwargs)

    app = create_app('testing')
    app.response_class = Response
    app.test_client_class = TestClient
    app.testing = True
    return app


@pytest.fixture(scope='function')
def db(app):
    from server import db as _db

    def drop_db():
        for collection in [User]:
            collection.drop_collection()
        _db.connection.drop_database('test')

    with app.app_context():
        yield _db
        drop_db()


@pytest.fixture
def client(app):
    return app.test_client()
