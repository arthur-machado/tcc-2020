import statistics
import csv

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
ficheiro_de_gravacao = 'ValoresDogSentado1.csv'

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
            #o valor lido na lista linha posicao 0 é algo como: '18:55:08.000 -> -0.10'
            #para tanto, precisamos separa o tempo e o valor do eixo x em uma posicao da lista cada
            value = linha[0].split(" -> ")
            #remove o valor antigo da lista linha
            linha.remove(linha[0])
            #adiciona o tempo na lista linha posicao 0 
            linha.insert(0, value[0])
            #adiciona o valor do eixo x na lista linha posicao 1
            linha.insert(1, value[1])
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

#mediana 
listmedianX = []
medianX = []
listmedianY = []
medianY = []
listmedianY = []
medianY = []
listmedianZ = []
medianZ = []

#desvio padrao
listdespX = []
despX = []
listdespY = []
despY = []
listdespZ = []
despZ = []


#calcula as medianas e os desvios padroes do eixo X
for values in x_AxisGroups:
    #calcula e salva a mediana
    mediana = statistics.median(values)
    listmedianX.append(mediana)
    medianX.append(listmedianX)
    #calcula e salva o desvio 
    desvio_padrao = statistics.stdev(values)
    listdespX.append(desvio_padrao)
    despX.append(listdespX)
    #reseta as listas
    listmedianX = []
    listdespX = []
#print(len(x_AxisGroups))
#print(medianX)
#print(hoursGroups)

#calcula as medianas e os desvios padroes do eixo Y
for values in y_AxisGroups:
    #calcula e salva a mediana
    mediana = statistics.median(values)
    listmedianY.append(mediana)
    medianY.append(listmedianY)
    #calcula e salva o desvio padrao
    desvio_padrao = statistics.stdev(values)
    listdespY.append(desvio_padrao)
    despY.append(listdespY)
    #reseta as listas
    listmedianY = []
    listdespY= []


#calcula as medianas e os desvios padroes do eixo Z
for values in z_AxisGroups:
    #calcula e salva a mediana
    mediana = statistics.median(values)
    listmedianZ.append(mediana)
    medianZ.append(listmedianZ)
    #calcula e salva o desvio padrao
    desvio_padrao = statistics.stdev(values)
    listdespZ.append(desvio_padrao)
    despZ.append(listdespZ)
    #reseta as listas
    listmedianZ = []
    listdespZ = []

#===============================================================#
#                   GRAVA ARQUIVO NO CSV                        #
#===============================================================#
with open(ficheiro_de_gravacao, 'w') as ficheiro:
    #'cria' a escrita no arquivo
    writer = csv.writer(ficheiro)
    try:
        #defini a linha de 'nomes' da tabela
        writer.writerow( ('Desvio padrao de X', 'Desvio padrao de Y', 'Desvio padrao de Z', 'Mediana de X', 'Mediana de Y', 'Mediana de Z') )
        #le cada linha das listas
        for value in range (len(medianX)):
            writer.writerow( (despX[value], despY[value], despZ[value], medianX[value], medianY[value], medianZ[value]) )

    except csv.Error as e:
        print('ficheiro %s, linha %d: %s' % (ficheiro_de_gravacao, writer.line_num, e))