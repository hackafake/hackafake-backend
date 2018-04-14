import os
from datetime import timedelta

class Config(object):
    RESTPLUS_VALIDATE = True

    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGODB_NAME') or 'default',
        'host': os.environ.get('MONGODB_URL') or 'mongomock://test'
    }


class TestConfig(Config):
    SECRET_KEY = 'test-super-secret'
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'test',
        'host': 'mongomock://test'
    }

class DockerConfig(Config):
    MONGODB_SETTINGS = {
        'db':  os.environ.get('MONGO_DB'),
        'host': os.environ.get('MONGO_URL')
    }


configs = {
    'default': Config,
    'testing': TestConfig,
    'docker': DockerConfig
}
