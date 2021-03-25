# -*- coding: utf-8 -*-
__author__ = 'admin'

import pandas as pd
import sys
import numpy as np
from sklearn import svm
from sklearn.feature_selection import SelectKBest, f_classif
import utils
import clfs.utilclf as utilclf
import time
import numpy as np
from .utilclf import *
from datetime import date
from sklearn.metrics import confusion_matrix
from sklearn import cross_validation as crv
from sklearn.feature_selection import SelectPercentile, f_classif
from datetime import datetime


def clfr0(ds):

    time_inicial = datetime.now()
    print(('Time inicial: ', time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()), ':: Redutores'))
    print((ds['descricao']))
    t1 = time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.localtime())

    ds['path0'] = ds['main_path']+ds['target0']
    ds['path1'] = ds['main_path']+ds['target1']
    ds['path2'] = ds['main_path']+ds['target2']

    store_full = pd.HDFStore(ds['file_hdf'])
    store_res =  pd.HDFStore(ds['file_hdf_result'])

    store = {'full': store_full, 'result': store_res}
    for wave in (ds['wavelet1'], ds['wavelet2']):

        if wave!='None':
            calc_result(ds, wave, store)
        else:
            print('Wavelet = None')

    time_total = (time_inicial - datetime.now()).total_seconds()/60/60
    store_res.put(ds['id_dataset']+'/Time/T1', pd.Series([t1]))
    store_res.put(ds['id_dataset']+'/Time/T2', pd.Series([time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.localtime())]))
    store_res.put(ds['id_dataset']+'/Time/Total', pd.Series(str(time_total)+' horas'))

    store_res.close()
    store_full.close()

    print(('Time final: ', time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.localtime())))
    sys.exit(0)

    return


def calc_result(ds,wave, store):

      # keyds  =  ds['id_dataset/']+wave+'/Datasets/Features/'

      pvalues = {'09': 0.9, '05': 0.5, '02': 0.2, '005': 0.05, '001': 0.01}
      for detalhe in ('Aproximacao', 'Verticais', 'Horizontais', 'Diagonais'):
          features = None
          for redutor in ((ds['redutor1'],ds['fredutor1']), (ds['redutor2'],ds['fredutor2'])):
              if redutor[1]=='S':
                  for k in list(pvalues.keys()):
                      key = ds['id_dataset']+'/'+wave+'/Resultados/'+redutor[0]+'-'+k+'/'+detalhe


                      calckernel = False
                      for kkernel in ('linear', 'rbf', 'poly'):

                          if not (key+'/'+kkernel in store['result']) or not (key in store['result']):
                              calckernel = True
                              break

                      if calckernel:
                          print(('Calculos para: ', key+'/'+kkernel))
                          if (features==None):
                              features, targets = tenfolds(concatena1(ds, wave, store['full'], detalhe), 70, 0.1, 10, ( 0, 1, 2 ))
                          xreduced = reduct_features(features, targets, redutor[0],pvalues[k] )
                          key += '/'
                          calc_cross(xreduced,targets,store['result'], key, ds)
                          store['result'].put( key+'Shape', pd.Series(xreduced.shape))
                          store['result'].put( key+'Fator', pd.Series(pvalues[k]))
                          store['result'].close()
                          store['result'].open()

      return


def reduct_features(features, targets, redutor, pvalue):

    print(('Aplicando ', redutor))
    if (redutor=='Anova'):
        selector = SelectKBest(f_classif, k='all')
        selector.fit(features, targets)
        xreduced = np.array(features[:, np.where(selector.pvalues_ < pvalue)[0]])

    elif (redutor=='Percentil'):
        selector = SelectPercentile(f_classif, percentile=10*pvalue)
        selector.fit(features, targets)
        xreduced = selector.transform(features)

    elif (redutor==None):
        print('Falta um redutor')
        sys.exit(0)

    return xreduced

