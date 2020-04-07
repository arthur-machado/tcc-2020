#importa os metodos
from flask import render_template, redirect, url_for, flash
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
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        #'chama' o metodo InsertUser
        validacao = user.InsertUser()
        #redireciona para página de login
            #if validacao == "Usuário e E-mail já cadastrados":
            #   flash('Usuário e E-mail já cadastrados')
        if validacao == "Usuário já cadastrado":
            flash('Usuário já cadastrado')
            #elif validacao == "E-mail já cadastrado"
            #    flash('E-mail já cadastrado')
        elif validacao == "Erro":
            flash('Erro')
        else:
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    #'chama' o formulário
    form = LoginForm()
    if form.validate_on_submit():
        #'chama' a classe
        user = User()
        #pega os dados informados pelo usuario
        user.username = form.username.data
        user.password = form.password.data
        #'chama' a funcao Login
        if user.Login() == True:
            return redirect(url_for('meuspets'))
        else:
            flash('Credenciais inválidas')
    return render_template('login.html', form=form)

@app.route("/meuperfil/", methods=["GET", "POST"])
def meuperfil():
    #'chama' o formulário
#    form = ProfileForm()
#    if form.validate_on_submit():
        #'chama' a classe
#        user = User()
        #pega os dados do campo
#        user.username = form.username.data
#        user.email = form.email.data
#        user.password = form.password.data
        #'chama' a funcao Editar
#        if user.Login() == True:
#            return redirect(url_for('meuspets'))
#        else:
#            flash('Credenciais inválidas')
    return render_template('meuperfil.html')

@app.route("/cadastropet/")
def cadastropet():
    return render_template('cadastroPet.html')


@app.route("/meuspets/")
def meuspets():
    return render_template('meuspets.html')

@app.route("/editarpet/")
def editarpet():
    return render_template('editarpet.html')



