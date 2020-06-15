import csv
import pandas as pd
import numpy as np

##1 - Capturar dados brutos do sensor (Arduino) [FEITO]
##2 - Pré-processamento | filtro (arc Python (ARDUINO POR ENQUANTO)) [FEITO]
##3 - Segmentação dos dados | time window - 10s (fixa), Frequência 50Hz* (arc Python) [FEITO]
##4 - Feature extraction (estatísticas) (arc Python)
##5 - Classificação da atividade (Cadeias ocultas de Markov e Random Forest)
#*a frequência

#===============================================================#
#         LEITURA E SEPARACAO DE DADOS DO ARQUIVO CSV           #
#===============================================================#

#defini o arquivo .csv a ser lido
nome_ficheiro = 'DogSentado.csv'
#defini o arquivo .csv que recebera os dados
ficheiro_de_gravacao = 'ValoresDogSentadoO.csv'

#lista que armazena o conteudo das linhas ['hora', 'x', 'y', 'z']
linesValues = []

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


#'abre' o arquivo
with open(nome_ficheiro, 'r') as ficheiro:
    #'armazena' a leitura do arquivo
    reader = csv.reader(ficheiro)
    try:
        #le cada linha do arquivo
        for linha in reader:
            #salva o valor da linha em uma lista
            linesValues.append(linha)

    except csv.Error as e:
        print('ficheiro %s, linha %d: %s' % (nome_ficheiro, reader.line_num, e))

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
    #reinicia a lista segundos reconhecidos
    group = []
    #reinicia a lista horas reconhecidas
    hours = []
    #reinicia os listaes de eixos conhecidos
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
    #calcula a raiza quadrada nao negativa da 'soma divida'. essa raiz e a media quadratica
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
#                   GRAVA ARQUIVO NO CSV                        #
#===============================================================#
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
        print('ficheiro %s, linha %d: %s' % (ficheiro_de_gravacao, writer.line_num, e))
