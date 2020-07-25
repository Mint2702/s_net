from datetime import datetime

from application import db



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)

    def __init__(self, text):
        self.text = text
        

