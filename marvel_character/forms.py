from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()

class CharacterForm(FlaskForm):
    name = StringField('name')
    description = StringField('description')
    comics_appeared_in = IntegerField('comics_appeared_in')
    super_power = StringField('super_power')
    date_created = DateTimeField('date_created')
    submit_button = SubmitField()