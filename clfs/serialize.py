
# -*- coding: utf-8 -*-
__author__ = 'Sidon'
from sklearn.feature_selection import SelectKBest, f_classif
from .utilclf import *
from sklearn.linear_model import SGDClassifier


def save_sgd():

    print('\nObtendo os dados de treino')
    x, y = getdata(exp, agrupado=True)

    print('\nReduzindo os atributos (SKB)')
    skb = SelectKBest(f_classif, k=10000)
    x_skb = skb.fit_transform(x, y)

    clf = SGDClassifier(loss="hinge", penalty="l2")
    clf.fit(x_skb, y)


    return