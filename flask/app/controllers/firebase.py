#importa os metodos
from firebase import firebase
import json
#importa bibliotecas
import pandas as pd
import numpy as np

from app.models.functions import TransformationRequest, CurrentDate, CurrentHour, TransformationHour, TransformationDate, DogIdGenerator


#configuracao do firebase
    #realtime database
firebase =  firebase.FirebaseApplication("https://tcc2020-78c46.firebaseio.com/", None)

#'guarda' o usuário logado
logged = ""
check_login = "access denied"

#defini classes, metodos
class User():
    #dados comuns do usuario
    username = ""
    email = ""
    password = ""

    #metodo para checar login
    def CheckLogin(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global check_login
        return check_login

    #metodo para fazer logout
    def Logout(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global check_login
        check_login = "access denied"
        return check_login

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
            result = firebase.put('Users/'+self.username, 'User_Data', data)
        else:
            result = "Erro"
        return result
    
    #metodo para efetuar login
    def Login(self):
        #defini o 'validador'
        ticket = False
        #faz a consulta dos dados na base
        usernameTicket = firebase.get('/Users/'+self.username, 'User_Data/Username')
        passwordTicket = firebase.get('/Users/'+self.username, 'User_Data/Password')
        #defini as condições entre os dados digitados e os encontrados na base de dados
        if self.username == usernameTicket and self.username != None and self.password == passwordTicket and self.password != None:
            ticket = True
            #'puxa' as variaveis globais para serem usadas dentro do metodo
            global logged, check_login
            #defini o usuario que 'logou'
            logged = self.username
            check_login = "logged"
        elif self.username == None or passwordTicket == None:
            ticket = False
        else:
            ticket = False
        return ticket

    #metodo para pegar os dados do usuario
    def ReadUser(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #faz a consulta dos dados na base
        FRusername = firebase.get('/Users/'+logged, 'User_Data/Username')
        FRemail = firebase.get('/Users/'+logged, 'User_Data/Email')
        FRpassword = firebase.get('/Users/'+logged, 'User_Data/Password')
        #registra os dados lidos na base na lista
        user_data_received = [FRusername, FRemail, FRpassword]
        return user_data_received
    
    #metodo para editar usuario
    def EditUser(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #defini os dados a serem editados
        data = {
            'Username': logged,
            'Email': self.email,
            'Password': self.password
        }
        firebase.put('Users/'+logged, 'User_Data', data)
        result = "ok"
        return result
        
class Dog():
    #dados comuns ao cao
    dog_id=""
    dogname=""
    age=""
    weight=""
    breed=""

    #metodo para cadastrar cao
    def InsertDog(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #defini o 'resultado'
        result = "empty"
        #while para geracao e e teste de id
        while True:        
            #gera um id
            generate_dog_id = DogIdGenerator(self.dogname)
            #verifica se esse id ja foi cadastrado
            dogIdTicket = firebase.get('/Dogs/', generate_dog_id+'/Dog_Data/Dog_Id')
            #se o id for valido, defini como o id do cao
            if dogIdTicket == None:
                self.dog_id = generate_dog_id
                break
            
        #id que ficara no usuario
        dog_id_data = {
                'Dog_Id' : self.dog_id,
                'Dog_Name': self.dogname
        }
        #salva os dados do cao no usuario
        firebase.put('Users/'+logged+'/Dogs', self.dog_id, dog_id_data)
            
        #dados do cao
        data = {
            'Dog_Id' : self.dog_id,
            'Dog_Name': self.dogname,
            'Age': self.age,
            'Weight': self.weight,
            'Breed': self.breed
        }
        #salva os dados do cao
        firebase.put('Dogs/'+self.dog_id, 'Dog_Data', data)
            
        result = "Feito"
        return result

    #metodo para pegar dados de todos os caes
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
            #faz a consulta dos nomes na base de dados
            FRdogsnames = firebase.get('/Users/', logged+'/Dogs')
            #trata o dict com o metodo
            firebaseResult = TransformationRequest(FRdogsnames)
            #utiliza o metodo json
            obj = json.loads(firebaseResult)
            #cria lista que armazena os ids de cada cao
            dogssearch = []
            #for que pega o id de cada cao 
            for dogs in obj.values():
                dogssearch.append(dogs['Dog_Id'])

            #lista que salva os dados dos caes
            dogsinf = []

            #faz consulta dos dados dos caes
            for dog in dogssearch:
                FRdogsdata = firebase.get('Dogs/', dog+'/Dog_Data')
                #trata o dict com o metodo
                firebaseResults = TransformationRequest(FRdogsdata)
                #utiliza o metodo json
                dog_dict = json.loads(firebaseResults)
                #pega os dados [nome, idade, raca, peso, id] de cada cachorro e salva na lista
                dogsdata = [dog_dict['Dog_Name'], dog_dict['Age'], dog_dict['Breed'], dog_dict['Weight'], dog_dict['Dog_Id']]
                #quando os sensores estiverem prontos
                #dogsdata = [obj[dogs]['Dog_Name'], obj[dogs]['Age'], obj[dogs]['Breed'], obj[dogs]['Weight'], obj[dogs]['Status']]
                dogsinf.append(dogsdata)
            result = dogsinf
        return result

    #metodo para ler warnings do cao
    def ReadDogWarnings(self):
        #defini o valor inicial do resultado
        result = ''
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #faz a consulta dos dados na base
        
        ##codigo para teste
        FRdogsWarnings = firebase.get('/Dogs/', self.dog_id+'/Warnings/17_06_2020')
        
        #FRdogsWarnings = firebase.get('/Dogs/', self.dog_id+'/Warnings/'+CurrentDate())
        
        if FRdogsWarnings == None:
            result = None
        else:
            #trata o dict com o metodo
            firebaseResult = TransformationRequest(FRdogsWarnings)
            #utiliza o metodo json
            obj = json.loads(firebaseResult)
            print(obj)
            #lista que armazena os horarios de cada dicionario aninhado
            hours = []
            #for que pega os horarios de cada warning
            for hour in obj.values():
                HourKey = TransformationHour(hour['Hour'])
                hours.append(HourKey)
            #cria lista que armazena os dados de cada horario de um aviso
            hoursinf = []
            #for que pega os dados [data, frequencia, frequencia_status, hora] de cada hora e salva na lista, ignorando os avisos onde a frequencia esta normal
            for hour in hours:
                if obj[hour]['Frequency_Status'] == "Alterada":
                    hoursdata = [obj[hour]['Date'], obj[hour]['Frequency'], obj[hour]['Frequency_Status'], obj[hour]['Hour']]
                    hoursinf.append(hoursdata)
                else: 
                    pass
            result = hoursinf
            
        return result

    #metodo para ler determinados bpms registrados
    def ReadDogBPMHistory(self):
        #defini o valor inicial do resultado
        result = ''
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #faz a consulta dos dados na base
        FRBPMHistory = firebase.get('Dogs/', self.dog_id+'/BPM_History')
        if FRBPMHistory == None:
            result = None
        else:
            #trata o dict com o metodo
            firebaseResult = TransformationRequest(FRBPMHistory)
            #utiliza o metodo json
            obj = json.loads(firebaseResult)
            #lista que armazena os dias de cada dicionario aninhado
            dates = []
            #for que pega as datas de cada media
            for date in obj.values():
                DateKey = TransformationDate(date['Date'])
                dates.append(DateKey)
            #inverte a lista para que ela comece com o resultado mais recente
            dates.sort(reverse=True)
            #cria lista que armazena os dados de cada data de um media
            averagesinf = []
            #for que pega os dados [media_diaria, data] de cada data e salva na lista
            for date in dates:
                averagedata = [obj[date]['Date'], obj[date]['Daily_Average']]
                averagesinf.append(averagedata)
            result = averagesinf
        return result

    #metodo para adicionar cao
    def AddDog(self):
        #verifica o id informado corresponde a um cao cadastrado
        dogIDTicket = firebase.get('/Dogs/', self.dog_id+'/Dog_Data/Dog_Id')
        if dogIDTicket == None:
            result = None
        elif dogIDTicket == self.dog_id:
            #'puxa' a variavel global para ser usada dentro do metodo
            global logged
            #'pega' o nome do cao
            self.dogname = firebase.get('/Dogs/', self.dog_id+'/Dog_Data/Dog_Name')
            #defini os dados para o cadastro
            dog_id_data = {
                    'Dog_Id' : self.dog_id,
                    'Dog_Name': self.dogname
            }
            #adiciona o cao ao perfil do usuario logado
            firebase.put('Users/'+logged+'/Dogs', self.dog_id, dog_id_data)
            result = "ok"
        else:
            result = "erro"
        return result

    #metodo para desvincular cao da conta
    def UnlinkDog(self):
         #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #defini os dados a serem editados
        firebase.delete('Users/'+logged+'/Dogs', self.dog_id)
        result = "unlinked"
        return result

    #metodo para verificar se o cao ainda esta cadastrado
    def DogVerify(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #faz a consulta dos nomes na base de dados
        FRdogsnames = firebase.get('/Users/', logged+'/Dogs')
        if FRdogsnames == None:
            pass
        else:
            #trata o dict com o metodo
            firebaseResult = TransformationRequest(FRdogsnames)
            #utiliza o metodo json
            obj = json.loads(firebaseResult)
            #cria lista que armazena os ids de cada cao
            dogssearch = []
            #for que pega o id de cada cao 
            for dogs in obj.values():
                dogssearch.append(dogs['Dog_Id'])
            
            #faz consulta dos caes
            for dog in dogssearch:
                #pesquisa se os caes que o usuario tem em seu perfil ainda existem
                FRdogsdata = firebase.get('Dogs/', dog)
                if FRdogsdata == None:
                    #se nao existem, os caes sao excluidos do perfil
                    self.dog_id = dog
                    firebase.delete('Users/'+logged+'/Dogs', self.dog_id)
                else:
                    pass

        result = "ok"
        return result


        

    #metodo para ler dados do cao
    def SearchDog(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #pesquisa se existe o id do cao informado
        dognameTicket = firebase.get('/Dogs/', self.dog_id+'/Dog_Data')
        if dognameTicket == None:
            result = None
            
        elif dognameTicket != None:
            #trata o dict com o metodo
            firebaseResult = TransformationRequest(dognameTicket)
            #utiliza o metodo json
            obj = json.loads(firebaseResult)
            #variavel que armazena, em lista, os dados [nome, idade, raca, peso] do cao
            dogsdata = [obj['Dog_Name'], obj['Age'], obj['Breed'], obj['Weight'], obj['Dog_Id']]
            #quando os sensores estiverem prontos
            #dogsdata = [obj[dogs]['Dog_Name'], obj[dogs]['Age'], obj[dogs]['Breed'], obj[dogs]['Weight'], obj[dogs]['Status'], obj['Dog_Id']]
            
            result = dogsdata
            
        return result

    #metodo para pegar o nome do cachorro
    def GetDogName(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #pesquisa o nome do cao
        dogname = firebase.get('Dogs/', self.dog_id+'/Dog_Data/Dog_Name')
        
        return dogname
        
    #metodo para editar dog
    def EditDog(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #defini os dados a serem editados
        data = {
            'Dog_Id': self.dog_id,
            'Dog_Name': self.dogname,
            'Age': self.age,
            'Weight': self.weight,
            'Breed': self.breed
        }
        firebase.put('Dogs/'+self.dog_id, 'Dog_Data', data)
        result = "ok"
        return result

    #metodo para editar dog
    def DeleteDog(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #defini os dados a serem editados
        firebase.delete('Users/'+logged+'/Dogs', self.dog_id)
        firebase.delete('Dogs/', self.dog_id)
        result = "deleted"
        return result

#classe para os dados brutos
class RawData():

    #variáveis para receber os valores do JSON
    raw_data = ""
    sensor = ""
    petID = ""
    time = ""
    girX = ""
    girY = ""
    girZ = ""
    accX = ""
    accY = ""
    accZ = ""
    HR = ""

    #método que recebe o JSON enviado para a URL 
    def receiveJSON(self, postData):
      
        self.postData = postData

        #extrai os valores recebidos
        self.sensor = self.postData['sensor']
        self.petID = self.postData['petID']
        #self.time = self.postData['time']
        self.time = CurrentHour()
        self.girX = self.postData['girX']
        self.girY = self.postData['girY']
        self.girZ = self.postData['girZ']
        self.accX = self.postData['accX']
        self.accY = self.postData['accY']
        self.accZ = self.postData['accZ']
        self.HR = self.postData['HR']
    
    #antes de mandar para o firebase, verifica se tem todos os valores
        self.raw_data = {
            'Sensor': self.sensor,
            'petID': self.petID,
            'time': self.time,
            'girX': self.girX,
            'girY': self.girY,
            'girZ': self.girZ,
            'accX': self.accX,
            'accY': self.accY,
            'accZ': self.accZ 
        }

        return True

    
    #método para salvar dados no firebase  
    def saveRawData(self):
        #adiciona os dados brutos recebidos do sensor ao servidor
        firebase.put('RawDog/'+CurrentDate(), TransformationHour(self.time), self.raw_data)

