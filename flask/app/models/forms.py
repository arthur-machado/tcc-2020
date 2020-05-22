from flask_wtf  import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired

#formulario de registro de usuarios 
class RegisterUserForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

#formulario de login
class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

#formulario de visualizacao de perfil usuario
class ProfileForm(FlaskForm):
    #userphoto = FileField("userphoto")
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])

#formulario de edicao de perfil de usuario
class EditProfileForm(FlaskForm):
    #userphoto = FileField("userphoto")
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])

#formulario de registro de caes
class RegisterDogForm(FlaskForm):
    #dogphoto = FileField("dogphoto", validators=[FileRequired(), FileAllowed(images, 'Somente imagens!')])
    dogname = StringField("dogname", validators=[DataRequired()])
    age = StringField("age", validators=[DataRequired()])
    weight = StringField("weight", validators=[DataRequired()])
    breed = SelectField("breed", choices=[('SRD', 'Sem Raça Definida'), ('Pastor Alemão','Pastor Alemão'), ('Salsicha', 'Salsicha'), ('Golden Retriever', 'Golden Retriever'), ('Labrador', 'Labrador'), ('Outro', 'Outro')])
    #adicionar sensor

#formulario de edicao de perfil de caes
class EditDogForm(FlaskForm):
    #adicionar foto
    dogname = StringField("dogname")
    age = StringField("age")
    weight = StringField("weight")
    breed = SelectField("breed", choices=[('SRD', 'Sem Raça Definida'), ('Pastor Alemão','Pastor Alemão'), ('Salsicha', 'Salsicha'), ('Golden Retriever', 'Golden Retriever'), ('Labrador', 'Labrador'), ('Outro', 'Outro')])
    #adicionar sensor

#formulario de selecao de data para pesquisa no historico de media de BPM do cao
#class HistoryDate(FlaskForm):
    #LW = Last Week | LM = Last Month | LY = Last Year
    #datelimit = SelectField("breed", choices=[('LW', 'Últimos 7 dias'), ('LM','Último mês'), ('LY', 'Último ano')])

