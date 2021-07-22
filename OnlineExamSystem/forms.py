from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed , FileRequired
from wtforms import StringField , PasswordField  , SubmitField , BooleanField , TextAreaField , SelectField , IntegerField
from wtforms.validators import DataRequired , Length , Email , EqualTo , ValidationError , NumberRange
from OnlineExamSystem.models import User

class RegistrationForm(FlaskForm) :

    name = StringField(
        'Name' , validators = [DataRequired() , Length(min=5 , max=40)]
    )

    username = StringField(
        'Username' , validators = [DataRequired() , Length(min=2 , max=20)]
    )
    gender = SelectField(
        'Gender', choices = ['Male', 'Female']
    )
    password = PasswordField(
        'Password' , validators = [DataRequired() , EqualTo('confirm_pass')]
    )
    confirm_pass = PasswordField(
        'Confirm Password' , validators = [DataRequired() , EqualTo('password')]
    )
    submit = SubmitField('Sign Up')

    def validate_username(self , username) :
        user = User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError('Username Already Exists')
 

class LoginForm(FlaskForm) :
    username = StringField(
        'Username' , validators = [DataRequired() , Length(min=2 , max=20)]
    )
    password = PasswordField(
        'Password' , validators = [DataRequired()]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm) :

    name = StringField(
        'Name' , validators = [DataRequired() , Length(min=5 , max=40)]
    )

    username = StringField(
        'Username' , validators = [DataRequired() , Length(min=2 , max=20)]
    )
    gender = SelectField(
        'Gender', choices = ['Male', 'Female']
    )
    submit = SubmitField('Update')

    def validate_username(self , username) :
        user = User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError('Username Already Exists')

class QuestionForm(FlaskForm) :

    question = TextAreaField(
        'Question' , validators = [DataRequired()]
    )
    difficulty = IntegerField(
        'Difficulty' , validators = [DataRequired() , NumberRange(min=1 , max=5)]
    )
    option1 = StringField(
        'Option 1' , validators = [DataRequired()]
    )
    option2 = StringField(
        'Option 2' , validators = [DataRequired()]
    )
    option3 = StringField(
        'Option 3' , validators = []
    )
    option4 = StringField(
        'Option 4' , validators = []
    )

    correct = IntegerField(
        'Correct' , validators=[DataRequired() ,  NumberRange(min=1 , max=4)]
    )
    submit = SubmitField('Add')

class TestForm(FlaskForm) :

    options = SelectField(
        'Your Response' , choices = [(0 , 'None') , (1 , 1) , (2 , 2) , (3 , 3) , (4 , 4)]
    )

    submit = SubmitField('Submit')