#importa os metodos
from firebase import firebase
import json

from app.models.functions import TransformationRequest


#configuracao do firebase
firebase =  firebase.FirebaseApplication("https://tcc2020-78c46.firebaseio.com/", None)

#'guarda' o usuário logado
logged = ""

#defini classes, metodos
class User():
    #dados comuns do usuario
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
            #'puxa' a variavel global para ser usada dentro do metodo
            global logged
            #defini o usuario que 'logou'
            logged = self.username
        elif self.username == None or passwordTicket == None:
            ticket = False
        else:
            ticket = False
        return ticket

    def ReadUser(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #faz a consulta dos dados na base
        FRusername = firebase.get('/Users/', logged+'/Username')
        FRemail = firebase.get('/Users/', logged+'/Email')
        FRpassword = firebase.get('/Users/', logged+'/Password')
        #registra os dados lidos na base na lista
        user_data_received = [FRusername, FRemail, FRpassword]
        return user_data_received
    
    def EditUser(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #defini os dados a serem editados
        data = {
            'Username': logged,
            'Email': self.email,
            'Password': self.password
        }
        firebase.put('Users/', logged, data)
        result = "ok"
        return result
        
class Dog():
    #dados comuns ao cao
    #adicionar foto
    dogname=""
    age=""
    weight=""
    breed=""

    def InsertDog(self):
        data = {
            'Dog_Name': self.dogname,
            'Age': self.age,
            'Weight': self.weight,
            'Breed': self.breed
        }
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #defini o 'resultado'
        result = "empty"
        #pesquisa se já existe o cao cadastrado
        dognameTicket = firebase.get('/Users/', logged+'/Dogs/'+self.dogname+'/Dog_Name')
        if dognameTicket == self.dogname:
            result = "Cão já cadastrado"
        elif dognameTicket == None:
            #envia os dados para o firebase
            firebase.put('Users/'+logged+'/Dogs', self.dogname, data)
            result = "Feito"
        else:
            result = "Erro"
        return result

    def ReadDog(self):
        #defini o result
        result = ""
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #pesquisa se já existe algum cao cadastrado
        dognameTicket = firebase.get('/Users/', logged+'/Dogs')
        if dognameTicket == None:
            result = None
        elif dognameTicket != None:
            #faz a consulta dos dados na base
            FRdogsid = firebase.get('/Users/', logged+'/Dogs')            
            #trata o dict com o metodo
            firebaseResult = TransformationRequest(FRdogsid)
            #utiliza o metodo json
            obj = json.loads(firebaseResult)
            #lista que armazena os id's de cada dicionario aninhado
            dogs_ids = []
            #for que pega os id's de cada cao
            for dogs in obj.values():
                dogs_ids.append(dogs['Dog_Name'])
            #cria lista que armazena os dados de cada cao
            dogsinf = []
            #for que pega os dados [nome, idade, raca, peso] de cada cachorro e salva na lista
            for dogs in dogs_ids:
                dogsdata = [obj[dogs]['Dog_Name'], obj[dogs]['Age'], obj[dogs]['Breed'], obj[dogs]['Weight']]
                dogsinf.append(dogsdata)
                
            result = dogsinf
            
        return result

    