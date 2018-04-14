from . import db
from datetime import datetime, timedelta

class FakeNews(db.Document):
    id = db.SequenceField(primary_key=True)
    counter = db.IntField()
    date = db.DateTimeField(default=datetime.utcnow)
    url = db.StringField()
    title = db.StringField()
    is_fake = db.BooleanField()

class User(db.Document):
    id = db.SequenceField(primary_key=True)
    username = db.StringField(required=True, unique=True)
    fake = db.IntField()
    real = db.IntField()
