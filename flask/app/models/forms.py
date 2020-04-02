from flask_wtf  import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class RegisterForm(Form):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

class LoginForm(Form):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")
