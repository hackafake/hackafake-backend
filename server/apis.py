from flask_restplus import Namespace, Resource, fields
from flask import request

from .models import FakeNews, User, NewsToUser

from flask_restplus import Api

api = Api(
    title='hackafake Open API',
    version='1.0',
    description='API for HackAFake',
)

fake_post_model = api.model('FakeNewsPost', {
    'url': fields.String,
    'user': fields.String,
})

fake_news_model = api.model('FakeNews', {
    'url': fields.String,
    'counter': fields.Integer
})




@api.route('/counter')
class CounterResource(Resource):
    def get(self):
        cnts = [fake.counter for fake in FakeNews.objects]
        return {'counter': sum(cnts)}


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
        return fake