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



def clf0(ds):

    time_inicial = datetime.now()
    print(('Time inicial: ', time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()), ':: Somente Full'))
    print((ds['descricao']))
    t1 = time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.localtime())

    ds['path0'] = ds['main_path']+ds['target0']
    ds['path1'] = ds['main_path']+ds['target1']
    ds['path2'] = ds['main_path']+ds['target2']

    store_full = pd.HDFStore(ds['file_hdf'])
    store_res =  pd.HDFStore(ds['file_hdf_result'])

    store = {'full': store_full, 'result': store_res}
    for wave in (ds['wavelet1'], ds['wavelet2']):

        print(('Wave1 ', ds['wavelet1']))
        print(('Wave2 ', ds['wavelet2']))

        if wave!='None':
            print(('Valor da wavelet',  wave))
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
    print('******* Operação terminada com sucesso ******************************')
    print('*********************************************************************')
    return


def calc_result(ds, wave, store):

    for detalhe in ('Verticais', 'Horizontais', 'Diagonais', 'Aproximacao'):

        key = ds['id_dataset']+'/'+wave+'/Resultados/'+'Full/'+detalhe+'/'

        calc_kernel = False;
        for kernel in ['linear']:
            if not (key+kernel+'/cmfolds' in store['result']):
                #print 'Nao encontrado: ', key+kernel
                calc_kernel = True

        if calc_kernel:
            key=key+'/linear'
            print(('Montando folds para subbanda: ', key, ':: Somente Full'))
            features = concatena1(ds, wave, store['full'], detalhe)
            targets = set_targets(210)
            m3.calcfolds(features, targets, store['result'], key, ds)
        else:
            print(('Key já calculada: ', key+kernel))




