from flask_restplus import Namespace, Resource, fields
from flask import request

from .models import FakeNews, User

from flask_restplus import Api

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
    'counter': fields.Integer
})

user_model = api.model('User', {
    'username': fields.String,
    'counter': fields.Integer
})

true_fake_model = api.model('TrueFake', {
    'fake': fields.String,
    'real': fields.String
})



@api.route('/counter')
class CounterResource(Resource):
    def get(self):
        cnts = [fake.counter for fake in FakeNews.objects]
        return {'counter': sum(cnts)}

@api.route('/challenge')
class ChallengeResource(Resource):
    @api.marshal_with(true_fake_model)
    def get(self):
        return {
            'fake': 'https://www.fake.com',
            'real': 'https://google.com'
        }
        


@api.route('/users')
class UserResource(Resource):
    @api.marshal_with(user_model, as_list=True)
    def get(self):
        return [user for user in User.objects]

@api.route('/fakenews')
class FakeNewsResource(Resource):
    @api.marshal_with(fake_news_model, as_list=True)
    def get(self):
        return [fake for fake in FakeNews.objects]

    @api.expect(fake_post_model)
    @api.marshal_with(fake_news_model)
    def post(self):
        data = request.json
        try:
            fake = FakeNews.objects.get(url=data['url'])
        except:
            fake = FakeNews(url=data['url'], counter = 0)
        fake.counter += 1
        fake.save()

        try:
            user = User.objects.get(username=data['username'])
        except:
            user = User(username=data['username'], counter = 0)
        user.counter += 1
        user.save()
        
        return fake