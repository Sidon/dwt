#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.feature_selection import RFECV
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score, KFold
from scipy.stats import sem
from sklearn import metrics
import sys

store = pd.HDFStore('/home/sidon/etc/output/lymphoma/hdf/swt2_haar.h5')

opcao = 2
coef_analise = 'Aproximacao'
path_store = '/SWT2_DB1_1_113'


# Carregando Aproximação nível 1 dwt2 (100 imagens)
features_cll = np.array( (store[path_store+'/wcll/'+coef_analise]).tolist())#CLL
features_fl = np.array( (store[path_store+'/wfl/'+coef_analise]).tolist())  #FL
features_mcl = np.array( (store[path_store+'/wmcl/'+coef_analise]).tolist())#MCL

features = np.concatenate((features_cll, features_fl, features_mcl))
samples = features.shape[0]/3
targets = np.concatenate( (np.zeros(samples, np.int8), np.ones(samples, np.int8), np.ones(samples, np.int8)+1 ))

print(('Shape de features: ', features.shape))
print(('Shape de targets: ', targets.shape))

sys.exit(0)

'''
Padronizando os dados
Recurso de dimensionamento ou padronizacao das amostras: Para todo atributo, atributo = ((atributo - media)/desvio)
'''
print('Padronizando')
scaler = StandardScaler().fit(features)
features = scaler.transform(features)

'''
Criando as partições de treino e teste
A função train_test_split cria automaticamente os conjuntos de dados de treinamento e avaliação e faz a seleção
aleatória das amostas.
'''
print('Criando as partições de treino e teste')
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.25, random_state=33)

print('Create the RFE object and compute a cross-validated score.')
svc = SVC(kernel="linear")

print('Criando o seletor')
selector  = RFECV(estimator=svc, step=1, cv=2, scoring='accuracy', verbose=1)

print('Fazendo a seleção')
new_features = selector.fit_transform(X_train, y_train)

print(("Optimal number of features : %d" % rfecv.n_features_))
print((('Score: '), selector.score(X_train, y_train)))


'''
print('Criando anova')
anova_filter = SelectKBest(f_regression, k=3)

print('Criando o classificador')
svc_1 = SVC(kernel='linear')
anova_svm = make_pipeline(anova_filter, svc_1)
anova_svm.fit(features, targets)
'''

def evaluate_cross_validation(clf, X, y, K):
    # create a k-fold croos validation iterator
    cv = KFold(len(y), K, shuffle=True, random_state=0)
    # by default the score used is the one returned by score method of the estimator (accuracy)
    scores = cross_val_score(clf, X, y, cv=cv)
    print(scores)
    print((("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))))


print('Fazendo a avaliação do cross validation')
evaluate_cross_validation(anova_svm, features, targets, 5)


def train_and_evaluate(clf, X_train, X_test, y_train, y_test):

    clf.fit(X_train, y_train)

    print("Accuracy on training set:")
    print((clf.score(X_train, y_train)))
    print("Accuracy on testing set:")
    print((clf.score(X_test, y_test)))

    y_pred = clf.predict(X_test)

    print("Classification Report:")
    print((metrics.classification_report(y_test, y_pred)))
    print("Confusion Matrix:")
    print((metrics.confusion_matrix(y_test, y_pred)))
    n_components = 150

    '''
    # MCL
    wmcl_n1_cA = (store['/gray_dwt2_db8_100_2niveis/wmcl/Nivel1/'+coef_analise]).tolist()
    wmcl_n1_cH = (store['/gray_dwt2_db8_100_2niveis/wmcl/Nivel1/Horizontais']).tolist()
    wmcl_n1_cV = (store['/gray_dwt2_db8_100_2niveis/wmcl/Nivel1/Verticais']).tolist()
    wmcl_n1_cD = (store['/gray_dwt2_db8_100_2niveis/wmcl/Nivel1/Diagonais']).tolist()

    wmcl_n2_cA = (store['/gray_dwt2_db8_100_2niveis/wmcl/Nivel2/'+coef_analise]).tolist()
    wmcl_n2_cH = (store['/gray_dwt2_db8_100_2niveis/wmcl/Nivel2/Horizontais']).tolist()
    wmcl_n2_cV = (store['/gray_dwt2_db8_100_2niveis/wmcl/Nivel2/Verticais']).tolist()
    wmcl_n2_cD = (store['/gray_dwt2_db8_100_2niveis/wmcl/Nivel2/Diagonais']).tolist()


    #FL
    wfl_n1_cA = (store['/gray_dwt2_db8_100_2niveis/wfl/Nivel1/'+coef_analise]).tolist()
    wfl_n1_cH = (store['/gray_dwt2_db8_100_2niveis/wfl/Nivel1/Horizontais']).tolist()
    wfl_n1_cV = (store['/gray_dwt2_db8_100_2niveis/wfl/Nivel1/Verticais']).tolist()
    wfl_n1_cD = (store['/gray_dwt2_db8_100_2niveis/wfl/Nivel1/Diagonais']).tolist()

    wfl_n2_cA = (store['/gray_dwt2_db8_100_2niveis/wfl/Nivel2/'+coef_analise]).tolist()
    wfl_n2_cH = (store['/gray_dwt2_db8_100_2niveis/wfl/Nivel2/Horizontais']).tolist()
    wfl_n2_cV = (store['/gray_dwt2_db8_100_2niveis/wfl/Nivel2/Verticais']).tolist()
    wfl_n2_cD = (store['/gray_dwt2_db8_100_2niveis/wfl/Nivel2/Diagonais']).tolist()

    #CLL
    wcll_n1_cA = (store['/gray_dwt2_db8_100_2niveis/wcll/Nivel1/'+coef_analise]).tolist()
    wcll_n1_cH = (store['/gray_dwt2_db8_100_2niveis/wcll/Nivel1/Horizontais']).tolist()
    wcll_n1_cV = (store['/gray_dwt2_db8_100_2niveis/wcll/Nivel1/Verticais']).tolist()
    wcll_n1_cD = (store['/gray_dwt2_db8_100_2niveis/wcll/Nivel1/Diagonais']).tolist()

    wcll_n2_cA = (store['/gray_dwt2_db8_100_2niveis/wcll/Nivel2/'+coef_analise]).tolist()
    wcll_n2_cH = (store['/gray_dwt2_db8_100_2niveis/wcll/Nivel2/Horizontais']).tolist()
    wcll_n2_cV = (store['/gray_dwt2_db8_100_2niveis/wcll/Nivel2/Verticais']).tolist()
    wcll_n2_cD = (store['/gray_dwt2_db8_100_2niveis/wcll/Nivel2/Diagonais']).tolist()
    '''


    store.close()






