from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import Email, InputRequired, Length, EqualTo


class RegisterForm(FlaskForm):
    email = TextField('Email', [InputRequired(), Email()])
    password = PasswordField('Password',
                             [InputRequired(),
                              EqualTo('confirm_password'),
                              Length(8, 16, message='Password must be between 8-16 characters.')
                              ])
    confirm_password = PasswordField('Confirm Password', [InputRequired()])


class LoginForm(FlaskForm):
    email = TextField('Email', [InputRequired(), Email()])
    password = PasswordField('Password', [InputRequired(),])
