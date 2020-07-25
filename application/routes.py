from flask import Flask, render_template, url_for, redirect, request, flash
from datetime import datetime

from application import db, app
from application.models import Article


db.create_all()


@app.route('/')
@app.route('/index')
def index():
          return render_template('index.html')


@app.route('/about')
def about():
          return render_template('about.html')


@app.route('/all_posts')
def all_posts():
          return render_template('all_posts.html',articles=Article.query.all())


@app.route('/new_post')
def new_post():
          return render_template('new_post.html')


@app.route('/add_article',methods=['POST'])
def add_article():
          text = request.form['text']

          db.session.add(Article(text))
          db.session.commit()

          return redirect(url_for('new_post'))