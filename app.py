#imports
from flask import Flask, request, redirect, url_for, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from forms import PostForm, UserForm
from flask_wtf import CsrfProtect
from datetime import datetime

#config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/epic-when-capstone'
app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
db = SQLAlchemy(app)

CsrfProtect(app)
app.config['SECRET_KEY'] = "such secret" #Store this elsewhere

#models
class User(db.Model):

  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.Text(), unique=True)
  password = db.Column(db.Text())

  def __init__(self, user, password):
    self.user = user
    self.password = password

class Post(db.Model):

  __tablename__ = 'posts'
  
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.Text())
  url = db.Column(db.Text())
  game = db.Column(db.Text())
  u_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
  timestamp = db.Column(db.DateTime())

  users = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))

  def __init__(self, title, url, game, timestamp):
    self.title = title
    self.url = url
    self.game = game
    self.timestamp = datetime.utcnow()


#routes - posts
@app.route('/')
def root():
  return redirect(url_for('index'))

@app.route('/posts')
def index():
  return render_template('index.html', posts=Post.query.all())

@app.route('/posts/new')
def new():
  return render_template('newpost.html', form=PostForm())

@app.route('/posts', methods=['POST'])
def create():
  form = PostForm()
  if form.validate_on_submit():
    new_post = Post(form.title.data, form.url.data, form.game.data, form.user.data)
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('index'))
  return render_template('newpost.html', form=form)

#routes - users
@app.route('/users')
def userList():
  return render_template('users.html', posts=User.query.all())

@app.route('/users/new')
def newUser():
  return render_template('newuser.html', form=PostForm())

@app.route('/users', methods=['POST'])
def createUser():
  form = UserForm()
  if form.validate_on_submit():
    new_user = User(form.username.data, form.password.data)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('index'))
  return render_template('newuser.html', form=form)

if __name__ == '__main__':
  app.run(debug=True, port=3000)

