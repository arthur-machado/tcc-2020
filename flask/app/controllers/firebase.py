#importa os metodos
from firebase import firebase
from flask import jsonify, make_response, request, redirect


#configuracao do firebase
firebase =  firebase.FirebaseApplication("https://tcc2020-78c46.firebaseio.com/", None)

#defini classes, metodos
class User():
    username = ""
    email = ""
    password = ""
    #metodo para cadastrar usuario
    def InsertUser(self):
        data = {
            'Username': self.username,
            'Email': self.email,
            'Password': self.password
        }
        #envia os dados para o firebase
        result = firebase.put('Users/', self.username, data)
        return result
        
    def Login(self):
        #pega os dados digitados
        #defini o 'validador'
        ticket = False
        #faz a consulta dos dados no banco
        usernameTicket = firebase.get('/Users/', self.username+'/Username')
        passwordTicket = firebase.get('/Users/', self.username+'/Password')
        #defini as condições
        if self.username == usernameTicket and self.username != None and self.password == passwordTicket and self.password != None:
            ticket = True
        elif self.username == None or passwordTicket == None:
            ticket = False
        else:
            ticket = False
        return ticket
        

    