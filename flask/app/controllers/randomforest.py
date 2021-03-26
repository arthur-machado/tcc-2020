from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn import preprocessing
from sklearn import utils
import pandas as pd
import numpy as np
from pathlib import Path

# Classificação da atividade com Random Forest
# [Name: scikit-learn Version: 0.24.1]

#funcao que prediz a acao do cao
def WhichActivityIs(sensorData_Package):

    activity = "undefined"

    #carrega o dataset de treino
    df = pd.read_csv(Path('c:\\Projetos\\TCC\\tcc-2020\\flask\\app\\controllers\\datasetdog.csv'))

    #defini o mapeamento
    map_activity = {'sitting':0, 'running':1, 'walking':2, 'jumping':3, 'lying_down':4, 'stopped':5}

    #aplica o mapeamento ao dataset
    df['activity'] = df['activity'].map(map_activity)

    #Seleciona as variaveis
    features = ['absolute_deviation', 'standard_deviation', 'arithmetic_average', 'RMS', 'median', 'variance']

    #Defini a variavel a ser prevista
    feat_predicted = ['activity']

    #Cria o objeto
    X = df[features].values
    Y = df[feat_predicted].values

    #passa a lista para o formato array do numpay
    sensorData = np.array(sensorData_Package)

    #Converte os valores em float para int, dessa forma o sistema aceita a entrada
    #lab_enc = preprocessing.LabelEncoder()
    #sensorData = lab_enc.fit_transform(sensorData)


    #Converte a matriz de 6-d para 1d
    #sensorData = sensorData.reshape(-1, 1)

    #Converte a lista para 24 colunas
    #X = X.reshape(-1, 36)

    #Inverte a lista, para que o sistema considere o mesmo numero de colunas [24]
    #X = X.transpose()
    #sensorData = sensorData.transpose()

    #Defini o tamanho da base de teste (split)
    split_test_size = 0.20

    #Criando dados de treino e de teste
    X_training, X_test, Y_training, Y_test = train_test_split(X,Y, test_size = split_test_size, random_state=42) 

    #Criando objeto de substituicao
    exchange_Zero = SimpleImputer(missing_values = 0, strategy = "mean")

    #Substituindo os valores iguais a zero pela media dos dados
    X_training = exchange_Zero.fit_transform(X_training)
    X_test = exchange_Zero.fit_transform(X_test)

    Y_training = exchange_Zero.fit_transform(Y_training)
    Y_test = exchange_Zero.fit_transform(Y_test)
   
    #'''

    #Defini o modelo de RandomForest (classificador)
    clf = RandomForestClassifier(max_depth=50, min_samples_leaf=5, min_samples_split=10, n_estimators=40, random_state=42)
    clf.fit(X_training, Y_training.ravel())

    #Calcula a acuracia e captura o id da atividade prevista
    result = clf.predict(Y_test[-1:])

    #Defini a atividade prevista
    if result == [0]:
        activity = "sitting"
    elif result == [1]:
        activity = "running"
    elif result == [2]:
       activity = "walking"
    elif result == [3]:
        activity = "jumping"
    elif result == [4]:
        activity = "lying_down"
    elif result == [5]:
        activity = "stopped"#'''

    return activity