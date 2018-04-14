from datetime import datetime, timedelta

from flask_jwt_extended import decode_token, create_access_token
from jwt import ExpiredSignatureError
import pytest

from mongoengine.errors import NotUniqueError

def test_app_running(client):
    res = client.get('/')
    assert res.status_code is not None
    

def test_api_cnt(client):
    res = client.get('/test/counter').json
    assert 'counter' in res
