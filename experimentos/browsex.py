__author__ = 'admin'
# -*- coding: utf-8 -*-
# import PyQt4 QtCore and QtGui modules
from PyQt4 import uic

from PyQt4.QtGui import *

from database import controller as ctds, ct_experimentos as cte
from utils import *
from clfs.applyclf import *


(Ui_MainWindow, QMainWindow) = uic.loadUiType('browsex.ui')

class ClassificacaoWindow(QMainWindow):

    experimentos = cte.getallExperimentos()
    rows = []

    for experimento in experimentos:
        rows.append([experimento.id_experimento, experimento.descricao, experimento.select])


    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect(self.ui.btClassificar1, SIGNAL('clicked()'), SLOT('classificar1()'))
        self.connect(self.ui.btClassificar2, SIGNAL('clicked()'), SLOT('classificar2()'))
        self.connect(self.ui.btCarregar, SIGNAL('clicked()'), SLOT('carregar_experimento()'))

        self.ui.tbExperimentos.setModel(MyTableModel(self.rows, self))

    @pyqtSlot()
    def classificar1(self):

        pk_dataset = self.experimentos[self.ui.tbExperimentos.currentIndex().row()].id_dataset
        ds = ctds.searchRecords(pk_dataset)[0]
        self.experimento = self.experimentos[self.ui.tbExperimentos.currentIndex().row()]

        exp = {}
        exp['store'] = ds.result_file
        exp['key'] = '/'+ds.id_dataset
        exp['classificador'] = self.experimento.classificador
        exp['detalhe'] = self.experimento.detalhe
        exp['descricao'] = self.experimento.descricao
        exp['folds'] = self.experimento.folds_test

        apply_exp(exp)


    @pyqtSlot()
    def classificar2(self):


        pk_dataset = self.experimentos[self.ui.tbExperimentos.currentIndex().row()].id_dataset
        ds = ctds.searchRecords(pk_dataset)[0]
        self.experimento = self.experimentos[self.ui.tbExperimentos.currentIndex().row()]

        exp = {}
        exp['store'] = ds.result_file
        exp['key'] = '/'+ds.id_dataset
        exp['classificador'] = self.experimento.classificador
        exp['detalhe'] = self.experimento.detalhe
        exp['descricao'] = self.experimento.descricao
        exp['folds'] = self.experimento.folds_test

        apply_exp(exp)



    @pyqtSlot()
    def carregar(self):

        pk_dataset = self.experimentos[self.ui.tbExperimentos.currentIndex().row()].id_dataset
        ds = ctds.searchRecords(pk_dataset)[0]
        self.experimento = self.experimentos[self.ui.tbExperimentos.currentIndex().row()]

        exp = {}
        exp['store'] = ds.result_file
        exp['key'] = '/'+ds.id_dataset
        exp['classificador'] = self.experimento.classificador
        exp['detalhe'] = self.experimento.detalhe
        exp['descricao'] = self.experimento.descricao
        exp['folds'] = self.experimento.folds_test

        self.ui.leDataset = ds.id_dataset
        self.ui.leDescricao = ds.Descricao
        # self.ui.leHDF = ds.

        apply_exp(exp)




if __name__ == '__main__':

    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('Wavelets Sidon 2014')

    # create widget
    w = ClassificacaoWindow()
    w.setWindowTitle('UFABC Posinfo 2014 :: Wavelets :: Classificacao :: Sidon')
    w.show()

    # connection
    QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    sys.exit(app.exec_())

