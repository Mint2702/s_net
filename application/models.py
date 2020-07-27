from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash

from application import db,manager



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(520), nullable=False)
    articles = db.relationship('Article', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    intro=db.Column(db.String(300),nullable=False)
    text=db.Column(db.Text,nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __init__(self, title,intro,text,user_id):
        self.title = title
        self.intro = intro
        self.text = text
        self.user_id = user_id


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
