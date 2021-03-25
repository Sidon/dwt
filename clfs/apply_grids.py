__author__ = 'sidon'

from sklearn import grid_search

from clfs import utilclf
from clfs.applyclf import *


def gridsearch(exp):
    
    t0 = time.time()
    if exp['detalhe']=='Todos':
        fresult = open(exp['fresult'],mode='a')
        fresult.write(exp['descricao'])
        fresult.close()

        for kernel in ['linear', 'rbf', 'poly', 'sigmoid']:
            search_detalhes(gridsearch_svm, exp, (kernel,))


        search_detalhes(gridsearch_et, exp)

    fresult = open(exp['fresult'],mode='a')
    fresult.write('\nTempo em Horas: ')
    fresult.write( (time.time()-t0)/60/60)

    # fresult.close()


def search_detalhes(get_grid, exp, kernel=('None',)):
    results = {}
    t0 = time.time() 
    detalhes = ['Aproximacao', 'Horizontais', 'Verticais', 'Diagonais']
    for detalhe in detalhes:
        exp['detalhe'] = detalhe
        gs0 = get_grid(exp, kernel)
        results['Estimator'] = gs0.best_estimator_
        results['Acuracia'] = gs0.best_score_
        results['Detalhe'] = detalhe
        results['Tempo'] = (time.time()-t0)/60/60
        save_result(results,exp['fresult'])


def save_result(results, path):

    print('Salvando...')
    file = open(path,mode='a')
    file.write('\n--------------------------------------------------------\n')
    file.write('Detalhe:'+results['Detalhe']+'\n')
    file.write('Estimator:\n'+str(results['Estimator'])+'\n')
    file.write('Acuracia: '+str(results['Acuracia'])+'\n')
    
    file.write('Tempo (Em Horas): '+str(results['Tempo']))

    file.close()
 

def gridsearch_svm(exp, kernel, redutor=None):

    #print exp

    features, y = utilclf.getdata(exp, agrupado=True)
    if redutor != None:
        if redutor=='skb':
            skb = SelectKBest(f_classif, k=10000)
            x_reduced = skb.fit_transform(features, y)
    else:
        x_reduced = features
        
    kfold = cross_validation.KFold(len(x_reduced), n_folds=10)
    c_range = 10.0 ** np.arange(-2, 9)
    gamma_range = 10.0 ** np.arange(-5, 4)

    param_grid = dict(C=c_range, kernel=kernel, gamma=gamma_range)
    gs0 = GridSearchCV(SVC(), param_grid=param_grid, cv=kfold)

    print((kernel[0], 'fitting ....'))
    gs0.fit(x_reduced, y)


    return gs0


def gridsearch_et(exp, kernel=None, redutor=None):

    features, y = utilclf.getdata(exp, agrupado=True)

    if redutor != None:
        if redutor=='skb':
            skb = SelectKBest(f_classif, k=10000)
            x_reduced = skb.fit_transform(features, y)
    else:
        x_reduced = features


    kfold = cross_validation.KFold(len(x_reduced), n_folds=10)

    parm_extra_tree = {'n_estimators':[10, 100, 1000, 10000], 'criterion':('gini', 'entropy'),
                   'max_features':('auto','sqrt', 'log2'), 'min_samples_split':[2, 10, 100]}

    clf_extratree = ExtraTreesClassifier()
    gs0 = grid_search.GridSearchCV(clf_extratree, parm_extra_tree, cv=kfold)

    print((exp['detalhe'],': Extratree sem reducao fitting....'))
    gs0.fit(features, y)

    return gs0
