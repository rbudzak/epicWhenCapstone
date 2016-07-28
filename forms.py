from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class PostForm(Form):

  title = StringField('title', validators=[DataRequired()])
  url = StringField('url', validators=[DataRequired()])
  game = IntegerField('game', validators=[DataRequired()])

class UserForm(Form):

  username = StringField('username', validators=[DataRequired()])
  password = StringField('password', validators=[DataRequired()])