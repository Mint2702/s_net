from flask import Flask, render_template, url_for, redirect, request, flash
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user,logout_user, login_required

from application import db, app
from application.models import Article,User


user = None


@app.route('/')
@app.route('/index')
def index():
          return render_template('index.html', user=user)


@app.route('/about')
def about():
          return render_template('about.html', user=user)


@app.route('/all_posts')
def all_posts():
          articles=Article.query.order_by(Article.date.desc()).all()
          return render_template('all_posts.html',articles=articles, user=user)


@app.route('/new_post')
@login_required
def new_post():
          return render_template('new_post.html', user=user)


@app.route('/all_posts/<int:id>')
def full_post(id):
          article = Article.query.get(id)
          user_name = User.query.filter_by(id=article.user_id).first()
          return render_template('full_post.html',article=article, user=user,user_name=user_name.login,user_uni=user_name.university)


@app.route('/add_article',methods=['POST'])
@login_required
def add_article():
          title = request.form['title']
          intro = request.form['intro']
          text = request.form['text']
          user_id = user.id

          article = Article(title=title,intro=intro,text=text,user_id=user_id)

          try:
                    db.session.add(article)
                    db.session.commit()
                    return redirect('/all_posts')
          except:
                    return "There was a mistake"

          return redirect(url_for('new_post'))


@app.route('/login',methods=['GET','POST'])
def login_page():
          global user_full
          global user

          login = request.form.get('login')
          password = request.form.get('password')

          if request.method == "POST":
                    if login and  password:
                              user = User.query.filter_by(login=login).first()

                              if user and user.check_password(password):
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
          return render_template('login_page.html',user=user)


@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
          global user
          logout_user()
          user = None
          return redirect(url_for('index'))


@app.route('/register',methods=['GET','POST'])
def register():
          login = request.form.get('login')
          university = request.form.get('university')
          password = request.form.get('password')
          password2 = request.form.get('password2')

          if request.method == "POST":
                    if not(login or password or password2 or university):
                              flash("Please fill all fields")
                    elif password != password2:
                              flash("passwords differ")
                    else:
                              new_user = User(login=login,university = university)
                              new_user.set_password(password)

                              db.session.add(new_user)
                              db.session.commit()

                    return redirect(url_for('login_page'))

          return render_template('register.html',user=user)


@app.after_request
def redirect_to_signin(response):
          if response.status_code == 401:
                    return redirect(url_for('login_page') + '?next=' + request.url)
          return response
