from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db, app
from app.models import User


@app.route('/')
@app.route('/index')
def index():
          return render_template('index.html')


@app.route('/about')
def about():
          return render_template('about.html')


@app.route('/new_post')
def new_post():
          text = request.form['text']
          text = request.form['text']
          return render_template('new_post.html')


@app.route('/all_posts')
def all_posts():
          return render_template('all_posts.html')


@app.route('/new_user')
def new_user():
          return render_template('new_user.html')


@app.route('/commit', methods=['POST'])
def commit():
          username = request.form['username']
          password = request.form['password']

          db.session.add(User(username,password))
          db.session.commit()

          return redirect(url_for('index'))
