from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired() , Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20), EqualTo('pass_confirm',    message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Save')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Login')