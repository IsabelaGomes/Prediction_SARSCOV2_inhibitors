# -*- coding: utf-8 -*-
"""2_search_pipeline.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10uPiB8cOAj1vxfSjb3wJfYYBmKJ2UsKT
"""

pip install tpot

from google.colab import drive
drive.mount('/content/drive')

from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn import preprocessing
import numpy as np
import pandas as pd
import os
from numpy.matlib import repmat

"""
def pre_process(train_set, drugbank):
    # Dado concatenado
    all_data = pd.concat([train_set,drugbank])
    #SVD
    U, s, V = np.linalg.svd(np.transpose(all_data), full_matrices=True)
    # Valores singulares normalizados
    y = s * (1/np.sum(s))
    # Calcula o "joelho" da curva
    rank = get_knee(y)
    # Computa matrix aproximada de posto reduzido
    new_data = low_rank_approximation(s, V , rank)
    # Normalizando os dados
    data_scaled = preprocessing.scale(new_data)
    # separa train_set do drugbank
    new_train_set = data_scaled[:len(train_set)][:]
    new_drugbank_set = data_scaled[len(train_set):][:]

    return new_train_set, new_drugbank_set
"""
'''
  Funções auxiliares para o SVD
'''
"""
# In: singular values
def get_knee(sgl_values):
    values = list(sgl_values)

    #get coordinates of all the points
    nPoints = len(values)
    allCoord = np.vstack((range(nPoints), values)).T

    # get the first point
    firstPoint = allCoord[0]

    # get vector between first and last point - this is the line
    lineVec = allCoord[-1] - allCoord[0]
    lineVecNorm = lineVec / np.sqrt(np.sum(lineVec**2))
    # find the distance from each point to the line:
    # vector between all points and first point
    vecFromFirst = allCoord - firstPoint
    scalarProduct = np.sum(vecFromFirst * repmat(lineVecNorm, nPoints, 1), axis=1)
    vecFromFirstParallel = np.outer(scalarProduct, lineVecNorm)
    vecToLine = vecFromFirst - vecFromFirstParallel

    # distance to line is the norm of vecToLine
    distToLine = np.sqrt(np.sum(vecToLine ** 2, axis=1))

    # knee/elbow is the point with max distance value
    return np.argmax(distToLine) + 1

# In: rank, sigle values and rows
def low_rank_approximation(s, V, rank):
    return np.transpose(np.dot(np.diag(s[:rank]), V[:][:rank]))

"""

def split_data(train_data, proporcao):
    # nova proporcao entre as classes
    DENOMINATOR = proporcao
    
    # rows with positive class
    pos_data = train_data[train_data['class'] == 1]
    
    # rows with negative class
    neg_data = train_data[train_data['class'] == 0]
    
    # The number of partitions is set according the positive class length
    p = int(len(neg_data)/len(pos_data))
    if p < DENOMINATOR:
        n_parts = p
    else:
        n_parts = int((len(neg_data)/len(pos_data))/DENOMINATOR)

    return pos_data, neg_data, n_parts

def run_search_pipelines(train_set, out_dir):
    
    # split data
    pos_data, neg_data, N_PARTITIONS = split_data(train_set, 4)
    
    # shuffle negative index
    permuted_indices = np.random.permutation(len(neg_data))
    for i in range(N_PARTITIONS):
        print(i,':',N_PARTITIONS)
        
        # Concat positive and a fragment os negative instances
        final_matrix = pd.concat([pos_data, neg_data.iloc[permuted_indices[i::N_PARTITIONS]]])
        
        # Separa classe dos atributos
        train_data = final_matrix.iloc[:,:-1]
        train_class = final_matrix.iloc[:,-1]
        
        # Run SVD
        #new_train_data, new_test_set = pre_process(train_data, test_set)
        
        X_train, X_test, y_train, y_test = train_test_split(train_data, train_class,train_size=0.75,test_size=0.25)
        pipeline_optimizer = TPOTClassifier(generations=5, population_size=25, cv=5,random_state=42, verbosity=2, scoring="roc_auc") #roc_auc, f1
        pipeline_optimizer.fit(X_train, y_train)
        pipeline_optimizer.export(pipelines + 'pipeline_'+ str(i) + '.py')

"""# MAIN"""

train_set = pd.read_csv('/content/drive/My Drive/covid/COVID/train_set.csv', index_col="name")
#drugbank = pd.read_csv('/content/drive/My Drive/covid/Drugbank/drugbank.csv', index_col="name")
pipelines = '/content/drive/My Drive/covid/COVID/pipelines2/'

run_search_pipelines(train_set, drugbank, pipelines)
