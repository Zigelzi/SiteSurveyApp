from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from sitesurvey import data_req_msg


# Form for logging in to the site.
class LogInForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(message=data_req_msg), Email(message="Not valid email")])
    password = PasswordField('Password',
                             validators=[DataRequired(message=data_req_msg)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class RequestPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(data_req_msg),
                         Email(message='Not valid email')])
    submit = SubmitField('Request Password Reset')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')
