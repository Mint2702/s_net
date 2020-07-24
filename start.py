from flask import Flask, render_template, url_for


app=Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
          return render_template('index.html')


@app.route('/about')
def about():
          return render_template('about.html')


@app.route('/new_post')
def new_post():
          return render_template('new_post.html')


@app.route('/all_posts')
def all_posts():
          return render_template('all_posts.html')


if __name__=="__main__":
          app.run(debug=True)