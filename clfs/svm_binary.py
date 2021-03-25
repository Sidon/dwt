__author__ = 'sidon'


# -*- coding: utf-8 -*-
__author__ = 'Sidon'
from sklearn import cross_validation
from sklearn import svm
from sklearn.feature_selection import SelectKBest, f_classif
from .utilclf import *


# SVM Cross Validation 2 a 2
def svm_cv_one_to_one(exp):

    # Baseado em: http://scikit-learn.org/stable/modules/cross_validation.html

    print ('\nObtendo os dados)')
    features, y = getdata(exp, agrupado=False)

    cll_x_fl = np.concatenate((features['target0'], features['target1']))
    cll_x_mcl = np.concatenate((features['target0'], features['target2']))
    fl_x_mcl = np.concatenate((features['target1'], features['target2']))

    ycll = ['CLL'] * 100
    yfl = ['FL'] * 100
    ymcl = ['MCL'] * 100

    # Criacao do objeto ANOVA
    anova = SelectKBest(f_classif, k=10000)

    t0 = time.time()
    print ("\nClassificando cll x fl")
    results_cllxfl = svc_cv(cll_x_fl, ycll+yfl)
    print(("feito em %0.3fs" % (time.time() - t0)))

    t0 = time.time()
    print ("\nClassificando cll x mcl")
    results_cllxmcl = svc_cv(cll_x_mcl, ycll+ymcl)
    print(("feito em %0.3fs" % (time.time() - t0)))

    t0 = time.time()
    print ("\nClassificando fl x mcl")
    results_flxmcl = svc_cv(fl_x_mcl, yfl+ymcl)
    print(("feito em %0.3fs" % (time.time() - t0)))

    print(("\nclassification Report: ", time.strftime("%d/%m/%Y %I:%M:%S")))
    print(("Descricao Experimento: ", exp['descricao']))

    print(("\nResultados CLL x FL", results_cllxfl))
    print(("\nResultados CLL x MCL", results_cllxmcl))
    print(("\nResultados FL x MCL", results_flxmcl))


# Aplicação do svm
def svc_cv(X, targets, seletor, kernel='linear', test_size=0.2, n_folds=10):

    results = {}

    # Aplicando o Seletor
    features = seletor.fit_transform(X, targets)

    print ('\nCriando o classificador...')
    clf = svm.SVC(kernel=kernel, C=1)

    t0 = time.time()
    print ('\nComputando o score (Acurácia) ...')
    scores_SVC = cross_validation.cross_val_score(clf, features, targets, cv=n_folds)
    print(("feito em %0.3fs" % (time.time() - t0)))
    print(('Scores SVC: ',scores_SVC))

    # Media e desvio padrão
    t0 = time.time()
    accuracia, std = scores_SVC.mean(), scores_SVC.std() * 2
    print(("feito em %0.3fs" % (time.time() - t0)))
    print(("Accuracia: %0.2f (+/- %0.2f)" % (scores_SVC.mean(), scores_SVC.std() * 2)))


    '''Por default, o score computado em cada interação do CV é através do metodo do
    estimador. Isto pode ser alterado através da utilização do parametro scoring'''
    score_f1 = cross_validation.cross_val_score(clf, features, targets, cv=n_folds, scoring='f1')

    results['scores_SVC'] = scores_SVC
    results['Accuracia'] = accuracia
    results['Desvio'] = std
    results['score_f1'] = score_f1

    print(('Sores SVC: ', scores_SVC))
    print(('Acuraica: ', accuracia ))
    print(('Desvio padrão: '. std))
    print(('Score F1: ', score_f1))

    return results

