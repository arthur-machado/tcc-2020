from flask import render_template
from app import app

@app.route("/registro/")
def registro():
    return render_template('register.html')

@app.route("/")
@app.route("/login/")
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



