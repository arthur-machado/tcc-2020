#importa os metodos
from flask import render_template, redirect
from app import app

from app.models.forms import RegisterForm, LoginForm
from app.controllers.firebase import User

#defini rotas e seus respetivos acontecimentos
@app.route("/registro/", methods=["GET", "POST"])
def registro():
    #'chama' o formulário
    form = RegisterForm()
    if form.validate_on_submit():
        #'chama' a classe
        user = User()
        #pega os dados informados pelo usuario
        user.name = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        #'chama' o metodo InsertUser
        user.InsertUser()
        #redireciona para página de login
        return redirect('/login')
    return render_template('register.html', form=form)

@app.route("/")
@app.route("/login/", methods=["GET", "POST"])
def login():
    #'chama' o formulário
    form = LoginForm()
    if form.validate_on_submit():
        #'chama' a classe
        user = User()
        #pega os dados informados pelo usuario
        user.email = form.email.data
        user.password = form.password.data
        #'chama' a funcao Login
        if user.Login() == True:
            return redirect('/meuspets')
        else:
            render_template('login.html', error="Credenciais inválidas")
    return render_template('login.html', form=form)

@app.route("/cadastropet/")
def cadastropet():
    return render_template('cadastroPet.html')

@app.route("/meuperfil/")
def meuperfil():
    return render_template('meuperfil.html')

@app.route("/meuspets/")
def meuspets():
    return render_template('meuspets.html')

@app.route("/editarpet/")
def editarpet():
    return render_template('editarpet.html')



