# -*- coding: utf-8 -*-
__author__ = 'sidon'
from sqlalchemy import Column
from sqlalchemy import Integer, Float, String, Date, CHAR, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

from .dbconnection import *
import utils

conf = utils.getconfig('')
engine = Connection().connectdb(conf['database'], True)
Base = declarative_base(engine)
metadata = Base.metadata

class Datasets(Base):
    __tablename__ = "Datasets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_dataset = Column(String(60))
    espectro = Column(String(20))
    canal = Column(String(20))
    descricao = Column(String(70))
    main_path = Column(String(150))
    nivel = Column(String(1))
    wavelet1 = Column(String(5))
    wavelet2 = Column(String(5))

    redutor1 = Column(String(10))
    redutor2 = Column(String(10))
    fredutor1 = Column(String(1))
    fredutor2 = Column(String(1))

    clffull = Column(String(1))
    wmae = Column(String(10))
    file_hdf = Column(String(150))
    file_hdf_result = Column(String(150))

    target0 = Column(String(10))
    target1 = Column(String(10))
    target2 = Column(String(10))
    dataset = Column(String(1))  # Indica se é para salvar ou não o dataset sem reducao ( 1 = True)
    detalhes = Column(String(1)) # Indica se é para salvar ou não os detalhes wavelets



class Results(Base):
    __tablename__ = "Results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_dataset = Column(String(60))
    wavelet = Column(String(5))
    wavemae = Column(String(10))
    redutor = Column(String(20))
    reducao = Column(DECIMAL(10,3))
    subbanda = Column(String(20))
    atributos_subbanda = Column(DECIMAL(10))

    kernel = Column(String(20))
    acuracia = Column(DECIMAL(10,3))
    f1 = Column(DECIMAL(10,3))
    precisao = Column(DECIMAL(10,3))
    recall = Column(DECIMAL(10,3))

    desvio = Column(DECIMAL(10,3))
    time = Column(DECIMAL(10,3))
    fator = Column(DECIMAL(10,3))

    atributos = Column(DECIMAL(10))
    espectro = Column(String(10))
    canal = Column(String(20))

    key_kernel = Column(String(120))

    num_fl = Column(DECIMAL(3))
    num_mcl = Column(DECIMAL(3))
    num_cll = Column(DECIMAL(3))

    fl_fl = Column(DECIMAL(3))
    fl_mcl = Column(DECIMAL(3))
    fl_cll = Column(DECIMAL(3))

    mcl_fl = Column(DECIMAL(3))
    mcl_mcl = Column(DECIMAL(3))
    mcl_cll = Column(DECIMAL(3))

    cll_fl = Column(DECIMAL(3))
    cll_mcl = Column(DECIMAL(3))
    cll_cll = Column(DECIMAL(3))

# Criação das tabelas
metadata.create_all()
