#-*- coding: utf-8 -*-
__author__ = 'Sidon'

from __future__ import print_function

 from sklearn import cross_validation
 from sklearn import svm

 from utilclf import *


 ''' features = atributos, nos exemplos scikit o padrão é dataset.data, por ex. iris.data
    targets = classes, nos exemplos scikit o padrão é dataset.targets, ex. iris.target'''
def cv_svm(exp):

    # Baseado em: http://scikit-learn.org/stable/modules/cross_validation.html

    print ('Obtendo os dados ja normalizados (minha lib classutil)')
    features, targets = getdata(exp, normalize=True)

    # Aplicando o PCA
    features = applypca(features,targets, 2)

    test_part = 0.2
    kernel = 'rbf'

    print('Partiçionando os dado em testes e treino...')
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(features, targets,
                                                                         test_size=test_part, random_state=0)

    '''
    Para construir um hiperplano otimizado, SVM emprega um algoritmo iterativo, que é utilizado para minimizar a
    função de erro. SVM pode ser classificado em 4 grupos distintos, de acordo com o tipo da função de erro:

    * Classification SVM Type 1 (also known as C-SVM classification)
    * Classification SVM Type 2 (also known as nu-SVM classification)
    * Regression SVM Type 1 (also known as epsilon-SVM regression)
    * Regression SVM Type 2 (also known as nu-SVM regression)

    https://www.statsoft.com/textbook/support-vector-machines

    ------------------------------------------------------------------------------------------------------------------

    No pacote scikit learn, sklearn.svm.SVC é a função para 'C-Support Vector Classification', a implementação é
    baseada na libsvm, a complexidade no tempo é mais do que quadratica, o que torna dificil para datasets com mais
    de 10000 amostras

    O suporte a multiclasses é manipulado de acordo com o esquema um-vs-um.

    http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
    '''


    # Aplicando o PCA
    # X_train, X_test =  apply_pca(2, X_train, X_test)


    print ('Criando o classificador...')
    clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
    scores_clf = clf.score(X_test, y_test)
    ### print('Scores: ', clf.score(X_test, y_test))

    print ('Estimando a precisão de um kernel SVM em 5 k-folds...')
    clf = svm.SVC(kernel=kernel, C=1)

    print ('Computando o score (Acurácia) ...')
    scores_SVC = cross_validation.cross_val_score(clf, features, targets, cv=5)
    # print (scores_SVC)

    sys.exit(0)


    # Media e desvio padrão
    #  print("Accuracia: %0.2f (+/- %0.2f)" % (scores_SVC.mean(), scores_SVC.std() * 2))

    '''Por default, o score computado em cada interação do CV é através do metodo do
     estimador. Isto pode ser alterado através da utilização do parametro scoring'''
    score_f1 = cross_validation.cross_val_score(clf, features, targets, cv=5, scoring='f1')
    print (score_f1)

    '''
    The scoring parameter: defining model evaluation rules
    --------------------------------------------------------------
    Scoring	                Function
    ---------------------------------------------------------------
    Classification
    ‘accuracy’          	sklearn.metrics.accuracy_score
    ‘average_precision’	    sklearn.metrics.average_precision_score
    ‘f1’	                sklearn.metrics.f1_score
    ‘precision’         	sklearn.metrics.precision_score
    ‘recall’	            sklearn.metrics.recall_score
    ‘roc_auc’           	sklearn.metrics.roc_auc_score

    Clustering
    ‘adjusted_rand_score’	sklearn.metrics.adjusted_rand_score

    Regression
    ‘mean_squared_error’	sklearn.metrics.mean_squared_error
    ‘r2’                	sklearn.metrics.r2_score

     http://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter

     Em análise estatística de classificação binária, a pontuaçã F1 [F1 score (também chamado de F-score ou
     F-meassure)] é a  medida da acuracia. Esta medida considera a 'precisio' p e o 'recall' r do teste para computar
     a pontuação (o score): p é o número de resultados corretos dividido pelo numero de todos os resultados e r é o
     número de resultados corretos dividido pelo número de resultados corretos que deveriam ser retornados.
     F1 score também pode ser interpretado  como uma média ponderada da precisão e recall, onde uma pontuação F1
     atinge o seu melhor valor em 1 e pior resultado em 0.

     A F-measure tradicional ou pontuação balanceada (balanced F-score) é a média harmônica entre a precisão e o recall:

        F1 = 2[(prexison.recall)/(precison+recall)]
        fonte: http://en.wikipedia.org/wiki/F1_score

    Quando o argumento (linha acima com o fragmento de codigo: score_f1 = ...) é um inteiro,  cross_val_score usa
    as strategias KFold ou StratifiedKFold por default (dependendo da presença ou da falta do array target (classes)

    Também é possível usar outra estrategia de cross validation passando diretamente um iterator de cross validation
    em detrimento do default:
    '''


    n_samples = features.shape[0]
    cv = cross_validation.ShuffleSplit(n_samples, n_iter=3, test_size=0.3, random_state=0)
    cv_score_val = cross_validation.cross_val_score(clf, features, targets, cv=cv)

    print ("classification Report: ", time.strftime("%d/%m/%Y %I:%M:%S"),end="")
    print ("Descricao Experimento: ", exp['descricao'],end="")
    print ("Classificador: ", exp['classificador'],end="")
    print ("Kernel: ", kernel, end="")
    print ("Teste Size: ", test_part, end="")

    print ("","**** Score do calssicador *****")
    print ("svm.SVC, Kernel Linear, C=1: ", scores_clf)

    print ("","**** Cross Validation Metrics *****")
    print (print("svm.SVC, Kernel Linear, C=1: ", scores_SVC))
    print ("","***Media e Desvio a partir da do cross-validation***")
    print("Acuracia: %0.2f (+/- %0.2f)" % (scores_SVC.mean(), scores_SVC.std() * 2))

