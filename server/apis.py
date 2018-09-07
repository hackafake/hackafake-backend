from flask_restplus import Namespace, Resource, fields
from flask import request

from .models import FakeNews, User

from flask_restplus import Api
from bs4 import BeautifulSoup
import requests
import random

import logging
import sys

def get_title_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return str(soup.find('title').string.strip()) or url
    
api = Api(
    title='hackafake Open API',
    version='1.0',
    description='API for HackAFake',
)

fake_post_model = api.model('FakeNewsPost', {
    'url': fields.String,
    'username': fields.String,
})

fake_news_model = api.model('FakeNews', {
    'url': fields.String,
    'counter': fields.Integer,
    'title': fields.String,
    'is_fake': fields.Boolean
})

user_model = api.model('User', {
    'username': fields.String,
    'fake': fields.Integer,
    'real': fields.Integer
})

true_fake_model = api.model('TrueFake', {
    'fake': fields.Nested(fake_news_model),
    'real': fields.Nested(fake_news_model)
})


@api.route('/counter')
class CounterResource(Resource):
    def get(self):
        fakes = [fake.counter for fake in FakeNews.objects(is_fake=True) ]
        reals = [fake.counter for fake in FakeNews.objects(is_fake=False) ]
        return {
            'fake': sum(fakes),
            'real': sum(reals)
            }

@api.route('/challenge')
class ChallengeResource(Resource):
    @api.marshal_with(true_fake_model)
    def get(self):
        
        fakes = [fake for fake in FakeNews.objects(is_fake=True) ]
        reals = [fake for fake in FakeNews.objects(is_fake=False) ]

        fake = random.choice(fakes)
        real = random.choice(reals)
        return {
            'fake': fake,
            'real': real
            }

@api.route('/users')
class UserResource(Resource):
    @api.marshal_with(user_model, as_list=True)
    def get(self):
        return sorted([user for user in User.objects], key=lambda user: user.fake, reverse=True)

@api.route('/fakenews')
class FakeNewsResource(Resource):
    @api.marshal_with(fake_news_model, as_list=True)
    def get(self):
        return sorted([fake for fake in FakeNews.objects if fake.is_fake == True], key=lambda news: news.counter, reverse=True)

    @api.expect(fake_post_model)
    @api.marshal_with(fake_news_model)
    def post(self):
        # logging.basicConfig(format='%(message)s')
        # logging.warn('I print to stderr by default')
        app.logger.info('For this you must change the level and add a handler.')
        # print('hello world')

        data = request.json
        println("DEBUG: apis.py: data=" + data)
        try:
            fake = FakeNews.objects.get(url=data['url'])
        except:
            fake = FakeNews(url=data['url'], counter = 0)
            fake.title = get_title_from_url(data['url'])
            r = requests.get('https://api.fakenewsdetector.org/votes?url={}&title='.format(data['url']))
            chance = 0.0
            for d in r.json()['content']['robot']:
                if d['category_id'] == 2:
                    chance = d['chance']
            fake.is_fake = chance > 0.5
        fake.counter += 1
        fake.save()
        try:
            user = User.objects.get(username=data['username'])
        except:
            user = User(username=data['username'], fake = 0, real = 0)
        if fake.is_fake:
            user.fake += 1
        else:
            user.real += 1
        user.save()
        
        return fake

# EOF
