from flask_wtf  import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired

class RegisterUserForm(FlaskForm):
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

class RegisterDogForm(FlaskForm):
    #adicionar foto
    dogname = StringField("dogname", validators=[DataRequired()])
    age = StringField("age", validators=[DataRequired()])
    weight = StringField("weight", validators=[DataRequired()])
    breed = SelectField("breed", choices=[('SRD', 'SRD'), ('PA','Pastor Alemão'), ('S', 'Salsicha'), ('GR', 'Golden Retriever'), ('L', 'Labrador'), ('O', 'Outro')])
