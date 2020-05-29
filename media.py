import pandas as pd
#import numpy as np Não precisamos no momento
#import matplotlib.pyplot as mp

#leitura do arquivo, definido como os valores estão separados e os cabeçalhos dentro de 'names' 
arquivo = pd.read_csv('DogSentado.csv', sep=",", header=None,  names=['AX', 'AY', 'AZ'])

#variáveis para armazenar média e mediana dos dados
media = arquivo.mean()
mediana = arquivo.median()

#prints para verificar se tudo deu certo
print("Mediana: ")
print(mediana)

print("========================")

print("Médias: ")
print(media)


#armazena a mediana em um arquivo csv, senão existir ele cria 
mediana.to_csv('medianaSentado.csv', sep=',', header=False)  

    