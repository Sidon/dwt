# -*- coding: utf-8 -*-
import platform
import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import database.ct_datasets as ct
from datasets.build import build_dataset2 as dsb, wave2
from utils import *
from qtutil import *


window = 'browseds.ui'
if __name__!='__main__':
    window = 'datasets/browseds.ui'


(Ui_MainWindow, QMainWindow) = uic.loadUiType(window)

class BrowseWindow(QMainWindow):

    """MainWindow inherits QMainWindow"""

    datasets = ct.getAllDatasets()
    rows = []

    for dataset in datasets:
        rows.append([dataset.id_dataset, dataset.descricao])

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect(self.ui.btGerarDataset, SIGNAL('clicked()'), SLOT('gerar_dataset()'))
        # self.connect(self.ui.btClassificar, SIGNAL('clicked()'), SLOT('classificar()'))

        # set table model
        header = ['Identificacao', 'Descricao']
        tablemodel = MyTableModel1(self.rows, header, self)
        self.ui.tbDatasets.setModel(tablemodel)
        self.ui.tbDatasets.resizeColumnsToContents()


    def __del__(self):
        self.ui = None

    @pyqtSlot()
    def gerar_dataset(self):

        print((self.datasets[0]))
        ds = ct.dataset2dict(self.datasets[self.ui.tbDatasets.currentIndex().row()])
        dsb.build0(ds)
        return

    @pyqtSlot()
    def classificar(self):
        exp = {}
        ds = self.datasets[self.ui.tbDatasets.currentIndex().row()]
        exp['store'] = ds.result_file
        exp['key']='/'+ds.id_dataset
        #apply_svm(exp)



if __name__ == '__main__':

    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('Wavelets Sidon 2014')

    # create widget
    w = BrowseWindow()
    w.setWindowTitle('UFABC Posinfo 2014 :: Lymphoms :: Browse Datasets :: Sidon')
    w.show()

    # connection
    QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    sys.exit(app.exec_())