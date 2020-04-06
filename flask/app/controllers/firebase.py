#importa os metodos
from firebase import firebase
from flask import jsonify, make_response, request, redirect


#configuracao do firebase
firebase =  firebase.FirebaseApplication("https://tcc2020-78c46.firebaseio.com/", None)

#defini classes, metodos
class User():
    name = ""
    email = ""
    password = ""
    #metodo para cadastrar usuario
    def InsertUser(self):
        data = {
            'Name': self.name,
            'Email': self.email,
            'Password': self.password
        }
        #pega somente o 'user' do email
            #achar outra solucao
        split = self.email.split('@')
        #envia os dados para o firebase
        result = firebase.put('Users/', split[0], data)
        return result
        
    def Login(self):
        #pega somente o 'user' do email
            #achar outra solucao
        split = self.email.split('@')
        #defini o 'validador'
        ticket = False
        #faz a consulta dos dados no banco
        usernameTicket = self.firebase.get('/Users', split[0]+'/Email')
        passwordTicket = self.firebase.get('/Users', split[0]+'/Password')
        #defini as condições
        if split[0] == emailTicket and self.email != None and self.password == passwordTicket and self.password != None:
            ticket = True
        elif split[0] == None or passwordTicket == None:
            ticket = False
        else:
            ticket = False
        return ticket
        

    