from flask import Flask, render_template, url_for, redirect, request, flash
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user,logout_user, login_required

from application import db, app
from application.models import Article,User


logged = False
user = None

@app.route('/')
@app.route('/index')
def index():
          global logged

          return render_template('index.html',logged=logged, user=user)


@app.route('/about')
def about():
          global logged

          return render_template('about.html',logged=logged, user=user)


@app.route('/all_posts')
def all_posts():
          global logged

          articles=Article.query.order_by(Article.date.desc()).all()
          return render_template('all_posts.html',articles=articles,logged=logged, user=user)


@app.route('/new_post')
@login_required
def new_post():
          global logged

          return render_template('new_post.html',logged=logged, user=user)


@app.route('/all_posts/<int:id>')
def full_post(id):
          global logged

          article=Article.query.get(id)
          return render_template('full_post.html',logged=logged,article=article, user=user)


@app.route('/add_article',methods=['POST'])
@login_required
def add_article():
          title=request.form['title']
          intro=request.form['intro']
          text=request.form['text']

          article=Article(title=title,intro=intro,text=text)

          try:
                    db.session.add(article)
                    db.session.commit()
                    return redirect('/all_posts')
          except:
                    return "There was a mistake"

          return redirect(url_for('new_post'))


@app.route('/login',methods=['GET','POST'])
def login_page():
          global logged
          global user

          login = request.form.get('login')
          password = request.form.get('password')

          if request.method == "POST":
                    if login and  password:
                              user = User.query.filter_by(login=login).first()

                              if user and check_password_hash(user.password, password):
                                        login_user(user)

                                        next_page = request.args.get('next')
                                        logged = True
                                        if next_page==None:
                                                  return redirect(url_for('index'))
                                        else:
                                                  return redirect(next_page)

                              else:
                                        flash('Check login and password')

                    else:
                              flash('Fill both login and password please')
          return render_template('login_page.html',logged=logged)


@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
          global logged

          logout_user()
          logged = False
          return redirect(url_for('index'))


@app.route('/register',methods=['GET','POST'])
def register():
          global logged

          login = request.form.get('login')
          password = request.form.get('password')
          password2 = request.form.get('password2')

          if request.method == "POST":
                    if not(login or password or password2):
                              flash("Please fill all fields")
                    elif password != password2:
                              flash("passwords differ")
                    else:
                              hash_pwd = generate_password_hash(password)
                              new_user = User(login=login, password=hash_pwd)

                              db.session.add(new_user)
                              db.session.commit()

                    return redirect(url_for('login_page'))

          return render_template('register.html',logged=logged)


@app.after_request
def redirect_to_signin(response):
          if response.status_code == 401:
                    return redirect(url_for('login_page') + '?next=' + request.url)
          return response
