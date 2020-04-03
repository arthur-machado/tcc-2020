#importa os metodos
from flask import render_template
from app import app

from app.models.forms import RegisterForm
from app.controllers.firebase import InsertUser

#defini rotas e seus respetivos acontecimentos
@app.route("/registro/", methods=["GET", "POST"])
def registro():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        password = form.password.data
        InsertUser(name, email, password)
    return render_template('register.html', form=form)

@app.route("/")
@app.route("/login/", methods=["GET", "POST"])
def login():
    return render_template('login.html')

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



