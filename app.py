#imports
from flask import Flask, request, redirect, url_for, flash, render_template, jsonify, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from forms import PostForm
from flask_wtf import CsrfProtect
from datetime import datetime
from functools import wraps
import os
import json
import requests

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
  name = db.Column(db.Text(), unique=True)
  password = db.Column(db.Text())

  def __init__(self, name, password):
    self.name = name
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

# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
  env = os.environ
  code = request.args.get('code')

  json_header = {'content-type': 'application/json'}

  token_url = "https://{domain}/oauth/token".format(domain='rbudzak.auth0.com')

  token_payload = {
    'client_id':     'il4kY37SVusYd9IDOeuIeqqiOhiti85i',
    'client_secret': 'oyOC8rLBBNUK0_xch6dlZQwSH1qSIW93p3ttMIj1Jfi9Ww0j2q5d-ICFFx8Ek5Ut',
    'redirect_uri':  'http://localhost:3000/callback',
    'code':          code,
    'grant_type':    'authorization_code'
  }

  token_info = requests.post(token_url, data=json.dumps(token_payload), headers = json_header).json()

  user_url = "https://{domain}/userinfo?access_token={access_token}" \
      .format(domain='rbudzak.auth0.com', access_token=token_info['access_token'])

  user_info = requests.get(user_url).json()

  # We're saving all user information into the session
  session['profile'] = user_info

  # Redirect to the User logged in page that you want here
  # In our case it's /dashboard
  return redirect(url_for('index'))


def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated


#routes - posts
@app.route('/')
def root():
  return redirect(url_for('index'))

@app.route('/posts')
def index():
  return render_template('index.html', posts=Post.query.all())

@app.route('/posts/new')
@requires_auth
def new():
  print(session['profile']['name'])
  return render_template('new.html', form=PostForm())

@app.route('/posts', methods=['POST'])
def create():
  form = PostForm()
  if form.validate_on_submit():
    new_post = Post(form.title.data, form.url.data, 'Overwatch', session['profile']['name'])
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('index'))
  return render_template('new.html', form=form)

# These have been commented out since all of my auth is handled by Auth0/Google
# #routes - users
# @app.route('/users')
# def userList():
#   return render_template('users.html', posts=User.query.all())

# @app.route('/users/new')
# def newUser():
#   return render_template('newuser.html', form=PostForm())

# @app.route('/users', methods=['POST'])
# def createUser():
#   form = UserForm()
#   if form.validate_on_submit():
#     new_user = User(form.username.data, form.password.data)
#     db.session.add(new_user)
#     db.session.commit()

#     return redirect(url_for('index'))
#   return render_template('newuser.html', form=form)


if __name__ == '__main__':
  app.run(debug=True, port=3000)

