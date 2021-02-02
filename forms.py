from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class RegisterUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email(message="Not a valid email"), Length(max = 50), InputRequired()])
    first_name = StringField("First Name", validators=[Length(max=30), InputRequired()])
    last_name = StringField("Last Name", validators=[Length(max=30), InputRequired()])
    

class LoginUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    
class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[Length(max=100), InputRequired()])
    content = StringField("Content", validators=[InputRequired()])


    