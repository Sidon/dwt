# -*- coding: utf-8 -*-
__author__ = 'sidon'

import numpy as np
import pandas as pd
import time
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.decomposition import PCA
import sys
import numpy as np
from sklearn import svm
from sklearn.feature_selection import SelectKBest, f_classif
import utils
from . import utilclf
from datetime import date
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.metrics import confusion_matrix
from sklearn import cross_validation as crv
import itertools as it
from datetime import datetime


# Classificação
def clf_svm(targets, features, store, key):

    print(('\nClassificando...', key))
    for kernel in ('linear', 'rbf', 'poly'):

        clf = svm.SVC(kernel=kernel)

        print(('Calculando matriz de confusao ',key+kernel))
        cms, acuracias = calcfolds(features,targets,70,0.10,10,clf)

        # print 'Gravando matriz de confusao ',key+kernel
        store.put( key+kernel+'/cms', pd.Series(cms))
        store.put( key+kernel+'/acuracias', pd.Series(acuracias))

    store.close()
    store.open()
    clf=None
    return

# Concatenacao das imagens
def concatena1(ds, wave, store, detalhe):

    # Contatena as distribuições das 3 classes diferentes da subbanda

    features=[]
    for t in ('FL', 'MCL', 'CLL'):
        print(('Concatenando: ', t))
        key = ds['id_dataset']+'/'+wave+'/'+'Detalhes/'+t+'/'+detalhe+'/Subbanda'
        features.append(np.array(store[key].tolist()))

    return np.concatenate((features[0], features[1], features[2]))


# Reorganização da concatenação das imagens para kfold
def tenfolds(features, qtcasos, testsize, nfold, targets):

    qttest = qtcasos * testsize
    l1 = []
    l2 = []

    for n in range(0, int(nfold)):

        # print 'Concatenando fold: ', n

        temp1 = [m for m in range(int(n * qttest), int((n + 1) * qttest))]
        l2.extend(list(it.repeat(targets[0], len(temp1))))

        temp2 = [m for m in range(int(qtcasos + (n * qttest)), int(qtcasos + ((n + 1) * qttest)))]
        l2.extend(list(it.repeat(targets[1], len(temp2))))

        temp3 = [m for m in range(int((2 * qtcasos) + (n * qttest)), int((2 * qtcasos) + ((n + 1) * qttest)))]
        l2.extend(list(it.repeat(targets[2], len(temp3))))

        tempc = np.concatenate((temp1, temp2, temp3),axis=0)
        l1.append(tempc)

    return features[((np.array(l1)).flatten())], l2


# Aplicação da calscores
def calc_cross(features, targets, store, key, ds):

    for kernel in ('linear', 'rbf', 'poly'):

        if not (key+kernel in store):
            print(('Calculando scores...', key+kernel))
            clf = svm.SVC(kernel=kernel)
            scores, metrics, cost_time = calcscores(features, np.array(targets), 10, clf, key+kernel, ds, 1)

            # print 'Gravando matriz de confusao ',key+kernel
            df_metrics = pd.DataFrame(data=list(metrics.values()), index=list(metrics.keys()))
            df_costs = pd.DataFrame(data=list(cost_time.values()), index=list(cost_time.keys()))
            store.put( key+kernel+'/metrics', df_metrics)
            store.put( key+kernel+'/scores', pd.Series(scores))
            store.put( key+kernel+'/cost_time', df_costs)
            store.close()
            store.open()
        else:
            print((key+kernel, ' => ', 'Já calculado'))


# Kfold da scikit (retorno de metricas)
def calcscores(features, targets, nfolds, clf, key, ds, _jobs=1):

    kfold = crv.KFold(len(features), n_folds=nfolds)
    cost_time = {}

    tempo0 = datetime.now()
    inicio = datetime.now()
    print(('Calculo Scores ::', key,' :: ', ds['descricao'],' :: ', time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())))


    scores = crv.cross_val_score(clf, features, targets, cv=kfold, n_jobs=_jobs)
    cost_time['scores'] = (inicio-datetime.now()).total_seconds()

    inicio = datetime.now()
    print(('Calculo Accuracy ::', key,' :: ', ds['descricao'],' :: ', time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())))
    accuracy = crv.cross_val_score(clf, features, targets, cv=kfold, n_jobs=_jobs, scoring='accuracy')
    # Average se restring a classificacao binaria
    cost_time['accuracy'] = (inicio-datetime.now()).total_seconds()


    inicio = datetime.now()
    print(('Calculo F1 ::', key,' :: ', ds['descricao'],' :: ', time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())))

    f1 = crv.cross_val_score(clf, features, targets, cv=kfold, n_jobs=_jobs, scoring='f1')
    cost_time['f1'] = (inicio-datetime.now()).total_seconds()


    inicio = datetime.now()
    print(('Calculo Precision ::', key,' :: ', ds['descricao'],' :: ', time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())))
    precision = crv.cross_val_score(clf, features, targets, cv=kfold, n_jobs=_jobs, scoring='precision')
    cost_time['precison'] = (inicio-datetime.now()).total_seconds()

    inicio = datetime.now()
    print(('Calculo Recall ::', key,' :: ', ds['descricao'],' :: ', time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())))
    recall = crv.cross_val_score(clf, features, targets, cv=kfold, n_jobs=_jobs, scoring='recall')
    cost_time['recall'] = (inicio-datetime.now()).total_seconds()

    cost_time['Total'] = (tempo0-datetime.now()).total_seconds()
    # roc_acu_score (AUC) se restringe á classificacao binaria
    metrics = {'accuracy': accuracy, 'f1': f1, 'precision': precision, 'recall': recall}

    return scores, metrics, cost_time


'''
# Normalizando ou 'padronizando' os dados
Recurso de dimensionamento ou padronizacao das amostras: Para todo atributo, atributo = ((atributo - media)/desvio)
'''
def normalize(f):
    scaler = StandardScaler().fit(f)
    features = scaler.transform(f)

    return features


def set_targets(n_allsamples, labels=[0, 1, 2]):

    n_targets = len(labels)
    target_samples = n_allsamples/n_targets

    targets = []
    for label in labels:
        newtarget = [label]*target_samples
        targets.extend(newtarget)

    return np.array(targets)


# Calcula e grava a matriz de confusao
# Aplicação da calscores
def calc_cm(features, targets, store, key, ds):

    for kernel in ('linear'):

        if not (key+kernel+'/cm' in store):
            print(('Calculando matriz de confusao...', key+kernel))
            clf = svm.SVC(kernel=kernel)

            scores, metrics, cost_time = calcscores(features, np.array(targets), 10, clf, key+kernel, ds, 1)

            # print 'Gravando matriz de confusao ',key+kernel
            df_metrics = pd.DataFrame(data=list(metrics.values()), index=list(metrics.keys()))
            df_costs = pd.DataFrame(data=list(cost_time.values()), index=list(cost_time.keys()))
            store.put( key+kernel+'/metrics', df_metrics)
            store.put( key+kernel+'/scores', pd.Series(scores))
            store.put( key+kernel+'/cost_time', df_costs)
            store.close()
            store.open()
        else:
            print((key+kernel, ' => ', 'Já calculado'))


