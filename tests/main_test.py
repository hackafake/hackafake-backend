from datetime import datetime, timedelta

from flask_jwt_extended import decode_token, create_access_token
from jwt import ExpiredSignatureError
import pytest
from server.models import FakeNews, User

from mongoengine.errors import NotUniqueError

def test_app_running(client):
    res = client.get('/')
    assert res.status_code is not None
    

def test_fake_news(client, db):
    fake1 = FakeNews(url="", counter=10, is_fake=True).save()
    fake2 = FakeNews(url="", counter=20, is_fake=False).save()
    res = client.get('/counter')
    assert res.status_code == 200 
    fake = client.get('/counter').json['fake']
    cnt = client.get('/counter').json['real']
    assert fake == 10
    assert cnt == 20

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

    users = [u for u in User.objects]
    assert len(users) == 1
    assert users[0].username == 'ludusrusso'
    assert users[0].real == 1

    data["username"] = 'gmacario'
    data["url"] = 'https://www.zz7.it/trova-coccodrillo-nella-doccia-8953/'
    res = client.post('/fakenews', json=data)
    
    assert res.status_code == 200
    fakes = [f for f in FakeNews.objects]
    assert len(fakes) == 2
    assert fakes[1].url == 'https://www.zz7.it/trova-coccodrillo-nella-doccia-8953/'
    assert fakes[1].counter == 1

    users = [u for u in User.objects]
    assert len(users) == 2
    assert users[1].username == 'gmacario'
    assert users[1].fake == 1