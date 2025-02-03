from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.models import User
from flask_login import current_user

class EditProfileForm(FlaskForm):
    username = StringField('Username', 
                         validators=[DataRequired(), 
                                   Length(min=2, max=20)])
    
    email = StringField('Email',
                       validators=[DataRequired(), 
                                 Email()])
    
    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already taken. Please choose a different one.')
