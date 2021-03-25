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
from . import matrix3 as m3


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
    print('Operação terminada com sucesso')

    return


def calc_result(ds,wave, store):

      # keyds  =  ds['id_dataset/']+wave+'/Datasets/Features/'
      redutor = ['Anova']
      pvalues = {'09': 0.9, '05': 0.5, '02': 0.2, '005': 0.05, '001': 0.01}
      for detalhe in ('Aproximacao', 'Verticais', 'Horizontais', 'Diagonais'):
          features = None
          for k in list(pvalues.keys()):
              key = ds['id_dataset']+'/'+wave+'/Resultados/'+redutor[0]+'-'+k+'/'+detalhe

              calckernel = False
              for kkernel in ['linear']:

                  if not (key+'/'+kkernel+'/metrics2' in store['result']):
                      calckernel = True
                      break
                  else:
                      print((key+'/'+kkernel, ": *** Calculado ***"))

              if calckernel:
                  key=key+'/linear'
                  print(('Calculos para: ', key))

                  if (features==None):
                      features = concatena1(ds, wave, store['full'], detalhe)
                      targets = set_targets(210)
                  xreduced = reduct_features(features, targets, redutor[0],pvalues[k] )
                  m3.calcfolds(xreduced, targets, store['result'], key, ds)

      return


def reduct_features(features, targets, redutor, pvalue):

    print(('Aplicando ', redutor))
    if (redutor=='Anova'):
        selector = SelectKBest(f_classif, k='all')
        selector.fit(features, targets)
        xreduced = np.array(features[:, np.where(selector.pvalues_ < pvalue)[0]])
    else:
        print('Redutor errado')
        sys.exit(0)

    return xreduced

