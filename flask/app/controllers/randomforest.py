import pandas                   as pd
import numpy                    as np
from sklearn.ensemble           import RandomForestClassifier
from sklearn.model_selection    import train_test_split
from sklearn.impute             import SimpleImputer
from sklearn                    import preprocessing
from sklearn                    import utils
from pathlib                    import Path

# Classificação da atividade com Random Forest
# [Name: scikit-learn Version: 0.24.1]
# [Name: scipy        Version: 1.6.0 ]

#funcao que prediz a acao do cao
def WhichActivityIs(sensorData_Package):

    activity = "Indisponível"

    #carrega o dataset de treino
    dfTreino = pd.read_csv(Path('c:\\Projetos\\TCC\\tcc-2020\\flask\\app\\controllers\\datasetdog.csv'))

    #defini o mapeamento
    map_activity = {'sitting':0, 'running':1, 'walking':2, 'jumping':3, 'lying_down':4, 'stopped':5}

    #aplica o mapeamento ao dataset
    dfTreino['activity'] = dfTreino['activity'].map(map_activity)

    #Seleciona as variaveis
    features = ['absolute_deviation', 'standard_deviation', 'arithmetic_average', 'RMS', 'median', 'variance']

    #Defini a variavel a ser prevista
    feat_predicted = ['activity']

    #Cria o objeto
    X = dfTreino[features].values
    Y = dfTreino[feat_predicted].values

    #passa a lista para o formato array do numpay
    sensorData = np.array(sensorData_Package)

    #Defini o tamanho da base de teste (split)
    split_test_size = 0.10

    #Criando dados de treino e de teste
    X_training, X_test, Y_training, Y_test = train_test_split(X,Y, test_size = split_test_size, random_state=42) 

    #Criando objeto de substituicao
    exchange_Zero = SimpleImputer(missing_values = 0, strategy = "mean")

    #Substituindo os valores iguais a zero pela media dos dados
    X_training = exchange_Zero.fit_transform(X_training)
    X_test = exchange_Zero.fit_transform(X_test)

    Y_training = exchange_Zero.fit_transform(Y_training)
    Y_test = exchange_Zero.fit_transform(Y_test)

    #Codifica rotulos de destino entre 0 e n_classes-1
    lab_enc = preprocessing.LabelEncoder()
    Y_trainingEnc = lab_enc.fit_transform(Y_training)

    #Defini o modelo de RandomForest (classificador)
    clf = RandomForestClassifier(max_depth=50, min_samples_leaf=5, min_samples_split=10, n_estimators=40, random_state=42)
    clf.fit(X_training, Y_trainingEnc.ravel())

    #Calcula a acuracia e captura o id da atividade prevista
    ##result = clf.predict(X_test[-1:]))
    result = clf.predict(sensorData[-1:])

    #Defini a atividade prevista
    if result == [0]:
        activity = "Sentado"
    elif result == [1]:
        activity = "Correndo"
    elif result == [2]:
       activity = "Caminhando"
    elif result == [3]:
        activity = "Pulando"
    elif result == [4]:
        activity = "Deitado"
    elif result == [5]:
        activity = "Parado"

    return activity