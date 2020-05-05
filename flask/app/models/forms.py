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
    #userphoto = FileField("userphoto", validators=[FileRequired()])
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])

class EditProfileForm(FlaskForm):
    #adicionar foto
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])

class RegisterDogForm(FlaskForm):
    #dogphoto = FileField("dogphoto", validators=[FileRequired(), FileAllowed(images, 'Somente imagens!')])
    dogname = StringField("dogname", validators=[DataRequired()])
    age = StringField("age", validators=[DataRequired()])
    weight = StringField("weight", validators=[DataRequired()])
    breed = SelectField("breed", choices=[('SRD', 'Sem Raça Definida'), ('Pastor Alemão','Pastor Alemão'), ('Salsicha', 'Salsicha'), ('Golden Retriever', 'Golden Retriever'), ('Labrador', 'Labrador'), ('Outro', 'Outro')])
    #adicionar sensor

class EditDogForm(FlaskForm):
    #adicionar foto
    dogname = StringField("dogname")
    age = StringField("age")
    weight = StringField("weight")
    breed = SelectField("breed", choices=[('SRD', 'Sem Raça Definida'), ('Pastor Alemão','Pastor Alemão'), ('Salsicha', 'Salsicha'), ('Golden Retriever', 'Golden Retriever'), ('Labrador', 'Labrador'), ('Outro', 'Outro')])
    #adicionar sensor
