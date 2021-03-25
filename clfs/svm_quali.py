
# -*- coding: utf-8 -*-
__author__ = 'Sidon'
from sklearn import cross_validation
from sklearn import svm
from sklearn.feature_selection import SelectKBest, f_classif
from .utilclf import *
import sys


def svm_skb_cv(exp):

    t0 = time.time()
    results = {}

    for detalhe in ['Diagonais','Horizontais', 'Verticais', 'Aproximacao']:
        exp['detalhe'] = detalhe
        # print ('\nObtendo os dados de treino')
        features, y = getdata(exp, agrupado=True)
        # print ('\nReduzindo os atributos (SKB)')
        skb = SelectKBest(f_classif, k=10000)
        xskb = skb.fit_transform(features, y)

        p0 = getp_dwt()
        results[detalhe] = getscores(features,xskb,p0)



	'''

    sp = '           '
    r1c1 = "%0.4f" % results['svmlinear0'][0]
    r1c2 = "%0.4f" % results['svmlinear0'][1]
    r1c3 = "%0.4f" % results['svmlinear1'][0]
    r1c4 = "%0.4f" % results['svmlinear1'][1]
    row1 = 'Svm Linear          '+r1c1+sp+r1c2+sp+r1c3+sp+r1c4

    r2c1 = "%0.4f" % results['svmrbf0'][0]
    r2c2 = "%0.4f" % results['svmrbf0'][1]
    r2c3 = "%0.4f" % results['svmrbf1'][0]
    r2c4 = "%0.4f" % results['svmrbf1'][1]
    row2 = 'Svm RBF             '+r2c1+sp+r2c2+sp+r2c3+sp+r2c4

    r3c1 = "%0.4f" % results['svmpoly0'][0]
    r3c2 = "%0.4f" % results['svmpoly0'][1]
    r3c3 = "%0.4f" % results['svmpoly1'][0]
    r3c4 = "%0.4f" % results['svmpoly1'][1]
    row3 = 'Svm polinomial      '+r3c1+sp+r3c2+sp+r3c3+sp+r3c4

    r4c1 = "%0.4f" % results['sgd0'][0]
    r4c2 = "%0.4f" % results['sgd0'][1]
    r4c3 = "%0.4f" % results['sgd1'][0]
    r4c4 = "%0.4f" % results['sgd1'][1]
    row4 = 'SGD                 '+r4c1+sp+r4c2+sp+r4c3+sp+r4c4

    r5c1 = "%0.4f" % results['kng0'][0]
    r5c2 = "%0.4f" % results['kng0'][1]
    r5c3 = "%0.4f" % results['kng1'][0]
    r5c4 = "%0.4f" % results['kng1'][1]
    row5 = 'Nearest Neighbors   '+r5c1+sp+r5c2+sp+r5c3+sp+r5c4

    r6c1 = "%0.4f" % results['extratree0'][0]
    r6c2 = "%0.4f" % results['extratree0'][1]
    r6c3 = "%0.4f" % results['extratree1'][0]
    r6c4 = "%0.4f" % results['extratree1'][1]
    row6 = 'Extra tree          '+r6c1+sp+r6c2+sp+r6c3+sp+r6c4


    sep1 = '----------------------------------------------------------------------------------------------------------------\n'
    cabec1 = 'Detalhe: ' + exp['detalhe'] +'::' + 'Tempo: ' + str((time.time() - t0)) + '\n'
    cabec2 = '                          Sem redução                      Redutor PCA                          Redutor ANOVA \n  '
    cabec3 = 'Classificador       Acurácia         Desvio           Acurácia         Desvio           Acurácia         Desvio \n '

    # Gravando no arquivo

    fresult.write('\n\n'+sep1)
    fresult.write(exp['descricao'])
    fresult.write(cabec1)
    fresult.write(cabec2)
    fresult.write(sep1)
    fresult.write(cabec3)
    fresult.write(sep1)
    fresult.write(row1+'\n')
    fresult.write(row2+'\n')
    fresult.write(row3+'\n')
    fresult.write(row4+'\n')
    fresult.write(row5+'\n')

    print ('----------------------------------------------------------------------------------------')
    print (exp['descricao'])
    print ('Detalhe: ', exp['detalhe'],'::', 'Tempo: ', (time.time() - t0))
    print ('                          Sem redução                      Redutor ANOVA  ')
    print ('----------------------------------------------------------------------------------------')
    print ('Classificador       Acurácia         Desvio           Acurácia         Desvio           ')
    print ('----------------------------------------------------------------------------------------')
    print (row1)
    print (row2)
    print (row3)
    print (row4)
    print (row5)
    print (row6)
	'''
    return results


def getp_dwt():

    parametros = {}

    linear = dict(C=0.01, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=1e-05, kernel='linear',
                      max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001,verbose=False)

    rbf = dict(C=10.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,  gamma=1e-05, kernel='rbf',
                    max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)

    poly = dict(C=0.01, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.01, kernel='poly', max_iter=-1,
               probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)
    parametros[detalhe] = {'linear': linear, 'rbf': rbf, 'poly': poly}

    linear = dict(C=0.01, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=1e-05, kernel='linear',
                      max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001,verbose=False)
    rbf = dict(C=10.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,  gamma=1e-05, kernel='rbf',
                    max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)
    poly = dict(C=0.01, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.01, kernel='poly', max_iter=-1,
               probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)
    parametros['Horizontais'] = {'linear': linear, 'rbf': rbf, 'poly': poly}

    linear = dict(C=0.01, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=1e-05, kernel='linear',
                      max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001,verbose=False)
    rbf = dict(C=10.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,  gamma=1e-05, kernel='rbf',
                    max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)
    poly = dict(C=0.01, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.01, kernel='poly', max_iter=-1,
               probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)
    parametros['Verticais'] = {'linear': linear, 'rbf': rbf, 'poly': poly}

    linear = dict(C=0.01, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=1e-05, kernel='linear',
                      max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001,verbose=False)
    rbf = dict(C=100.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,  gamma=1e-05, kernel='rbf',
                   max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)
    poly = dict(C=0.01, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.01, kernel='poly', max_iter=-1,
               probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)
    parametros['Diagonais'] = {'linear': linear, 'rbf': rbf, 'poly': poly}

    return parametros



def getscores(features, Xskb, y, p):

    results = {}

    # Sem redução
    # print ('\nscores sem redução')
    results['svmlinear0'] = calcscores(features, y, p)
    results['svmrbf0'] = calcscores(features, y, p)
    results['svmpoly0'] = calcscores(features, y, p)

    # Com redução
    # print ('\nscores com redução anova')
    results['svmlinear1'] = calcscores(Xskb, y, p)
    results['svmrbf1'] = calcscores(Xskb, y, p)
    results['svmpoly1'] = calcscores(Xskb, y, p)

    return results
    


def calcscores(X, y, params ):

    print('Criando o classificador: ')
    clf = svm.SVC()
    clf.setparams(**params)

    print('Criando kfold')
    kfold = cross_validation.KFold(len(X), n_folds=10)

    print('Calculando scores')
    scores = cross_validation.cross_val_score(clf, X, y, cv=kfold, n_jobs=1)

    print(scores)
    sys.exit(0)

    return (scores)


