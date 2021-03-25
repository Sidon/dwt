# -*- coding: utf-8 -*-

__author__ = 'Sidon'
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn import svm
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import cross_val_score
from .utilclf import *
from sklearn.linear_model import SGDClassifier
import sys
from sklearn import neighbors


class Resultpath:
    file = None
    def __init__(self, _path):
        self.file = open(_path)
        return file

fresult = None

def apply_exp(exp):
    clfs = getclfs()
    funcs = getfunctions(execution=True)

    for func in funcs:
        if func.__name__ == exp['funcao']:
            if exp['detalhe']=='Todos':
                #ct.addDataset(self.dataset)

                for detalhe in ['Aproximacao', 'Horizontais', 'Verticais', 'Diagonais']:
                    exp['detalhe'] = detalhe
                    rst = func(exp)
                    results = {}
                    results['detalhe'] = detalhe
                    results
            else:
                func(exp)
            break


def getclfs():
    return ['svm']


def getfunctions(execution=False):

    if execution:
        #funcs = [svm_random, svm_cva, svm_cv_one_to_one, pipeline, extratree, multiclfs, svm_skb_cv]
        funcs = [calcmatrix]

    else:
        #funcs = ['svm_random', 'svm_cva', 'svm_cv_one_to_one', 'pipeline', 'extratree', 'multiclfs', 'svm_skb_cv']
        funcs = ['calcmatrix']

    return funcs

def getseletores():
    return [select_by_extratreeclf, applypca, anova1]



# SVM particionamento randomico com pca
def svm_random(exp):
    # Obtem os dados ja normalizados (minha lib classutil)
    features, targets = getdata(exp)

    test_size = 20
    _kernel = 'rbf'

    # Fazendo o split para o set de treino e testes
    X_train, X_test, y_train, y_test = train_test_split(
        features, targets, test_size=test_size)

    # Computando o PCA
    n_components = 2
    print ("Extraindo os melhores %d componentes do set de treino => %d amostras" % (n_components, X_train.shape[0]))
    t0 = time.time()
    pca = RandomizedPCA(n_components=n_components, whiten=True).fit(X_train)
    print("realizado em %0.3fs" % (time.time() - t0))

    print("\nProjetando os dados em eigenfaces em bases ortogonais")
    t0 = time.time()
    X_train_pca = pca.transform(X_train)
    X_test_pca = pca.transform(X_test)
    print("realizado em %0.3fs" % (time.time() - t0))

    print('',"Colocando o set de treinamento no classificador ")
    t0 = time.time()
    param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5], 'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
    clf = GridSearchCV(SVC(kernel=_kernel, class_weight='auto'), param_grid)
    clf = clf.fit(X_train_pca, y_train)
    print("feito em %0.3fs" % (time.time() - t0))

    print("\nMelhor estimador encontrado pela grid:")
    print(clf.best_estimator_)

    print("\nPredizendo os nomes do linfomas no set de teste")
    t0 = time.time()
    y_pred = clf.predict(X_test_pca)
    print("feito em in %0.3fs" % (time.time() - t0))

    target_names = np.array(['CLL', 'FLL', 'MCL'])
    n_classes = 3

    print ("classification Report: ", time.strftime("%d/%m/%Y %I:%M:%S"))
    print ("Descricao Experimento: ", exp['descricao'])
    print ("Classificador: ", exp['classificador'])
    print ("Kernel: ", _kernel)
    print ("Teste Size: ", test_size)
    print ("Num componentes PCA: ", n_components)

    print(classification_report(y_test, y_pred, target_names=target_names))
    print('Confusion Matrix:', confusion_matrix(y_test, y_pred, labels=list(range(n_classes))))

    sys.exit(0)


# SVM Cross Validation Agrupados
def svm_cva(exp):

    # Baseado em: http://scikit-learn.org/stable/modules/cross_validation.html

    print ('\nObtendo os dados (minha lib classutil)')
    features, targets = getdata(exp, agrupado=True)

    # Aplicando o PCA
    features = applypca(features,targets, 2)

    test_part = 0.2
    kernel = 'rbf'

    print('Partiçionando os dados em testes e treino...')
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(features, targets,
                                                                         test_size=test_part, random_state=0)
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

    n_samples = features.shape[0]
    cv = cross_validation.ShuffleSplit(n_samples, n_iter=3, test_size=0.3, random_state=0)
    cv_score_val = cross_validation.cross_val_score(clf, features, targets, cv=cv)

    print("classification Report: ", time.strftime("%d/%m/%Y %I:%M:%S"))
    print("Descricao Experimento: ", exp['descricao'])
    print("Classificador: ", exp['classificador'])
    print("Kernel: ", kernel, end="")
    print("Teste Size: ", test_part)

    print("","**** Score do calssicador *****")
    print("svm.SVC, Kernel Linear, C=1: ", scores_clf)

    print("","**** Cross Validation Metrics *****")
    print(print("svm.SVC, Kernel Linear, C=1: ", scores_SVC))
    print("","***Media e Desvio a partir da do cross-validation***")
    print("Acuracia: %0.2f (+/- %0.2f)" % (scores_SVC.mean(), scores_SVC.std() * 2))



def pipeline(exp):

    results ={}

    kernel = str(exp['kernel'])
    clf = str(exp['clf'])
    folds = int(exp['folds'])


    print ('\nObtendo os dados (minha lib classutil)')
    X, y = getdata(exp, agrupado=True)

    if exp['seletor']=='anova':
        print('Criando o filtro anova (selectbest)')
        select = SelectKBest(f_classif, k=10000)

    if exp['seletor']=='pca':
        select

    if exp['clf']=='svm':
        print('Criando o classificador svm')
        clf = svm.SVC(kernel=kernel)

    print('Criando o pipeline')
    pipe = Pipeline([(exp['seletor'], select), (exp['clf'], clf)])

    print('Fazendo o fit no pipeline')
    pipe.fit(X,y)

    t0 = time.time()
    print('Criando scores')
    scores_pipe = cross_val_score(pipe,X, y, cv=folds, verbose=3)
    custo_tempo_scores_pipe = (time.time() - t0)

    results['scores_pipe'] = scores_pipe
    results['custo_tempo_pipe'] = custo_tempo_scores_pipe
    results['acuracia'] = scores_pipe.mean()
    results['std'] = scores_pipe.std()

    print('\nResutltados:\n' )
    print('Em: ', time.strftime("%d/%m/%Y %I:%M:%S"))
    print(exp['experimento_id'])
    print('\nCusto, tempo: ',custo_tempo_scores_pipe)
    print('Scores pipé:\n', scores_pipe)
    print('Acuracia: ', results['acuracia'])

    t0 = time.time()
    print('Criando scores F1')
    results['score_f1'] = cross_val_score(pipe, X, y, cv=folds, scoring='f1', verbose=3 )
    custo_scores_f1 = (time.time() - t0)
    print('Scores F1: ', results['score_f1'])

    return results


def extratree(exp):

    print ('\nObtendo os dados (minha lib classutil)')
    X, y = getdata(exp, agrupado=True)

    print ('\nCriando o classificador')
    t0 = time.time()
    clf = ExtraTreesClassifier()
    X_new = clf.fit(X, y).transform(X)
    custo_tempo_tree = (time.time() - t0)

    t0 = time.time()
    print ('\nCriando o score:')
    score = clf.score(X,y)
    custo_tempo_score = (time.time() - t0)

    print('Custo tempo tree: ', custo_tempo_tree)
    print('Custo tempo score:', custo_tempo_score)

    print('Scores:\n ', score)

    print('Criando o score do teste...')
    t0 = time.time()
    X_test, y_test = gettest(exp,'target0')
    score_test = clf.score(X_test,y_test)
    custo_tempo_score_test = (time.time() - t0)

    print('Custo do score teste: ', custo_tempo_score_test)
    print('Score do teste: ', score_test)

    print ('\nPredict: \n',clf.predict(X_test))
    print ('\nDados Reais:\n', y_test)

    return


def anova1(exp):

    results = {}

    kernel = str(exp['kernel'])
    clf = str(exp['clf'])
    folds = int(exp['folds'])

    print ('\nObtendo os dados de treino')
    features, targets = getdata(exp, agrupado=True)


    print ('\nReduzindo os atributos')
    skb = SelectKBest(f_classif, k=1000)
    f_reduced = skb.fit_transform(features, targets)

    X = f_reduced[12:][:]
    y = targets[12:]

    X_test = f_reduced[0:12][:]
    y_test = targets[0:14]

    print('X.shape: ',X.shape)
    print('y.shape: ',y.shape)

    print('X_test.shape: ',X_test.shape)
    print('y_test.shape: ',y_test.shape)

    print('Criando o classificador svm')
    clf = svm.SVC(kernel='linear')
    clf.fit(X_test, y_test)

    print('Calculando a acuracia')
    accuracia = clf.score(X_test,y_test)

    print('accuracia :', accuracia)

    print ('\nPredict: \n',clf.predict(X_test))
    print ('\nDados Reais:\n', y_test)


    #X_new = applypca(X, y, 2)
    return


def multiclfs(exp, pca=True):

    t0 = time.time()
    results = {}

    '''if  fresult==None:
        fresult = Resultpath.file'''

    print ('\nObtendo os dados de treino')
    features, y = getdata(exp, agrupado=True)

    print ('\nReduzindo os atributos (SKB)')
    skb = SelectKBest(f_classif, k=10000)
    Xskb = skb.fit_transform(features, y)

    Xpca = features
    if pca:
        print ('\nReduzindo os atributos (PCA)')
        pca = PCA(n_components=2)
        pca.fit(features)
        Xpca = pca.fit_transform(features,y)

    # Sem redução
    print ('\nscores sem redução')
    results['svmlinear0'] = calcscores('svmlinear', features, y, n_folds=10)
    # results['svmrbf0'] = calcscores('svmrbf', features, y, n_folds=10)
    # results['svmpoly0'] = calcscores('svmpoly', features, y, n_folds=10)
    results['sgd0'] = calcscores('sgd', features, y, n_folds=10)
    results['kng0'] = calcscores('kng', features, y, n_folds=10)
    results['extratree0'] = calcscores('extratree', features, y, n_folds=10)


    
    print ('\nscores com pca')
    results['svmlinear1'] = calcscores('svmlinear', Xpca, y, n_folds=10)
    # results['svmrbf1'] = calcscores('svmrbf', Xpca, y, n_folds=10)
    # results['svmpoly1'] = calcscores('svmpoly', Xpca, y, n_folds=10)
    results['sgd1'] = calcscores('sgd', Xpca, y, n_folds=10)
    results['kng1'] = calcscores('kng', Xpca, y, n_folds=10)
    results['extratree1'] = calcscores('extratree', Xpca, y, n_folds=10)


    # Com redução
    print ('\nscores com redução anova')
    results['svmlinear2'] = calcscores('svmlinear', Xskb, y, n_folds=10)
    # results['svmrbf2'] = calcscores('svmrbf', Xskb, y, n_folds=10)
    # results['svmpoly2'] = calcscores('svmpoly', Xskb, y, n_folds=10)
    results['sgd2'] = calcscores('sgd', Xskb, y, n_folds=10)
    results['kng2'] = calcscores('kng', Xskb, y, n_folds=10)
    results['extratree2'] = calcscores('extratree', Xskb, y, n_folds=10)

    sp = '           '
    r1c1 = "%0.4f" % results['svmlinear0'][0]
    r1c2 = "%0.4f" % results['svmlinear0'][1]
    r1c3 = "%0.4f" % results['svmlinear1'][0]
    r1c4 = "%0.4f" % results['svmlinear1'][1]
    r1c5 = "%0.4f" % results['svmlinear2'][0]
    r1c6 = "%0.4f" % results['svmlinear2'][1]
    row1 = 'Svm Linear          '+r1c1+sp+r1c2+sp+r1c3+sp+r1c4+sp+r1c5+sp+r1c6

    r2c1 = "%0.4f" % results['svmrbf0'][0]
    r2c2 = "%0.4f" % results['svmrbf0'][1]
    r2c3 = "%0.4f" % results['svmrbf1'][0]
    r2c4 = "%0.4f" % results['svmrbf1'][1]
    r2c5 = "%0.4f" % results['svmrbf2'][1]
    r2c6 = "%0.4f" % results['svmrbf2'][1]
    #row2 = 'Svm RBF             '+r2c1+sp+r2c2+sp+r2c3+sp+r2c4+sp+r2c5+sp+r2c6

    r3c1 = "%0.4f" % results['svmpoly0'][0]
    r3c2 = "%0.4f" % results['svmpoly0'][1]
    r3c3 = "%0.4f" % results['svmpoly1'][0]
    r3c4 = "%0.4f" % results['svmpoly1'][1]
    r3c5 = "%0.4f" % results['svmpoly2'][0]
    r3c6 = "%0.4f" % results['svmpoly2'][1]
    #row3 = 'Svm polinomial      '+r3c1+sp+r3c2+sp+r3c3+sp+r3c4+sp+r3c5+sp+r3c6

    r4c1 = "%0.4f" % results['sgd0'][0]
    r4c2 = "%0.4f" % results['sgd0'][1]
    r4c3 = "%0.4f" % results['sgd1'][0]
    r4c4 = "%0.4f" % results['sgd1'][1]
    r4c5 = "%0.4f" % results['sgd2'][0]
    r4c6 = "%0.4f" % results['sgd2'][1]
    row4 = 'SGD                 '+r4c1+sp+r4c2+sp+r4c3+sp+r4c4+sp+r4c5+sp+r4c6


    r5c1 = "%0.4f" % results['kng0'][0]
    r5c2 = "%0.4f" % results['kng0'][1]
    r5c3 = "%0.4f" % results['kng1'][0]
    r5c4 = "%0.4f" % results['kng1'][1]
    r5c5 = "%0.4f" % results['kng2'][0]
    r5c6 = "%0.4f" % results['kng2'][1]
    row5 = 'Nearest Neighbors   '+r5c1+sp+r5c2+sp+r5c3+sp+r5c4+sp+r5c5+sp+r5c6

    r6c1 = "%0.4f" % results['extratree0'][0]
    r6c2 = "%0.4f" % results['extratree0'][1]
    r6c3 = "%0.4f" % results['extratree1'][0]
    r6c4 = "%0.4f" % results['extratree1'][1]
    r6c5 = "%0.4f" % results['extratree2'][0]
    r6c6 = "%0.4f" % results['extratree2'][1]
    row6 = 'Extra tree          '+r6c1+sp+r6c2+sp+r6c3+sp+r6c4+sp+r6c5+sp+r6c6



    '''
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
    '''

    print ('----------------------------------------------------------------------------------------------------------------')
    print (exp['descricao'])
    print ('Detalhe: ', exp['detalhe'],'::', 'Tempo: ', (time.time() - t0))
    print ('                          Sem redução                      Redutor PCA                          Redutor ANOVA    ')
    print ('-----------------------------------------------------------------------------------------------------------------')
    print ('Classificador       Acurácia         Desvio           Acurácia         Desvio           Acurácia         Desvio  ')
    print ('-----------------------------------------------------------------------------------------------------------------')
    print (row1)
    print (row2)
    print (row3)
    print (row4)
    print (row5)
    print (row6)

    return results




def svm_skb_cv(exp, pca=True):

    t0 = time.time()
    results = {}

    '''if  fresult==None:
        fresult = Resultpath.file'''

    # print ('\nObtendo os dados de treino')
    features, y = getdata(exp, agrupado=True)

    # print ('\nReduzindo os atributos (SKB)')
    skb = SelectKBest(f_classif, k=10000)
    Xskb = skb.fit_transform(features, y)

    param_rbf = dict(C=10.0, gamma=0.0001, kernel='rbf')
    parm_sgd = dict(criterion='gini', max_features = 'log2', min_samples_split=10, n_estimators=1000)


    '''
    parm_poly =
    param kng0 =
    param_et =
    '''

    # Sem redução
    # print ('\nscores sem redução')
    results['svmlinear0'] = calcscores('svmlinear', features, y, n_folds=10)
    results['svmrbf0'] = calcscores('svmrbf', features, y, param_rbf, n_folds=10)
    results['svmpoly0'] = calcscores('svmpoly', features, y, n_folds=10)
    results['sgd0'] = calcscores('sgd', features, y, n_folds=10)
    results['kng0'] = calcscores('kng', features, y, n_folds=10)
    results['extratree0'] = calcscores('extratree', features, y, n_folds=10)


    # Com redução
    # print ('\nscores com redução anova')
    results['svmlinear1'] = calcscores('svmlinear', Xskb, y, n_folds=10)
    results['svmrbf1'] = calcscores('svmrbf', Xskb, y, param_rbf, n_folds=10)
    results['svmpoly1'] = calcscores('svmpoly', Xskb, y, n_folds=10)
    results['sgd1'] = calcscores('sgd', Xskb, y, n_folds=10)
    results['kng1'] = calcscores('kng', Xskb, y, n_folds=10)
    results['extratree1'] = calcscores('extratree', Xskb, y, n_folds=10)

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



    '''
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
    '''

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

    return results



def calcscores(sclf, X, y, grid, detalhe, n_folds=10):

    print ('sclf: ', sclf)
    gamma = 1e-05
    c=0.01

    print('Criando o classificador: ', sclf)
    if sclf=='svmlinear':
        kernel = 'linear'
    elif sclf=='svmrbf':
        kernel = 'rbf'
        if detalhe=='Aproximacao':
            c=10
        elif detalhe=='Horizontais':
            c=10.0
            gamma = 0.0001
        elif detalhe=='Verticais':
            c = 0.01
        elif detalhe=='Diagonais':
            c=100.0
        clf = svm.SVC(C=c, gamma=gamma, kernel='rbf' )

    elif sclf=='svmpoly':
        kernel = 'poly'
        clf = svm.SVC(C=1, kernel='poly')

    if kernel != None:
        clf = svm.SVC(C=c, gamma=gamma, kernel=kernel )


    if sclf=='sgd':
        clf = SGDClassifier(loss="hinge", penalty="l2")
    elif sclf=='extratree':
        clf = ExtraTreesClassifier()
    elif sclf=='kng':
        clf = neighbors.KNeighborsClassifier()
    elif sclf=='extratree':
        clf = ExtraTreesClassifier(criterion='gini', max_features = 'log2', min_samples_split=10, n_estimators=1000)


    print('Criando kfold')
    kfold = cross_validation.KFold(len(X), n_folds=n_folds)

    print('Calculando scores',sclf)
    scores = cross_validation.cross_val_score(clf, X, y, cv=kfold, n_jobs=1)

    mean = scores.mean()
    std = scores.std()


    return (mean, std)



