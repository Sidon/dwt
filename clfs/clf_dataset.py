__author__ = 'sidon'


import pandas as pd
import sys
import numpy as np

from sklearn.feature_selection import SelectKBest, f_classif

import wave2
import utils
import clfs.utilclf as utilclf


def clf(ds):

    ds['path0'] = ds['main_path']+ds['target0']+utils.slash_os
    ds['path1'] = ds['main_path']+ds['target1']+utils.slash_os
    ds['path2'] = ds['main_path']+ds['target2']+utils.slash_os

    store = pd.HDFStore(ds['file_hdf'])
    for wave in (ds['wavelet1'], ds['wavelet2']):
        save_details(ds,wave,store)
        # print ('Gravando detalhes')

        store.close()
        store.open()

    if ds['dataset']=='S':
        for wave in (ds['wavelet1'], ds['wavelet2']):
            save_dataset(ds, wave, store)

    store.close()
    sys.exit(0)

    return

def save_dataset(ds,wave, store):
      # keyds  =  ds['id_dataset/']+wave+'/Datasets/Features/'
      print ('Gravando Datasets ')
      for detalhe in ('Aproximacao', 'Verticais', 'Horizontais', 'Diagonais'):
          apply_anova(ds, wave, store, detalhe)

def apply_anova(ds, wave, store, detalhe):

    keyds = ds['id_dataset']+'/'+wave+'/Dataset/Anova/'+detalhe+'/'
    features = concatena1(ds, wave, store, detalhe)
    targets = utilclf.set_targets(features.shape[0])
    anova1 = SelectKBest(f_classif, k='all')
    print ('Aplicando anova...')
    anova1.fit(features, targets)
    xreduced = np.array(features[:, np.where(anova1.pvalues_ < 0.05)[0]])
    print(('Gravando reduzido :: ', 'Key => :: ', keyds))
    store.put(keyds, pd.DataFrame(xreduced) )

    return


def concatena1(ds, wave, store, detalhe):

    keydet = ds['id_dataset']+'/'+wave+'/'+'Detalhes/'+detalhe+'/'
    print(('Carregando dataset: ', keydet+ds['target0']))
    target0=(store[keydet+ds['target0']]).tolist()
    print(('Carregando dataset: ', keydet+ds['target1']))
    target1=(store[keydet+ds['target1']]).tolist()
    print(('Carregando dataset: ', keydet+ds['target2']))
    target2=(store[keydet+ds['target2']]).tolist()

    print ('Concateando as classes')
    return np.concatenate((target0, target1, target2))


def save_details(ds, wave, store):
    key = ds['id_dataset']+'/'+wave+'/'
    targets = {ds['target0']: ds['path0'], ds['target1']: ds['path1'], ds['target2']: ds['path2']}
    for ktarget in list(targets.keys()):
            subbanda = applywave(ds, wave, targets[ktarget], ktarget)
            for detalhe in ('Aproximacao', 'Horizontais', 'Verticais', 'Diagonais'):
                keydet = key+'Detalhes/'+detalhe+'/'+ktarget
                pd_serie =  pd.Series(subbanda[detalhe])
                print(('Gravando, sub-bandas: ', '::', 'Key => ',keydet ))
                store.put(keydet, pd_serie )
    return


def applywave(ds, wave, path, target):
    print(('Aplicando wavelet','::',wave,'::', target ))
    imgs = wave2.buildimages(path)
    return wave2.build_wavelet(imgs, wave, ds['wmae'], ds['nivel'], target )


