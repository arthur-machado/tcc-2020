#importa os metodos
from firebase import firebase
import json
#importa bibliotecas
#import pandas as pd
import numpy as np

from app.models.functions import TransformationRequest, CurrentDate, CurrentHour, TransformationHour, TransformationDate, DogIdGenerator


#configuracao do firebase
    #realtime database
firebase =  firebase.FirebaseApplication("https://tcc2020-78c46.firebaseio.com/", None)

#'guarda' o usuário logado
logged = ""
check_login = "access denied"

#'guarda' os ids das dicionarios de dados brutos recebidos da placa arduino
data_id_block = []
#'guarda' a dicionarios 'temporaria' de dados brutos recebidos da placa arduino
block = []
#'guarda' o numero de amostras (em segundos)
sample_window = 10

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
    
    #junta o dicionario
        self.raw_data = {
            'Sensor': self.sensor,
            'petID': self.petID,
            'time': self.time,
            'girX': self.girX,
            'girY': self.girY,
            'girZ': self.girZ,
            'accX': self.accX,
            'accY': self.accY,
            'accZ': self.accZ, 
            'HR': self.HR
        }

        
        return "The package has been assembled!"

    #metodo para salvar dados no firebase  
    def saveRawData(self):
        #'chama' a variavel que guarda os ids da dicionarios de dados brutos
        global block
        global data_id_block
        global sample_window
        
        ##monta a chave do json
        ##Key = TransformationHour(self.time)
        ##monta os dicionarios
        ##obj = {Key:self.raw_data}

        #salva os dados brutos no firebase
        firebase.put('RawData/'+CurrentDate(), TransformationHour(self.time), self.raw_data)

        #monta os blocos de dicionarios
        if len(block) < sample_window:
            block.append(self.raw_data)
        else:
            #copia a dicionarios de ids temporarios para a dicionarios a ser enviada para analise
            data_id_block.extend(block)
            #print(f"\n\n\nAQUI >>> {data_id_block}\n\n\n")
            ReadRawData.Read()
            block.clear()
            block.append(self.raw_data)


class ReadRawData():

    ##1 - Capturar dados brutos do sensor (Arduino) [FEITO]
    ##2 - Pré-processamento | filtro (arc Python (ARDUINO POR ENQUANTO)) [FEITO]
    ##3 - Segmentação dos dados | time window - 10s (fixa), Frequência 50Hz (arc Python) [FEITO]
    ##4 - Feature extraction (estatísticas) (arc Python) [FEITO]
    ##5 - Classificação da atividade (Cadeias ocultas de Markov e Random Forest)

    #===============================================================#
    #       LEITURA E SEPARACAO DE DADOS VINDOS DO FIREBASE         #
    #===============================================================#

    def Read():
        print(f"\n\n\nFUNCAO READ INICIADA!\n\n\n")  
        #importa a variavel global
        global data_id_block

        #cria lista que guarda os dicionarios
        obj = []

        #copia o dicionario 'data_id_block' para 'obj'
        obj.extend(data_id_block)
        #'reseta' o dicionario 'data_id_block'
        data_id_block.clear()
        
        #print(f"\n\n\nAQUI >>> {obj}\n\n\n")    
        
        #cria lista que armazena cada dado do sensor ['hora', 'x', 'y', 'z']
        linesValues = []
        #for que pega os dados do sensor e armazena na lista
        for values in obj:
            sensor_data = [values['time'], values['girX'], values['girY'], values['girZ'], values['accX'], values['accY'], values['accZ']]
            linesValues.append(sensor_data)
        
        #print(f"\n\n\nLINHAS >>> {linesValues}\n\n\n")
        #'reseta' a lista 'obj'
        obj.clear()
        #print(f"\n\n\nLISTA OBJ RESETADA\n\n\n")  

        #print(f"\n\n\nAQUI >>> {linesValues}\n\n\n")
        
        #cria as listas e valores
        position = 0
        seconds = []

        #contadores
        cont = 1
        vezes = 0
        position = 0
        hours_axes_cont = 0

        hours = []
        #lista que armazena as horas a cada 10 segundos
        hoursGroups = []
        group = []
        #lista que armazena os segundos a cada 10 segundos
        secondsGroups=[]
        #lista que armanza os eixos a cada 10 segundos
        ##x 
        x_AxisGir = []
        x_AxisGroupsGir = []

        x_AxisAcc = []
        x_AxisGroupsAcc = []

        ##y 
        y_AxisGir = []
        y_AxisGroupsGir = []

        y_AxisAcc = []
        y_AxisGroupsAcc = []
        ##z 
        z_AxisGir = []
        z_AxisGroupsGir = []

        z_AxisAcc = []
        z_AxisGroupsAcc = []

        lastSecond = '0'

        #print(f"\n\n\nINICIO DO FILTRO\n\n\n")  
        #funcao para 'pegar' os segundos
        def getSeconds(time):  
            #separa o tempo em ['hora', 'minuto', 'segundos e milesimos']
            splitTime = time.split(":")
            #pega a posicao 2 da lista splitTime, ou seja, os segundos e milesimos e os separa
            #algo como: ['segundos', 'milesimos']
            getSeconds = splitTime[2].split(".")

            second = getSeconds[0]

            return second

        #print(linesValues)
        


        #pega e guarda em um lista os segundos de cada linha
        for value in range(len(linesValues)):
            hour = linesValues[value][0]
            second = getSeconds(hour)
            seconds.append(second)
            #print(f"Segundos: {seconds}")


        #print(f"\n\n\nSEGUNDOS >>> {seconds}\n\n\n")
        #pega os grupos de segundos, horas (H:M:S.m), valores dos eixos X, Y, Z e guarda em uma lista 
        for value in seconds:
            #o contador soma 1 a cada segundo registrado, ou seja, a lista ['05', '05', '06'] teria dois segundos armazenados. embora tenha 3 registros armazenados, as posicoes 0 e 1 correspondem ao mesmo segundo.
            #com isso, a cada 10 segundos reconhecidos, ele registra esses como um grupo na lista de grupos
            #o mesmo se aplica as horas e valores de eixos reconhecidos
            
            #se for a primeira vez que o laco 'roda', o ultimo segundo registrado e igual ao valor inicial
            if vezes == 0:
                lastSecond = value
            #se nao for a primeira vez que o laco 'roda', o ultimo segundo registrado e igual ao valor anterior da lista
            else:
                lastSecond = group[vezes-1]
                #print(f"LAST SECOND = {lastSecond}")

            #se o valor da lista for o mesmo, ou seja, o ultimo reconhecido, ele somente adiciona na lista de grupo
            if value == lastSecond:
                #print("\n\n\nENTREI 1\n\n\n")
                group.append(value)
                hours.append(linesValues[hours_axes_cont][0])
                x_AxisGir.append(float(linesValues[hours_axes_cont][1]))
                y_AxisGir.append(float(linesValues[hours_axes_cont][2]))
                z_AxisGir.append(float(linesValues[hours_axes_cont][3]))
                
                x_AxisAcc.append(float(linesValues[hours_axes_cont][4]))
                y_AxisAcc.append(float(linesValues[hours_axes_cont][5]))
                z_AxisAcc.append(float(linesValues[hours_axes_cont][6]))
                
            #se o valor da lista for diferente do ultimo reconhecido, ele adiciona na lista de grupo e soma mais um ao numero de segundos reconhecidos
            elif value != lastSecond:
                #print("\n\n\nENTREI 2\n\n\n"
                group.append(value)
                hours.append(linesValues[hours_axes_cont][0])
                x_AxisGir.append(float(linesValues[hours_axes_cont][1]))
                y_AxisGir.append(float(linesValues[hours_axes_cont][2]))
                z_AxisGir.append(float(linesValues[hours_axes_cont][3]))
                
                x_AxisAcc.append(float(linesValues[hours_axes_cont][4]))
                y_AxisAcc.append(float(linesValues[hours_axes_cont][5]))
                z_AxisAcc.append(float(linesValues[hours_axes_cont][6]))
                
                cont += 1

            #print(f"\n\n\nCONTADOR >>> {cont}\n\n\n")

            #DEBUG = ESSE TESTE ESTAVA NO COMECO ANTES, mas agora a janela so possui 10 elementos
            if cont == 10:
                #print(group)
                #registra na lista
                secondsGroups.insert(position, group)
                hoursGroups.insert(position, hours)
                x_AxisGroupsGir.insert(position, x_AxisGir)
                y_AxisGroupsGir.insert(position, y_AxisGir)
                z_AxisGroupsGir.insert(position, z_AxisGir)
                
                x_AxisGroupsAcc.insert(position, x_AxisAcc)
                y_AxisGroupsAcc.insert(position, y_AxisAcc)
                z_AxisGroupsAcc.insert(position, z_AxisAcc)
                
                #reinicia a lista de segundos reconhecidos
                group = []
                #reinicia a lista de horas reconhecidas
                hours = []
                #reinicia os listas de eixos conhecidos
                x_AxisGir = []
                y_AxisGir = []
                z_AxisGir = []
                
                x_AxisAcc = []
                y_AxisAcc = []
                z_AxisAcc = [] 
                
                #a variavel 'posicao' registra a posicao na qual o grupo de 10 segundos deve ser adicionado a lista de grupos. apos adicionar, soma-se um a posicao atual
                position += 1
                #a variavel 'vezes' registra o numero de vezes que o laco ja foi executado
                vezes -= vezes
                #a variavel 'cont' regista os segundos reconhecidos
                cont -= cont - 1

            vezes += 1
            hours_axes_cont += 1

        #print(f"\n\n\nFIM DO FILTRO\n\n\n")  
        print(f"\n\n\nVALORES DE X GIR>>> {x_AxisGroupsGir}")  
        print(f"VALORES DE Y GIR>>> {y_AxisGroupsGir}")
        print(f"VALORES DE Z GIR>>> {z_AxisGroupsGir} \n\n\n")  
        
        print(f"\n\n\nVALORES DE X ACC>>> {x_AxisGroupsAcc}")  
        print(f"VALORES DE Y ACC>>> {y_AxisGroupsAcc}")
        print(f"VALORES DE Z ACC>>> {z_AxisGroupsAcc} \n\n\n")
        
        
        #print(f"O valor é {value}, o ultimo segundo é {lastSecond}, o laço rodou {vezes} vezes e {cont} segundos já foram reconhecidos nesse grupo\n")

        #print(f"\n\n\nCALCULOS INICIADOS!\n\n\n")  
        #===============================================================#
        #                         CALCULOS                              #
        #===============================================================#

        '''
        #desvio absoluto medio
        listDAMX = []
        DAMX = []
        listDAMY = []
        DAMY = []
        listDAMZ = []
        DAMZ = []

        #media aritmetica
        listMeArX = []
        MeArX = []
        listMeArY = []
        MeArY = []
        listMeArZ = []
        MeArZ = []

        #variancia (amostral)
        listVaCX = []
        VaCX = []
        listVaCY = []
        VaCY = []
        listVaCZ = []
        VaCZ = []

        #mediana 
        listmedianX = []
        medianX = []
        listmedianY = []
        medianY = []
        listmedianZ = []
        medianZ = []

        #desvio padrao (da populacao)
        listdespX = []
        despX = []
        listdespY = []
        despY = []
        listdespZ = []
        despZ = []
        '''

        #media quadratica
        listRMSXGir = []
        RMSXGir = []
        #
        listRMSYGir = []
        RMSYGir = []
        #
        listRMSZGir = []
        RMSZGir = []
        ###
        listRMSXAcc = []
        RMSXAcc = []
        #
        listRMSYAcc = []
        RMSYAcc = []
        #
        listRMSZAcc = []
        RMSZAcc = []

        #calcula a media quadratica da lista
        def setRootMeanSquare(valuess):
            power =  []
            for value in valuess:
                #pega o valor, eleva a segunda potencia e salva na lista potencia
                power.append(value**2)
            #soma a lista que tem os valores elevados a segunda potencia e divide pelo numero de valores
            sum_division = sum(power) / len(power)
            #calcula a raiz quadrada nao negativa da 'soma divida'. essa raiz e a media quadratica
            square_root = np.sqrt(sum_division)
            return square_root


        #print(f"\n\n\nGRUPOS DE X {x_AxisGroups}\n\n\n")
        #calculos do eixo X
        for values in x_AxisGroupsGir:
            #'cria uma lista' no padrao do pandas
            #series = pd.Series(values)
            
            #========================================================#
            #calcula e salva a media quadratica
            RMSGir = setRootMeanSquare(values)
            listRMSXGir.append(RMSGir)
            RMSXGir.append(listRMSXGir)
            #========================================================#
            #reseta as listas
           
            listRMSXGir = []

        #print(len(x_AxisGroups))
        #print(medianX)
        #print(hoursGroups)

        #print(f"\n\n\nX CALCULADO\n\n\n")
        #calculos do eixo Y
        for values in y_AxisGroupsGir:
            #'cria uma lista' no padrao do pandas
            #series = pd.Series(values)
            #========================================================#
            #calcula e salva a media quadratica
            RMSGir = setRootMeanSquare(values)
            listRMSYGir.append(RMSGir)
            RMSYGir.append(listRMSYGir)
            
            #========================================================#
            #reseta as listas
        
            listRMSYGir = []

        #calculos do eixo Z
        for values in z_AxisGroupsGir:
            #'cria uma lista' no padrao do pandas
            #series = pd.Series(values)
           
            #========================================================#
            #calcula e salva a media quadratica
            RMSGir = setRootMeanSquare(values)
            listRMSZGir.append(RMSGir)
            RMSZGir.append(listRMSZGir)
            #========================================================#
            #reseta as listas
            
            listRMSZGir = []


        ############# ACC #################

        for values in x_AxisGroupsAcc:
            #'cria uma lista' no padrao do pandas
            #series = pd.Series(values)
            
            #========================================================#
            #calcula e salva a media quadratica
            RMSAcc = setRootMeanSquare(values)
            listRMSXAcc.append(RMSAcc)
            RMSXAcc.append(listRMSXAcc)
            #========================================================#
            #reseta as listas
           
            listRMSXAcc = []

        #calculos do eixo Y
        for values in y_AxisGroupsAcc:
            #'cria uma lista' no padrao do pandas
            #series = pd.Series(values)
            #========================================================#
            #calcula e salva a media quadratica 
            RMSAcc = setRootMeanSquare(values)
            listRMSYAcc.append(RMSAcc)
            RMSYAcc.append(listRMSYAcc)
            #========================================================#
            #reseta as listas
        
            listRMSYAcc = []

        #calculos do eixo Z
        for values in z_AxisGroupsAcc:
            #'cria uma lista' no padrao do pandas
            #series = pd.Series(values)
           
            #========================================================#
            #calcula e salva a media quadratica
            RMSAcc = setRootMeanSquare(values)
            listRMSZAcc.append(RMSAcc)
            RMSZAcc.append(listRMSZAcc)
            #========================================================#
            #reseta as listas
            
            listRMSZAcc = []

        #print(f"\n\n\nZ CALCULADO\n")
        #print(f"\n\n\nAQUI >>> {RMSX}\n\n\n")
        #===============================================================#
        #                 ENVIA OS DADOS PARA O FIREBASE                #
        #===============================================================#

        print(f"\n\n\nINICIO DO ENVIO\n\n\n")  
        RMS_data = {
            'girX': RMSXGir[0],
            'girY': RMSYGir[0],
            'girZ': RMSZGir[0],
            'accX': RMSXAcc[0],
            'accY': RMSYAcc[0],
            'accZ': RMSZAcc[0]
        }
        #print(f"ENVIANDO...")
        firebase.put('FeExtDog/'+CurrentDate(), TransformationHour(CurrentHour()), RMS_data)

        return "ok"  
