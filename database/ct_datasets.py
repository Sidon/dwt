# -*- coding: utf-8 -*-
__author__ = 'sidon'

from .model import Datasets
from . import dbutil
import utils
# Based: http://css.dzone.com/articles/wxpython-and-sqlalchemy

conf = utils.getconfig('')

def addDataset(row):
    #  O Dataset deve ser um dicionário
    dataset = Datasets()
    dataset.id_dataset = row['id_dataset']
    dataset.espectro = row['espectro']
    dataset.canal = row['canal']
    dataset.descricao = row['descricao']
    dataset.main_path = row['main_path']
    dataset.nivel = row['nivel']
    
    dataset.wavelet1 = row['wavelet1']
    dataset.wavelet2 = row['wavelet2']
    
    dataset.redutor1 = row['redutor1']
    dataset.redutor2 = row['redutor2']
    
    dataset.fredutor1 = row['fredutor1']
    dataset.fredutor2 = row['fredutor2']

    # dataset.clfful = row['clfful']

    dataset.wmae = row['wmae']

    dataset.file_hdf = row['file_hdf']
    dataset.file_hdf_result = row['file_hdf_result']


    dataset.target0 = row['target0']
    dataset.target1 = row['target1']
    dataset.target2 = row['target2']

    dataset.dataset = row['dataset']
    dataset.detalhes = row['detalhes']


    # connect to session and commit data to database
    session = dbutil.connectToDatabase()
    session.add(dataset)
    session.commit()
    session.close()

def deleteDataset(idNum):
    session = dbutil.connectToDatabase()
    record = session.query(Datasets).filter_by(id=idNum).one()
    session.delete(record)
    session.commit()
    session.close()

def editDataset(idNum, row):
    session = dbutil.connectToDatabase()
    record = session.query(Datasets).filter_by(id=idNum).one()
    record.id_dataset = row['id_dataset']
    record.espectro = row['espectro']
    record.canal = row['canal']
    record.descricao = row['descricao']
    record.main_path = row['main_path']
    record.nivel = row['nivel']
    record.wavelet1 = row['wavelet1']
    record.wavelet2 = row['wavelet2']

    record.redutor1 = row['redutor1']
    record.redutor2 = row['redutor2']
    
    record.fredutor1 = row['fredutor1']
    record.fredutor2 = row['fredutor2']

    record.clfful = row['clffull']

    record.wmae = row['wmae']

    record.file_hdf = row['file_hdf']
    record.file_hdf_result = row['file_hdf_result']

    record.target0 = row['target0']
    record.target1 = row['target1']
    record.target2 = row['target2']
    record.dataset = row['dataset']
    record.detalhes = row['detalhes']

    # session.add(record)
    session.commit()
    session.close()


def getAllDatasets():
    session = dbutil.connectToDatabase()
    datasets = session.query(Datasets).all()
    session.close()
    return datasets #  O Dataset deve ser um dicionário

def searchRecords(keyword, filterfield='id'):
    session = dbutil.connectToDatabase()
    if filterfield == "id":
        qry = session.query(Datasets)
        result = qry.filter(Datasets.id == keyword).all()

    return result

# Converte registros em uma lista de dicionarios
def datasets2listdicts(datasets):
    ds_list = []
    for ds in datasets:
        ds_list.append(dataset2dict(ds))
    return ds_list


# Converte um registro em um dicionario
def dataset2dict(ds):
    ds_dict = {}
    ds_dict['id'] = ds.id
    ds_dict['id_dataset'] = ds.id_dataset

    ds_dict['espectro'] = ds.espectro
    ds_dict['canal'] = ds.canal

    ds_dict['descricao']  = ds.descricao
    ds_dict['main_path'] = ds.main_path
    ds_dict['nivel'] = ds.nivel

    ds_dict['wavelet1'] = ds.wavelet1
    ds_dict['wavelet2'] = ds.wavelet2
    ds_dict['wmae'] = ds.wmae

    ds_dict['file_hdf'] = ds.file_hdf
    ds_dict['file_hdf_result'] = ds.file_hdf_result


    ds_dict['target0'] = ds.target0.strip()
    ds_dict['target1'] = ds.target1.strip()
    ds_dict['target2'] = ds.target2.strip()

    ds_dict['dataset'] = ds.dataset
    ds_dict['detalhes'] = ds.detalhes

    ds_dict['redutor1'] = ds.redutor1
    ds_dict['redutor2'] = ds.redutor2

    ds_dict['fredutor1'] = ds.fredutor1
    ds_dict['fredutor2'] = ds.fredutor2

    ds_dict['clffull'] = ds.clffull


    return  ds_dict