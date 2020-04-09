from flask_wtf  import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

class ProfileForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
