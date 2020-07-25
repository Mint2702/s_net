from flask_login import UserMixin
from datetime import datetime

from application import db,manager



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    intro=db.Column(db.String(300),nullable=False)
    text=db.Column(db.Text,nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    def __init__(self, title,intro,text):
        self.title = title
        self.intro = intro
        self.text = text


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(240), nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
