from datetime import datetime, timedelta

from flask_jwt_extended import decode_token, create_access_token
from jwt import ExpiredSignatureError
import pytest
from server.models import FakeNews

from mongoengine.errors import NotUniqueError

def test_app_running(client):
    res = client.get('/')
    assert res.status_code is not None
    

def test_api_cnt(client):
    res = client.get('/test/counter').json
    assert 'counter' in res

def test_fake_news(client, db):
    fake1 = FakeNews(url="", counter=10).save()
    fake2 = FakeNews(url="", counter=20).save()
    res = client.get('/counter')
    assert res.status_code == 200 
    cnt = client.get('/counter').json['counter']
    assert cnt == 30

def test_post_fake_news(client, db):
    data = {
        'username': 'ludusrusso',
        'url': 'https://ludusrusso.cc/'
    }
    
    res = client.post('/fakenews', json=data)
    assert res.status_code == 200

    fakes = [f for f in FakeNews.objects]
    assert len(fakes) == 1
    assert fakes[0].url == 'https://ludusrusso.cc/'
    assert fakes[0].counter == 1

    res = client.post('/fakenews', json=data)
    assert res.status_code == 200
    fakes = [f for f in FakeNews.objects]
    assert len(fakes) == 1
    assert fakes[0].url == 'https://ludusrusso.cc/'
    assert fakes[0].counter == 2

