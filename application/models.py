from flask_login import UserMixin

from application import db,manager



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)

    def __init__(self, text):
        self.text = text


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(240), nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
