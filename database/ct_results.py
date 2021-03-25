# -*- coding: utf-8 -*-
__author__ = 'sidon'
from .model import Results
from . import dbutil
import utils
# Based: http://css.dzone.com/articles/wxpython-and-sqlalchemy

conf = utils.getconfig('')

def addresult(row):

    #  O Dataset deve ser um dicionárioprprecisaoecisao
    result = Results()
    result.id_dataset = row['id_dataset']
    result.wavelet = row['wavelet']
    result.wavemae = row['wavemae']
    result.redutor = row['redutor']
    result.reducao = row['reducao']
    result.subbanda = row['subbanda']
    result.atributos_subbanda = row['atributos_subbanda']
    result.kernel = row['kernel']
    result.acuracia = row['acuracia']
    result.f1 = row['f1']
    result.precisao = row['precisao']
    result.recall = row['recall']

    result.time = row['time']
    result.fator = row['fator']
    result.desvio = row['desvio']
    result.atributos = row['atributos']

    result.espectro = row['espectro']
    result.canal = row['canal']
    result.key_kernel = row['key_kernel']

    result.num_fl = row['num_fl']
    result.num_mcl = row['num_mcl']
    result.num_cll = row['num_cll']

    result.fl_fl = row['fl_fl']
    result.fl_mcl = row['fl_mcl']
    result.fl_cll = row['fl_cll']

    result.mcl_fl = row['mcl_fl']
    result.mcl_mcl = row['mcl_mcl']
    result.mcl_cll = row['mcl_cll']

    result.cll_fl = row['cll_fl']
    result.cll_mcl = row['cll_mcl']
    result.cll_cll = row['cll_cll']

    session = dbutil.connectToDatabase()
    session.add(result)
    session.commit()
    session.close()


def editResults(idNum, row, edit=False):

    session = dbutil.connectToDatabase()
    record = session.query(Datasets).filter_by(id=idNum).one()
    record.id_dataset = row['id_dataset']
    record.wavelet = row['wavelet']
    record.wavemae = row['wavemae']
    record.redutor = row['redutor']
    record.reducao = row['reducao']
    record.subbanda = row['subbanda']
    record.subbanda = row['atributos_subbanda']

    record.kernel = row['kernel']
    record.acuracia = row['acuracia']
    record.f1 = row['f1']
    record.precisao = row['precisao']
    record.recall = row['recall']

    record.time = row['time']
    record.fator = row['fator']
    record.desvio = row['desvio']
    record.atributos = row['atributos']

    record.espectro = row['espectro']
    record.canal = row['canal']

    record.key_kernel = row['key_kernel']

    record.num_fl = row['num_fl']
    record.num_mcl = row['num_mcl']
    record.num_cll = row['num_cll']

    record.fl_fl = row['fl_fl']
    record.fl_mcl = row['fl_mcl']
    record.fl_cll = row['fl_cll']

    record.mcl_fl = row['mcl_fl']
    record.mcl_mcl = row['mcl_mcl']
    record.mcl_cll = row['mcl_cll']

    record.cll_fl = row['cll_fl']
    record.cll_mcl = row['cll_mcl']
    record.cll_cll = row['cll_cll']


    # session.add(record)
    session.commit()
    session.close()


def deleteresult(idnum):
    session = dbutil.connectToDatabase()
    record = session.query(Results).filter_by(id=idnum).one()
    session.delete(record)
    session.commit()
    session.close()


def getallresults():
    session = dbutil.connectToDatabase()
    datasets = session.query(Results).all()
    session.close()
    return datasets  #  O Dataset deve ser um dicionário


def searchRecords(keyword, filterfield='id'):
    session = dbutil.connectToDatabase()
    result = ''
    if filterfield == "id":
        qry = session.query(Results)
        result = qry.filter(Results.id == keyword).all()
    return result


# Converte um registro em um dicionario
def result2dict(_rs):
    rs_dict = {}
    rs_dict['id'] = _rs.id
    rs_dict.id_dataset = _rs['id_dataset']
    rs_dict.wavelet = _rs['wavelet']
    rs_dict.wavemae = _rs['wavemae']
    rs_dict.redutor = _rs['redutor']
    rs_dict.reducao = _rs['reducao']
    rs_dict.subbanda = _rs['subbanda']
    rs_dict.subbanda = _rs['atributos_subbanda']

    rs_dict.kernel = _rs['kernel']
    rs_dict.acuracia = _rs['acuracia']
    rs_dict.f1 = _rs['f1']
    rs_dict.precisao = _rs['precisao']
    rs_dict.recall = _rs['recall']

    rs_dict.desvio = _rs['desvio']
    rs_dict.time = _rs['time']
    rs_dict.fator = _rs['fator']
    rs_dict.atributos = _rs['atributos']
    rs_dict.espectro = _rs['espectro']
    rs_dict.canal = _rs['canal']

    rs_dict.key_kernel = _rs['key_kernel']

    rs_dict.num_fl = _rs['num_fl']
    rs_dict.num_mcl = _rs['num_mcl']
    rs_dict.num_cll = _rs['num_cll']

    rs_dict.num_fl = _rs['num_fl']
    rs_dict.num_mcl = _rs['num_mcl']
    rs_dict.num_cll = _rs['num_cll']

    rs_dict.fl_fl = _rs['fl_fl']
    rs_dict.fl_mcl = _rs['fl_mcl']
    rs_dict.fl_cll = _rs['fl_cll']

    rs_dict.mcl_fl = _rs['mcl_fl']
    rs_dict.mcl_mcl = _rs['mcl_mcl']
    rs_dict.mcl_cll = _rs['mcl_cll']

    rs_dict.cll_fl = _rs['cll_fl']
    rs_dict.cll_mcl = _rs['cll_mcl']
    rs_dict.cll_cll = _rs['cll_cll']


    return rs_dict


# Converte registros em uma lista de dicionarios
def results2listdicts(results):
    rs_list = []
    for rs in results:
        rs_list.append(result2dict(rs))
    return rs_list
