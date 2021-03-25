# -*- coding: utf-8 -*-

###
# Nesta etapa as distribuições já foram construidas
#

__author__ = 'sidon'

from sklearn import svm
from sklearn.metrics import confusion_matrix
from .utilclf import *
import utils


def calcmatrix2(exp):

    store = pd.HDFStore(exp['store'])
    targets = np.array(store[exp['key']+'/Targets' ])

    for detalhe in ('Aproximacao', 'Verticais', 'Horizontais', 'Diagonais'):

        for kernel in ('linear', 'rbf', 'poly'):
            clf = svm.SVC(kernel=kernel)

            # features = utils.concatena1(ds, wave, store, detalhe)
            features = np.array(store[ exp['key']+'/Datasets/Features/Full/'+detalhe ])
            cmfolds = calcfolds(features, targets, 100, 0.10, 10, clf)

            # print cmfolds.shape
            # store.put(exp['key']+'/Results/Full/targets = np.array(store[exp['key']+'/Targets' ])'+detalhe+'/'+kernel, pd.Series(cmfolds))

            features = np.array(store[ exp['key']+'/Datasets/Features/Anova/'+detalhe ])
            cmfolds = calcfolds(features, targets, 100, 0.10, 10, clf)
            store.put(exp['key']+'/Results/Anova/'+detalhe+'/'+kernel, pd.Series(cmfolds))


def calcfolds(features, targets, qtcasos, testsize, nfold, clf):

    qttest = qtcasos * testsize
    cmtotal = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    cmfolds = []


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
        #print 'Matriz de confusao: ', '(Detalhe:', detalhe,')', 'Fold: ', n

    return cmfolds

def geratex1(paramstex, results):
    spaces = 12
    content = '\\begin{table}[!h]\n'
    content += '\\centering\n'
    content += '\\caption{'+paramstex['caption']+'}\n'
    content += '\\label{'+paramstex['label']+'\n'
    content += '\\begin{tcolorbox}[width=13.5cm,tabularx={l |l| |r |r| r| r}]\n'
    content += (' '*16)+'&'+(' '*18)+'& \\multicolumn{2}{l|}{Sem Redução}    & \\multicolumn{2}{l}{Redução ANOVA}\\\\\n'
    content += '\\cline{3-6}\n'
    content += 'Subbanda'.ljust(16)+'&\\textit{Kernel}  '+'& Acurácia'.ljust(spaces)+'& Desvio'.ljust(spaces)+\
               '& Acurácia'.ljust(spaces)+'& Desvio'.ljust(spaces)+'\n'
    content += '\\hline\\hline\n'

    # Aproximação
    acfull = results['Detalhes']['full']['Aproximacao']['svmlinear']['acuracia']
    dpfull = results['Detalhes']['full']['Aproximacao']['svmlinear']['desvio']
    acanova = results['Detalhes']['anova']['Aproximacao']['svmlinear']['acuracia']
    dpanova = results['Detalhes']['anova']['Aproximacao']['svmlinear']['desvio']
    content += '&'.rjust()+' SVM Linear'.ljust(spaces)+'& '+acfull.lust(spaces)+'& '+dpfull.ljust(spaces)+'& '+\
               acanova.ljust(spaces)+'& '+dpanova.ljust(spaces)+'\\\n'

    content += '\\hline\\hline\n'

    # Detalhes Horizontais
    acfull = results['Detalhes']['full']['Horizontais']['svmrbf']['acuracia']
    dpfull = results['Detalhes']['full']['Horizontais']['svmrbf']['desvio']
    acanova = results['Detalhes']['anova']['Horizontais']['svmrbf']['acuracia']
    dpanova = results['Detalhes']['anova']['Horizontais']['svmrbf']['desvio']
    content += '&'.rjust()+' SVM RBF'.ljust(spaces)+'& '+acfull.lust(spaces)+'& '+dpfull.ljust(spaces)+'& '+\
               acanova.ljust(spaces)+'& '+dpanova.ljust(spaces)+'\\\n'

    content += '\\hline\\hline\n'

    # Detalhes verticais
    acfull = results['Detalhes']['full']['Verticais']['svmpoly']['acuracia']
    dpfull = results['Detalhes']['full']['Verticais']['svmpoly']['desvio']
    acanova = results['Detalhes']['anova']['Verticais']['svmpoly']['acuracia']
    dpanova = results['Detalhes']['anova']['Verticais']['svmpoly']['desvio']
    content += '&'.rjust()+' SVM Polinomial'.ljust(spaces)+'& '+acfull.lust(spaces)+'& '+dpfull.ljust(spaces)+'& '+\
               acanova.ljust(spaces)+'& '+dpanova.ljust(spaces)+'\\\n'

    content += '\\hline\\hline\n'

    # Detalhes Diagonais
    acfull = results['Detalhes']['full']['Diagonais']['svmpoly']['acuracia']
    dpfull = results['Detalhes']['full']['Diagonais']['svmpoly']['desvio']
    acanova = results['Detalhes']['anova']['Diagonais']['svmpoly']['acuracia']
    dpanova = results['Detalhes']['anova']['Diagonais']['svmpoly']['desvio']
    content += '&'.rjust()+' SVM Polinomial'.ljust(spaces)+'& '+acfull.lust(spaces)+'& '+dpfull.ljust(spaces)+'& '+\
               acanova.ljust(spaces)+'& '+dpanova.ljust(spaces)+'\\\n'

    content += '\\hline\n'
    content += '\\end{tcolorbox}'
    content += '\\end{table}'


