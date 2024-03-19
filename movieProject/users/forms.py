from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Email
from model import User


class LoginForm(FlaskForm):
    email = StringField('email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email = StringField('email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password: ', validators=[DataRequired()])
    submit = SubmitField('Register!')


    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already taken. Try again')
