#importa os metodos
from firebase import firebase
import json
#importa bibliotecas
#import pandas as pd
#import numpy as np

from app.models.functions import TransformationRequest, CurrentDate, CurrentHour, TransformationHour, TransformationDate, DogIdGenerator


#configuracao do firebase
    #realtime database
firebase =  firebase.FirebaseApplication("https://tcc2020-78c46.firebaseio.com/", None)

#'guarda' o usuário logado
logged = ""
check_login = "access denied"

#'guarda' os ids das listas de dados brutos recebidos da placa arduino
data_id_block = []
#'guarda' a lista 'temporaria' de dados brutos recebidos da placa arduino
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
    
    #antes de mandar para o firebase, verifica se o dicionario tem todos os valores
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
        #'chama' a variavel que guarda os ids da lista de dados brutos
        global block
        global data_id_block
        global sample_window
        
        #monta a chave do json
        Key = TransformationHour(self.time)
        
        #adiciona os dados brutos recebidos do sensor ao servidor
        firebase.put('RawDog/'+CurrentDate(), Key, self.raw_data)

        #monta os blocos de listas de dados brutos
        if len(block) < sample_window:
            block.append(Key)
        else:
            #copia a lista de ids temporarios para a lista a ser enviada para analise
            data_id_block.extend(block)
            ReadRawData.Read()
            block.clear()
            block.append(Key)

class ReadRawData():
    ##1 - Capturar dados brutos do sensor (Arduino) [FEITO]
    ##2 - Pré-processamento | filtro (arc Python (ARDUINO POR ENQUANTO)) [FEITO]
    ##3 - Segmentação dos dados | time window - 10s (fixa), Frequência 50Hz (arc Python) [FEITO]
    ##4 - Feature extraction (estatísticas) (arc Python) [FEITO]
    ##5 - Classificação da atividade (Cadeias ocultas de Markov e Random Forest)

    #===============================================================#
    #       LEITURA E SEPARACAO DE DADOS VINDOS DO FIREBASE         #
    #===============================================================#
    
    #defini as variaveis a receberem os valores
    sensor = ""
    petID = ""
    time = ""
    girX = ""
    girY = ""
    girZ = ""
    accX = ""
    accY = ""
    accZ = ""

    def Read():
        #importas as variaveis globais
        global data_id_block
        print(data_id_block)
        #cria lista que armazena o tempo de cada dicionario
        raw_data_hour = []


        #PROBLEMA DA MEIA NOITE >> pesquisa de janelas com dias diferentes

        #pega os dados do firebase
        for data in data_id_block:
            SensorRawData = firebase.get('RawDog/', CurrentDate()+'/'+data)
            ##codigo para teste
            #SensorRawData = firebase.get('RawData2/', "09_08_2020")

            #trata o dict com o metodo
            firebaseResult = TransformationRequest(SensorRawData)
            #utiliza o metodo json
            obj = json.loads(firebaseResult)
            
            #pega somente o tempo de cada dicionario
            raw_data_hour.append(obj['time'])

            #print(f"\n\n\n\nAQUIIIIIIIIII \n {obj} \n\n\n\n")
            data_id_block.clear()
        print(raw_data_hour)
        '''    
        #cria lista que armazena cada dado do sensor ['hora', 'x', 'y', 'z']
        linesValues = []
        #for que pega os dados do sensor e armazena na lista
        ##ESSE REPLACE É SÓ PRO TESTE
        for values in raw_data_hour:
            sensor_data = [obj[values]['time'].replace("_", ':'), obj[values]['girX'], obj[values]['girY'], obj[values]['girZ']]
            linesValues.append(sensor_data)

        #print(linesValues)
        
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
        x_Axis = []
        x_AxisGroups = []
        ##y
        y_Axis = []
        y_AxisGroups = []
        ##z
        z_Axis = []
        z_AxisGroups = []

        lastSecond = '0'


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

        #pega os grupos de segundos, horas (H:M:S.m), valores dos eixos X, Y, Z e guarda em uma lista 
        for value in seconds:
            #o contador soma 1 a cada segundo registrado, ou seja, a lista ['05', '05', '06'] teria dois segundos armazenados. embora tenha 3 registros armazenados, as posicoes 0 e 1 correspondem ao mesmo segundo.
            #com isso, a cada 10 segundos reconhecidos, ele registra esses como um grupo na lista de grupos
            #o mesmo se aplica as horas e valores de eixos reconhecidos
            if cont == 10:
                #print(group)
                #registra na lista
                secondsGroups.insert(position, group)
                hoursGroups.insert(position, hours)
                x_AxisGroups.insert(position, x_Axis)
                y_AxisGroups.insert(position, y_Axis)
                z_AxisGroups.insert(position, z_Axis)
                #reinicia a lista de segundos reconhecidos
                group = []
                #reinicia a lista de horas reconhecidas
                hours = []
                #reinicia os listas de eixos conhecidos
                x_Axis = []
                y_Axis = []
                z_Axis = []
                #a variavel 'posicao' registra a posicao na qual o grupo de 10 segundos deve ser adicionado a lista de grupos. apos adicionar, soma-se um a posicao atual
                position = position + 1
                #a variavel 'vezes' registra o numero de vezes que o laco ja foi executado
                vezes = 0
                #a variavel 'cont' regista os segundos reconhecidos
                cont = 1

            #se for a primeira vez que o laco 'roda', o ultimo segundo registrado e igual ao valor inicial
            if vezes == 0:
                lastSecond = value
            #se nao for a primeira vez que o laco 'roda', o ultimo segundo registrado e igual ao valor anterior da lista
            else:
                lastSecond = group[vezes-1]
                #print(f"LAST SECOND = {lastSecond}")

            #se o valor da lista for o mesmo, ou seja, o ultimo reconhecido, ele somente adiciona na lista de grupo
            if value == lastSecond:
                group.append(value)
                hours.append(linesValues[hours_axes_cont][0])
                x_Axis.append(float(linesValues[hours_axes_cont][1]))
                y_Axis.append(float(linesValues[hours_axes_cont][2]))
                z_Axis.append(float(linesValues[hours_axes_cont][3]))

            #se o valor da lista for diferente do ultimo reconhecido, ele adiciona na lista de grupo e soma mais um ao numero de segundos reconhecidos
            elif value != lastSecond:
                group.append(value)
                hours.append(linesValues[hours_axes_cont][0])
                x_Axis.append(float(linesValues[hours_axes_cont][1]))
                y_Axis.append(float(linesValues[hours_axes_cont][2]))
                z_Axis.append(float(linesValues[hours_axes_cont][3]))
                cont += 1

            vezes = vezes + 1
            hours_axes_cont = hours_axes_cont + 1

            #print(f"O valor é {value}, o ultimo segundo é {lastSecond}, o laço rodou {vezes} vezes e {cont} segundos já foram reconhecidos nesse grupo\n")

        #===============================================================#
        #                         CALCULOS                              #
        #===============================================================#

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

        #media quadratica
        listRMSX = []
        RMSX = []
        listRMSY = []
        RMSY = []
        listRMSZ = []
        RMSZ = []

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

        #calculos do eixo X
        for values in x_AxisGroups:
            #'cria uma lista' no padrao do pandas
            series = pd.Series(values)
            
            #calcula o desvio absoluto medio
            DAM = series.mad()
            listDAMX.append(DAM)
            DAMX.append(listDAMX)
            #========================================================#
            #calcula e salva a media aritmetica
            MeAr = np.mean(values)
            listMeArX.append(MeAr)
            MeArX.append(listMeArX)
            #========================================================#
            #variancia (amostral)
            VaC = np.var(values)
            listVaCX.append(VaC)
            VaCX.append(listVaCX)
            #========================================================#
            #calcula e salva a mediana
            mediana = np.median(values)
            listmedianX.append(mediana)
            medianX.append(listmedianX)
            #========================================================#
            #calcula e salva o desvio padrao
            desvio_padrao = np.std(values)
            listdespX.append(desvio_padrao)
            despX.append(listdespX)
            #========================================================#
            #calcula e salva a media quadratica
            RMS = setRootMeanSquare(values)
            listRMSX.append(RMS)
            RMSX.append(listRMSX)
            #========================================================#
            #reseta as listas
            listDAMX = []
            listMeArX = []
            listVaCX = []
            listmedianX = []
            listdespX = []
            listRMSX = []

        #print(len(x_AxisGroups))
        #print(medianX)
        #print(hoursGroups)

        #calculos do eixo Y
        for values in y_AxisGroups:
            #'cria uma lista' no padrao do pandas
            series = pd.Series(values)
            
            #calcula o desvio absoluto medio
            DAM = series.mad()
            listDAMY.append(DAM)
            DAMY.append(listDAMY)
            #========================================================#
            #calcula e salva a media aritmetica
            MeAr = np.mean(values)
            listMeArY.append(MeAr)
            MeArY.append(listMeArY)
            #========================================================#
            #variancia (amostral)
            VaC = np.var(values)
            listVaCY.append(VaC)
            VaCY.append(listVaCY)
            #========================================================#
            #calcula e salva a mediana
            mediana = np.median(values)
            listmedianY.append(mediana)
            medianY.append(listmedianY)
            #========================================================#
            #calcula e salva o desvio padrao
            desvio_padrao = np.std(values)
            listdespY.append(desvio_padrao)
            despY.append(listdespY)
            #========================================================#
            #calcula e salva a media quadratica
            RMS = setRootMeanSquare(values)
            listRMSY.append(RMS)
            RMSY.append(listRMSY)
            #========================================================#
            #reseta as listas
            listDAMY = []
            listMeArY = []
            listVaCY = []
            listmedianY = []
            listdespY= []
            listRMSY = []


        #calculos do eixo Z
        for values in z_AxisGroups:
            #'cria uma lista' no padrao do pandas
            series = pd.Series(values)
            
            #calcula o desvio absoluto medio
            DAM = series.mad()
            listDAMZ.append(DAM)
            DAMZ.append(listDAMZ)
            #========================================================#
            #calcula e salva a media aritmetica
            MeAr = np.mean(values)
            listMeArZ.append(MeAr)
            MeArZ.append(listMeArZ)
            #========================================================#
            #variancia (amostral)
            VaC = np.var(values)
            listVaCZ.append(VaC)
            VaCZ.append(listVaCZ)
            #========================================================#
            #calcula e salva a mediana
            mediana = np.median(values)
            listmedianZ.append(mediana)
            medianZ.append(listmedianZ)
            #========================================================#
            #calcula e salva o desvio padrao
            desvio_padrao = np.std(values)
            listdespZ.append(desvio_padrao)
            despZ.append(listdespZ)
            #========================================================#
            #calcula e salva a media quadratica
            RMS = setRootMeanSquare(values)
            listRMSZ.append(RMS)
            RMSZ.append(listRMSZ)
            #========================================================#
            #reseta as listas
            listDAMZ = []
            listMeArZ = []
            listVaCZ = []
            listmedianZ = []
            listdespZ = []
            listRMSZ = []

        #===============================================================#
        #                   PRINTA DADOS (POR AGORA)                    #
        #===============================================================#
        #contador para saber o numero de grupos
        count = 1

        for value in range (len(medianX)):
            print("==-==-==-==-==-==-==-==-==-==-==")
            print(f" BEGIN OF THE {count} GROUP")
            print("==-==-==-==-==-==-==-==-==-==-==")
            print("MEDIA ARITMETICA")
            print(MeArX[value])
            print(MeArY[value]) 
            print(MeArZ[value]) 
            print("==-==-==-==-==-==-==-==-==-==-==")
            print("VARIANCIA")
            print(VaCX[value])
            print(VaCY[value])
            print(VaCZ[value])
            print("==-==-==-==-==-==-==-==-==-==-==")
            print("DESVIO PADRAO") 
            print(despX[value]) 
            print(despY[value]) 
            print(despZ[value])
            print("==-==-==-==-==-==-==-==-==-==-==")
            print("MEDIANA") 
            print(medianX[value]) 
            print(medianY[value]) 
            print(medianZ[value]) 
            print("==-==-==-==-==-==-==-==-==-==-==")
            print("DESVIO ABSOLUTO") 
            print(DAMX[value]) 
            print(DAMY[value]) 
            print(DAMZ[value]) 
            print("==-==-==-==-==-==-==-==-==-==-==")
            print("MEDIA QUADRATICA") 
            print(RMSX[value]) 
            print(RMSY[value]) 
            print(RMSZ[value])
            print("==-==-==-==-==-==-==-==-==-==-==")
            print(f" END OF THE {count} GROUP ")
            print("==-==-==-==-==-==-==-==-==-==-==")
            count += 1
        return SensorRawData


        with open(ficheiro_de_gravacao, 'w') as ficheiro:
            #'cria' a escrita no arquivo
            writer = csv.writer(ficheiro)
            try:
                #defini a linha de 'nomes' da tabela
                writer.writerow( ('Media Aritmetica de X', 'Media Aritmetica de Y', 'Media Aritmetica de Z', 'Variancia amostral de X', 'Variancia amostral de Y', 'Variancia amostral de Z', 'Desvio padrao de X', 'Desvio padrao de Y', 'Desvio padrao de Z', 'Mediana de X', 'Mediana de Y', 'Mediana de Z', 'Desvio Absoluto Medio de X', 'Desvio Absoluto Medio de Y', 'Desvio Absoluto Medio de Z', 'Media Quadratica de X', 'Media Quadratica de Y', 'Media Quadratica de Z') )
                #le cada valor das listas
                for value in range (len(medianX)):
                    writer.writerow( (MeArX[value], MeArY[value], MeArZ[value], VaCX[value], VaCY[value], VaCZ[value], despX[value], despY[value], despZ[value], medianX[value], medianY[value], medianZ[value], DAMX[value], DAMY[value], DAMZ[value], RMSX[value], RMSY[value], RMSZ[value]) )

            except csv.Error as e:
                print('ficheiro %s, linha %d: %s' % (ficheiro_de_gravacao, writer.line_num, e))'''      
