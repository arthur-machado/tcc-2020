#importa os metodos
from flask import render_template, redirect, url_for, flash, request
from app import app

from app.models.forms import RegisterUserForm, RegisterDogForm, LoginForm, ProfileForm
from app.controllers.firebase import User, Dog

#defini rotas e seus respetivos acontecimentos
@app.route("/registro/", methods=["GET", "POST"])
def registro():
    #'chama' o formulário
    form = RegisterUserForm()
    if form.validate_on_submit():
        #'chama' a classe User
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
        #'chama' a classe User
        user = User()
        #'pega' os dados informados pelo usuario
        user.username = form.username.data
        user.password = form.password.data
        #'chama' a funcao Login
        if user.Login() == True:
            return redirect(url_for('meuspets'))
        else:
            flash('Usuário e/ou senha inválidos')
    return render_template('login.html', form=form)

@app.route("/meuperfil/", methods=["GET", "POST"])
def meuperfil():
    #'chama' a classe User
    user = User()
    #'chama' o metodo ReadUser
    credentials = user.CheckLogin()
    if credentials == "access denied":
        return redirect(url_for('login'))
    elif credentials == "logged":
        #'chama' o formulário
        form = ProfileForm()
        #'chama' a classe User
        user = User()
        #'chama' o metodo ReadUser
        user_data = user.ReadUser()
        #testa se ocorreu algum problema ao encontrar dados do usuário
        if user_data == None:
            flash('Dados do usuário não encontrados')
        else:
            form.username.data = user_data[0]
            form.email.data = user_data[1]
            form.password.data = user_data[2]
        if form.validate_on_submit():
            user.Logout()
            return redirect(url_for('login'))

        return render_template('meuperfil.html', form=form)

@app.route("/cadastropet/", methods=["GET", "POST"])
def cadastropet():
    #'chama' a classe User
    user = User()
    #'chama' o metodo ReadUser
    credentials = user.CheckLogin()
    if credentials == "access denied":
        return redirect(url_for('login'))
    elif credentials == "logged":
        #'chama' o formulário
        form = RegisterDogForm()
        if form.validate_on_submit():
            #'chama' a classe Dog
            dog = Dog()
            #pega os dados informados pelo usuario
            dog.dogname = form.dogname.data
            dog.age = form.age.data
            dog.weight = form.weight.data
            dog.breed = form.breed.data
            #'chama' o metodo InsertDog
            validacao = dog.InsertDog()
            if validacao == "Cão já cadastrado":
                flash('Cão já cadastrado')
            elif validacao == "Erro":
                flash('Erro')
            elif validacao == "Feito":
                return redirect(url_for('meuspets'))
        return render_template('cadastroPet.html', form=form)

@app.route("/meuspets/")
def meuspets():
    #'chama' a classe User
    user = User()
    #'chama' o metodo ReadUser
    credentials = user.CheckLogin()
    if credentials == "access denied":
        return redirect(url_for('login'))
    elif credentials == "logged":
        #'chama' a classe Dog
        dog = Dog()
        #'chama' o metodo ReadDog
        dog_data = dog.ReadDog()
        #testa se ocorreu algum problema ao encontrar dados do usuário
        if dog_data == None:
            flash('Nenhum cão foi cadastrado')
            return render_template('meuspets.html', dog_data=0)
        else:
            #pega o numero de caes na lista
            dogs_in_list=len(dog_data)
            return render_template('meuspets.html', dogs_in_list=dogs_in_list, dog_data=dog_data)

        return render_template('meuspets.html')

@app.route("/acompanhamento/")
def acompanhamento():
    #'chama' a classe User
    user = User()
    #'chama' o metodo ReadUser
    credentials = user.CheckLogin()
    if credentials == "access denied":
        return redirect(url_for('login'))
    elif credentials == "logged":
        #'chama' a classe Dog
        dog = Dog()
        #'chama' o metodo ReadDog
        dog_data = dog.ReadDog()
        #testa se ocorreu algum problema ao encontrar dados do usuário
        if dog_data == None:
            flash('Nenhum cão foi cadastrado')
            return render_template('acompanhamento.html', dog_data=0)
        else:
            #pega o numero de caes na lista
            dogs_in_list=len(dog_data)
            #esse valor, posteriormente, vai estar dentro de dog_data
            dog_status = "ok"
            return render_template('acompanhamento.html', dogs_in_list=dogs_in_list, dog_status=dog_status, dog_data=dog_data)

        return render_template('acompanhamento.html')

@app.route("/editarpet/<string:dog_id>", methods=["GET", "POST"])
def editarpet(dog_id):
    #'chama' o formulário
    form = RegisterDogForm()
    #'chama' a classe Dog
    dog = Dog()
    #defini qual cao a ser pesquisado
    dog.dogname = dog_id
    #'chama' o metodo SearchDog
    dog_data = dog.SearchDog()
#    if dog_id == None:
#        print("NÃO EXISTE ESSE CACHORRO")
#    else:
    form.dogname.data = dog_data[0]
    form.age.data = dog_data[1]
    form.weight.data = dog_data[3]

    if form.validate_on_submit():
        #'chama' a classe Dog
        dog = Dog()
        #pega os dados informados pelo usuario
        dog.dogname = form.dogname.data
        dog.age = form.age.data
        dog.weight = form.weight.data
        dog.breed = "racaqualquer"
        print("AGE: %d \nWEIGHT: %d" % (dog.age, dog.weight))
        #'chama' o metodo InsertDog 
        if dog.EditDog() == "ok":
            print("FUI")
            return redirect(url_for('meuspets'))
    return render_template('editarpet.html', form=form)

@app.route("/historico/")
def historico():
    #'chama' a classe User
    user = User()
    #'chama' o metodo ReadUser
    credentials = user.CheckLogin()
    if credentials == "access denied":
        return redirect(url_for('login'))
    elif credentials == "logged":
        return render_template('historico.html')

@app.route("/avisos/")
def avisos():
    #'chama' a classe User
    user = User()
    #'chama' o metodo ReadUser
    credentials = user.CheckLogin()
    if credentials == "access denied":
        return redirect(url_for('login'))
    elif credentials == "logged":
        return render_template('avisos.html')


