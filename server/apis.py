from flask import Flask
from flask_restplus import Namespace, Resource, fields
from flask import request

from .models import FakeNews, User

from flask_restplus import Api
from bs4 import BeautifulSoup
import requests
import random

import sys

import logging
import urllib.parse

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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

        logging.debug('ChallengeResource.get(self=%s)', self)

        logging.debug('FakeNews.objects=%s', FakeNews.objects)

        fakes = [fake for fake in FakeNews.objects(is_fake=True) ]
        reals = [fake for fake in FakeNews.objects(is_fake=False) ]

        logging.debug('Got fakes=%s, reals=%s', fakes, reals)

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
        logging.debug("FakeNewsResource.post(self=%s)", self)
        data = request.json
        logging.debug("FakeNewsResource.post:Got data=", data)
        try:
            url=data['url']
            logging.debug("FakeNewsResource.post: Before FakeNews.objects.get: url=" + url)
            #
            # NOTE: Will raise exception if the url is unknown
            # Maywe we should instead check if the object exists
            #
            fake = FakeNews.objects.get(url=data['url'])
            logging.debug("After FakeNews.objects.get: fake=%s", fake)
        except:
            logging.debug("Not in cache, creating FakeNews(url=%s, counter=%d)", data['url'], 0)
            fake = FakeNews(url=data['url'], counter = 0)
            logging.debug("FakeNewsResource.post: fake=%s", fake)
            #
            # FIXME: Double exception may happen here!
            #
            fake.title = get_title_from_url(data['url'])
            # fake.title = "FIXME: This is a Fake title"
            logging.debug("FakeNewsResource.post: fake.title=%s", fake.title)
           
            # r = requests.get('https://api.fakenewsdetector.org/votes?url={}&title='
            #        .format(urllib.urlencode(data['url'])))
            logging.debug("FakeNewsResource.post: data=%s", data)
            # logging.debug("FakeNewsResource.post: data['url']=%s", data['url'])
            str_data_url = str(data['url'])
            logging.debug("FakeNewsResource.post: str_data_url=%s", str_data_url)
            str_data_url_encoded = urllib.parse.quote(str_data_url)
            # logging.debug("FakeNewsResource.post: str_data_url_encoded=%s", str_data_url_encoded)
            request_url = 'https://api.fakenewsdetector.org/votes?url={}&title='.format(str_data_url_encoded)
            logging.debug("FakeNewsResource.post: request_url=%s", request_url)
            r = requests.get(request_url);
            logging.debug("FakeNewsResource.post: Got r=%s", r)
            logging.debug("FakeNewsResource.post: Got r.json()=%s", r.json())
            #
            # FIXME: Double exception may happen here!
            #
            t_people = r.json()['people']
            logging.debug("FakeNewsResource.post: Got t_people=%s", t_people)
            #
            t_content = t_people['content']
            logging.debug("FakeNewsResource.post: Got t_content=%s", t_content)
            #
            t_robot = r.json()['robot']
            logging.debug("FakeNewsResource.post: Got t_robot=%s", t_robot)
            #
            t_fakenews = r.json()['robot']['fake_news']
            logging.debug("FakeNewsResource.post: Got t_fakenews=%s", t_fakenews)
            #
            chance = 0.0
            # for d in r.json()['people']['content']:
            #     logging.debug("FakeNewsResource.post: Inside loop: Got d=%s", d)
            #     if d['category_id'] == 2:
            #         chance = d['chance']
            #         logging.debug("FakeNewsResource.post: Inside loop: Got chance=%s", chance)
            #
            chance = r.json()['robot']['fake_news'];
            #
            logging.debug("FakeNewsResource.post: Overall chance=%s", chance)
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

# Got r.json()=
'''
  'robot': {
      'clickbait': 0.37361637,
      'fake_news': 0.0,
      'extremely_biased': 0.0
  },
  'domain': None,
  'people': {
      'title': {
          'clickbait': False,
          'count': -1
      },
      'content': [
          {'count': 1, 'category_id': 1}
      ]
  },
  'keywords': []
}
'''



# EOF
