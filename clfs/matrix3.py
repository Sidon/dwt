# -*- coding: utf-8 -*-

###
# Nesta etapa as distribuições já foram construidas
#

__author__ = 'sidon'

from sklearn import svm
from sklearn.metrics import confusion_matrix
from .utilclf import *
import utils
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score


def calcfolds(features, targets, store, key, ds, clf=svm.SVC(kernel='linear'), qtcasos=70, testsize=0.1, nfold=10):

    qttest = qtcasos * testsize
    cmtotal = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    cmfolds = []
    pfolds = []
    f1folds = []
    accfolds = []
    rfolds = []

    metrics2 = {}

    print('Calculando Matriz Confusao:')
    print(key)

    for n in range(0, int(nfold)):
        temp1 = [m for m in range(int(n * qttest), int((n + 1) * qttest))]
        temp2 = [m for m in range(int(qtcasos + (n * qttest)), int(qtcasos + ((n + 1) * qttest)))]
        temp3 = [m for m in range(int((2 * qtcasos) + (n * qttest)), int((2 * qtcasos) + ((n + 1) * qttest)))]
        tempconc = np.concatenate((temp1, temp2, temp3), axis=0)

        temp1=temp2=temp3=None

        #print tempconc
        xteste = features[tempconc]
        yteste = targets[tempconc]

        xtreino = np.delete(features, tempconc, 0)
        ytreino = np.delete(targets, tempconc, 0)

        ypred = clf.fit(xtreino, ytreino).predict(xteste)

        cm = confusion_matrix(yteste, ypred)
        precision = precision_score(yteste,ypred)
        f1 = f1_score(yteste,ypred)
        recall = recall_score(yteste,ypred)
        accuracia = accuracy_score(yteste, ypred)

        cmfolds.append(cm)
        pfolds.append(precision)
        f1folds.append(f1)
        rfolds.append(recall)
        accfolds.append(accuracia)


        print(('\nAcuuracia, Iteracao: ',n))
        print(key)
        print((ds['file_hdf']))
        print((ds['file_hdf_result']))
        print(('\n',accfolds))

        cmtotal = cmtotal + cm

    print('\nMatriz de confusão Final: ')
    print(('\n',cmtotal))

    dirplot = '/home/sidon/devel/python/swt/resultados/2015/graficos/cms/'
    plot1 = dirplot + key.replace('/','_') + '.png'
    plt.matshow(cmtotal)
    plt.title('Matriz de Confusão'.decode('utf-8'))
    plt.colorbar()
    plt.ylabel('Referência'.decode('utf-8'))
    plt.xlabel('Predição'.decode('utf-8'))
    plt.savefig(plot1)

    ps_cmf = pd.Series(data=cmfolds)
    df_cmt = pd.DataFrame(data=cmtotal)


    metrics2['Precisions'] = pfolds
    metrics2['f1s'] =  f1folds
    metrics2['recalls'] = rfolds
    metrics2['accuracias'] = accfolds

    dfm2 = pd.DataFrame(data=list(metrics2.values()), index=list(metrics2.keys()))

    store.put( key+'/cmfolds', ps_cmf)
    store.put( key+'/cmtotal', df_cmt)
    store.put( key+'/metrics2', dfm2)

    store.close()
    store.open()

    return


