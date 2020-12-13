import pandas as pd
import math

df = pd.read_csv('datasetDog_v.1_WithActivity.csv')
total_size = len(df)

# Aqui tu adiciona o tamanho do dataset com atividade
train_size = math.floor(0.80*total_size)

test_dataset = df.tail(len(df) - train_size)

test_dataset.to_csv('test.csv')


