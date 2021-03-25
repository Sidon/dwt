# -*- coding: utf-8 -*-
__author__ = 'sidon'

from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn import svm
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.cross_validation import cross_val_score
import sys
import numpy as np
from sklearn import cross_validation
import matplotlib.pyplot as plt
from .utilclf import *

from sklearn.metrics import fbeta_score, make_scorer, confusion_matrix


def calcmatrix(exp):
    t0 = time.time()
    fresult = open(exp['fresult'], mode='a')
    fresult.write(exp['descricao']+'\n\n')
    #fresult.close()

    # detalhes = ['Horizontais', 'Verticais', 'Diagonais', 'Aproximacao']
    detalhes = ['Aproximacao']
    for detalhe in detalhes:

        exp['detalhe'] = detalhe
        print ('\nObtendo os dados de treino')
        features, y = getdata(exp, agrupado=True)

        #redução de atributos
        if exp['reducao']!='None':
            print(('Aplicando ANOVA, Detalhe: ', detalhe))
            anova1 = SelectKBest(f_classif, k='all')
            anova1.fit(features, y)
            xreduced = np.array(features[:, np.where(anova1.pvalues_ < 0.05)[0]])
        else:
            print(('Sem Redução, Detalhe: ', detalhe))
            xreduced = features

        # print xreduced.shape
        to = str(features.shape[1])
        tr = str(xreduced.shape[1])
        pr = str(1.0 - (xreduced.shape[1] / features.shape[1]))

        features = None

        fresult.write('\n\n')
        fresult.write('Detalhe: '+ detalhe +'\n')

        fresult.write('***************************************************'+'\n')
        fresult.write('**                    Reducao                    **'+'\n')
        fresult.write('***************************************************'+'\n')
        fresult.write('** Qt. Original | Qt. Reduzida  | % de Redução   **'+'\n')
        fresult.write('_____________________________________'+'\n')
        fresult.write('** ' + to + '       |  ' + tr + '  |  ' + pr +'          **'+'\n')
        fresult.write('**************************************************'+'\n')

        # kernels = ['linear','rbf', 'poly' ]
        kernels = ['poly']
        for kernel in kernels:

            fresult.write('\n\nKernel: '+kernel+'\n\n')

            clf = svm.SVC(kernel=kernel)
            cmtotal = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

            qtcasos = 70
            testsize = 0.10
            qttest = qtcasos * testsize
            fold = 10

            for n in range(0, int(fold)):
                temp1 = [m for m in range(int(n * qttest), int((n + 1) * qttest))]
                temp2 = [m for m in range(int(qtcasos + (n * qttest)), int(qtcasos + ((n + 1) * qttest)))]
                temp3 = [m for m in range(int((2 * qtcasos) + (n * qttest)), int((2 * qtcasos) + ((n + 1) * qttest)))]

                tempconc = np.concatenate((temp1, temp2, temp3), axis=0)


                '''
                print "Temps:"
                print '1',temp1
                print '2',temp2
                print '3',temp3
                '''
                temp1 = None
                temp2 = None
                temp3 = None

                #print tempconc

                xteste = xreduced[tempconc]
                yteste = y[tempconc]


                #print 'Shape xtest: ', xteste.shape
                #print 'Shape ytest: ', yteste.shape

                xtreino = np.delete(xreduced, tempconc, 0)
                ytreino = np.delete(y, tempconc, 0)

                ypred = clf.fit(xtreino, ytreino).predict(xteste)

                #print 'Shape xtreino: ', xtreino.shape
                #print 'Shape ytreino: ', ytreino.shape

                #print 'yteste'
                #print yteste

                print('\nypred:')
                print(ypred)

                print('\nyTeste:')
                print(yteste)

                cm = confusion_matrix(yteste, ypred)

                fresult.write('Matriz de confusão ('+detalhe+') - ' + 'fold'  +  str(n) + ':\n')
                fresult.write(str(cm))
                fresult.write('\n')

                print(('Matriz de confusao: ', '(Detalhe:', detalhe,')', 'Fold: ', n))
                print(cm)
                cmtotal = cmtotal + cm


            fresult.write('Matriz de confusão Final:'+'\n')
            fresult.write(str(cmtotal))

            print(('\nMatriz de confusão Final:','\n'))
            print(cmtotal)

            dirplot = '/media/sidon/Dados-NTFS/Copy/devel/latex/icm2/sidon_icm2_2014/figuras/resultados/anova'
            plot1 = dirplot + exp['idexp'] + '_' + detalhe + '_' + kernel + '.png'
            plt.matshow(cmtotal)
            plt.title('Confusion matrix')
            plt.colorbar()
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
            plt.savefig(plot1)

            fresult.close()
            fresult = open(exp['fresult'],mode='a')

    #final = (time.time() - t0) / 60 / 60
    #fresult.write('\nTempo em Horas: ')
    #fresult.write(final)
    fresult.close()




