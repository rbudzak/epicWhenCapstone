from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class PostForm(Form):

  # title = StringField('title', validators=[DataRequired()])
  # url = StringField('url', validators=[DataRequired()])
  vidurl = StringField('vidurl')
  vidtitle = StringField('vidtitle')
  # game = IntegerField('game')

# class UserForm(Form):

#   username = StringField('username', validators=[DataRequired()])
#   password = StringField('password', validators=[DataRequired()])