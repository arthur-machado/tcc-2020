#importa os metodos
from flask import render_template
from app import app

from app.models.forms import RegisterForm


#defini rotas e seus respetivos acontecimentos
@app.route("/registro/", methods=["GET", "POST"])
def registro():
    form = RegisterForm()
    if form.validate_on_submit():
        print("Nome: %s \nE-mail: %s \nSenha: %s" % (form.username.data, form.email.data, form.password.data))
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



