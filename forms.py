from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Email, EqualTo, ValidationError
from flaskdmscreen.models import User



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() # Checks if theres a user in the database
        if user:
            raise ValidationError('Username is taken!')
    
    def validate_email(self, email_address):
        email = User.query.filter_by(email=email_address.data).first() # Checks if theres a user in the database
        if email:
            raise ValidationError('Email is already in use!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first() # Checks if theres a user in the database
            if user:
                raise ValidationError('Username is taken!')
    
    def validate_email(self, email_address):
        if email_address.data != current_user.email: # Checks to see if they have tried to change email, if so, check against database to see if email already exists and its valid
            email = User.query.filter_by(email=email_address.data).first() # Checks if theres a user in the database
            if email:
                raise ValidationError('Email is already in use!')

class UploadStatblock(FlaskForm):
    statblock = FileField('Upload Statblock', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')
    print("IN UPLOAD VALIDATION FORMS")
    

class AddToCombat(FlaskForm):
    in_combat = BooleanField('Select Monster')
    submit = SubmitField('Add to Combat Tracker')

class AddPlayerToCombat(FlaskForm):
    player_name = SelectField('Player Name', coerce=int, choices=[])
    player_initiative_score = IntegerField('Player Initiative Score')
    submit = SubmitField('Add Player')

class InitiativeForm(FlaskForm):
    submit = SubmitField('Roll Initiative')

class PlayerForm(FlaskForm):
    player_name = StringField('Player Name')
    picture = FileField('Add Player Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add Player')

class PlayerManager(FlaskForm):
    player_initiative_score = IntegerField('Player Initiative Score')
    in_combat = BooleanField('Add to Combat')
    submit = SubmitField('Submit')