#importa os metodos
from firebase import firebase
import json

from app.models.functions import TransformationRequest, CurrentDate, TransformationHour, TransformationDate, DogIdGenerator


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
        #pesquisa se já existe um cao com esse nome cadastrado
        dognameTicket = firebase.get('/Users/', logged+'/Dogs/'+self.dogname+'/Dog_Name')
        if dognameTicket == self.dogname:
            result = "Cão já cadastrado"
        elif dognameTicket == None:
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
            firebase.put('Users/'+logged+'/Dogs', self.dogname, dog_id_data)
            
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
        else:
            result = "Erro"
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
            #lista que armazena os nomes de cada dicionario aninhado
            dogs_names = []
            #for que pega os nomes dos caes cadastrados no usuario
            for dogs in obj.values():
                dogs_names.append(dogs['Dog_Name'])
            #cria lista que armazena os ids de cada cao
            dogssearch = []
            #for que pega o id de cada cao 
            for dogs in dogs_names:
                dogsearch = obj[dogs]['Dog_Id']
                dogssearch.append(dogsearch)

            #lista que salva os dados dos caes
            dogsinf = []

            #faz consulta dos dados dos caes
            for dog in dogssearch:
                FRdogsdata = firebase.get('Dogs/', dog+'/Dog_Data')
                #trata o dict com o metodo
                firebaseResults = TransformationRequest(FRdogsdata)
                #utiliza o metodo json
                dog_dict = json.loads(firebaseResults)
                print(dog_dict)
                #pega os dados [nome, idade, raca, peso] de cada cachorro e salva na lista
                dogsdata = [dog_dict['Dog_Name'], dog_dict['Age'], dog_dict['Breed'], dog_dict['Weight']]
                #quando os sensores estiverem prontos
                #dogsdata = [obj[dogs]['Dog_Name'], obj[dogs]['Age'], obj[dogs]['Breed'], obj[dogs]['Weight'], obj[dogs]['Status']]
                dogsinf.append(dogsdata)
                print("==============================")
                print(dogsdata)
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
        ##FRdogsWarnings = firebase.get('/Users/', logged+'/Dogs/'+self.dogname+'/Warnings/12_05_2020')
        
        FRdogsWarnings = firebase.get('/Users/', logged+'/Dogs/'+self.dogname+'/Warnings'+CurrentDate())
        if FRdogsWarnings == None:
            result = None
        else:
            #trata o dict com o metodo
            firebaseResult = TransformationRequest(FRdogsWarnings)
            #utiliza o metodo json
            obj = json.loads(firebaseResult)
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
        FRBPMHistory = firebase.get('/Users/', logged+'/Dogs/'+self.dogname+'/BPM_History')
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

    #metodo para ler dados do cao
    def SearchDog(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #pesquisa se existe o id do cao informado
        dognameTicket = firebase.get('/Users/', logged+'/Dogs/'+self.dogname)
        if dognameTicket == None:
            result = None
            #faz a consulta dos dados na base
            FRdogsid = firebase.get('/Users/', logged+'/Dogs/'+self.dogname)            
            #trata o dict com o metodo
            firebaseResult = TransformationRequest(FRdogsid)
            #utiliza o metodo json
            obj = json.loads(firebaseResult)
            #variavel que armazena, em lista, os dados [nome, idade, raca, peso] do cao
            dogsdata = [obj['Dog_Name'], obj['Age'], obj['Breed'], obj['Weight']]
            #quando os sensores estiverem prontos
            #dogsdata = [obj[dogs]['Dog_Name'], obj[dogs]['Age'], obj[dogs]['Breed'], obj[dogs]['Weight'], obj[dogs]['Status']]
            result = dogsdata

        elif dognameTicket != None:
            #faz a consulta dos dados na base
            FRdogsid = firebase.get('/Users/', logged+'/Dogs/'+self.dogname)            
            #trata o dict com o metodo
            firebaseResult = TransformationRequest(FRdogsid)
            #utiliza o metodo json
            obj = json.loads(firebaseResult)
            #variavel que armazena, em lista, os dados [nome, idade, raca, peso] do cao
            dogsdata = [obj['Dog_Name'], obj['Age'], obj['Breed'], obj['Weight']]
            #quando os sensores estiverem prontos
            #dogsdata = [obj[dogs]['Dog_Name'], obj[dogs]['Age'], obj[dogs]['Breed'], obj[dogs]['Weight'], obj[dogs]['Status']]
            
            result = dogsdata
            
        return result

    #metodo para editar dog
    def EditDog(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #defini os dados a serem editados
        data = {
            'Dog_Name': self.dogname,
            'Age': self.age,
            'Weight': self.weight,
            'Breed': self.breed
        }
        firebase.put('Users/'+logged+'/Dogs', self.dogname, data)
        result = "ok"
        return result

    #metodo para editar dog
    def DeleteDog(self):
        #'puxa' a variavel global para ser usada dentro do metodo
        global logged
        #defini os dados a serem editados
        firebase.delete('Users/'+logged+'/Dogs', self.dogname)
        result = "deleted"
        return result



    