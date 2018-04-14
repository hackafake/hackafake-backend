from . import db
from datetime import datetime, timedelta

class FakeNews(db.Document):
    id = db.SequenceField(primary_key=True)
    counter = db.IntField()
    date = db.DateTimeField(default=datetime.utcnow)
    url = db.StringField()

class User(db.Document):
    id = db.SequenceField(primary_key=True)
    username = db.StringField(required=True, unique=True)
    counter = db.IntField()
