import pandas as pd
import numpy as np
import matplotlib.pyplot as mp

arquivo = pd.read_csv('mediaGiro.csv', sep=",",  names=['X', 'Y', 'Z'])
arquivo.convert_dtypes("float")

print(arquivo.dtypes)

