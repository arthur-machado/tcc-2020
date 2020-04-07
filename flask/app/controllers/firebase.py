#importa os metodos
from firebase import firebase
from flask import jsonify, make_response, request, redirect


#configuracao do firebase
firebase =  firebase.FirebaseApplication("https://tcc2020-78c46.firebaseio.com/", None)

#defini classes, metodos
class User():
    #dados comuns do usuario
    username = ""
    email = ""
    password = ""
    #variavel que armazena o usuario 'logado' no momento
    logged = ""

    #metodo para cadastrar usuario
    def InsertUser(self):
        data = {
            'Username': self.username,
            'Email': self.email,
            'Password': self.password
        }
        #defini o 'resultado'
        result = ""
        #pesquisa se já existe o username cadastrado
        usernameTicket = firebase.get('/Users/', self.username+'/Username')
            #achar uma forma de verificar o email
            #emailTicket = firebase.get('/Users/', self.username+'/Email')
            #if usernameTicket == self.username and emailTicket == self.email:
            #    result = "Usuário e E-mail já cadastrados"
        if usernameTicket == self.username:
            result = "Usuário já cadastrado"
            #elif emailTicket == self.email:
            #    result = "E-mail já cadastrado"
        elif usernameTicket == None:
            #envia os dados para o firebase
            result = firebase.put('Users/', self.username, data)
        else:
            result = "Erro"
        return result
        
    def Login(self):
        #defini o 'validador'
        ticket = False
        #faz a consulta dos dados na base
        usernameTicket = firebase.get('/Users/', self.username+'/Username')
        passwordTicket = firebase.get('/Users/', self.username+'/Password')
        #defini as condições entre os dados digitados e os encontrados na base de dados
        if self.username == usernameTicket and self.username != None and self.password == passwordTicket and self.password != None:
            ticket = True
        elif self.username == None or passwordTicket == None:
            ticket = False
        else:
            ticket = False
        return ticket

    def ReadUser(self):
        #faz a consulta dos dados na base
        FRusername = firebase.get('/Users/', self.logged+'/Username')
        FRemail = firebase.get('/Users/', self.logged+'/Email')
        FRpassword = firebase.get('/Users/', self.logged+'/Password')
        #registra os dados lidos na base na lista
        user_data_received = [FRusername, FRemail, FRpassword]  
        return user_data_received
    
        


        

    