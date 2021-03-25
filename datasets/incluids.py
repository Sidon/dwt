# -*- coding: utf-8 -*-
import platform
import sys
from PyQt4 import uic
from PyQt4 import QtGui as qtg

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import database.ct_datasets as ct
from datasets.build import build_dataset2 as dsb
import utils


if __name__!='__main__':
    window = 'datasets/incluids.ui'

(Ui_MainWindow, QMainWindow) = uic.loadUiType(window)
conf = utils.getconfig('')

class InclusaoWindow(QMainWindow):

    """MainWindow inherits QMainWindow"""

    dataset = None
    idnum = None
    slash_os = '/'
    operacao = 0
    if platform.system() == 'Windows':
        slash_os = '\\'


    def __init__(self, parent=None, idnum=None):

        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        self.ui.leMainPath.setText(conf['img_path'])
        self.ui.leClasse0.setText(conf['classe0'])
        self.ui.leClasse1.setText(conf['classe1'])
        self.ui.leClasse2.setText(conf['classe2'])

        self.ui.leRedutor1.setText(conf['redutor1'])
        self.ui.leRedutor1.setText(conf['redutor2'])


        self.connect(self.ui.btImagens, SIGNAL('clicked()'), SLOT('select_images()'))
        self.connect(self.ui.btPathSubbanda, SIGNAL('clicked()'), SLOT('select_file_subband()'))
        self.connect(self.ui.btPathResult, SIGNAL('clicked()'), SLOT('select_file_result()'))

        self.connect(self.ui.btSalvar, SIGNAL('clicked()'), SLOT('save_to_database()'))

        #self.connect(self.ui.btExecutar, SIGNAL('clicked()'), SLOT('executar()'))

        self.connect(self.ui.btEncerrar, SIGNAL('clicked()'), SLOT('encerrar()'))
        self.connect(self.ui.btMakePath, SIGNAL('clicked()'), SLOT('make_path()'))
        self.connect(self.ui.btId, SIGNAL('clicked()'), SLOT('monta_id()'))

        if idnum!=None:
            self.idnum = idnum
            self.operacao = 1
            self.set_edit()

    def __del__(self):
        self.ui = None

    @pyqtSlot()
    def select_images(self):
        self.main_path = str(qtg.QFileDialog.getExistingDirectory(self, "Selecione o diretorio de imagens de entrada"))
        self.ui.leMainPath.setText(self.main_path)

    @pyqtSlot()
    def select_file_subband(self):
        self.main_path = str(qtg.QFileDialog.getExistingDirectory(self, "Selecione o diretorio para as imagens subbanda "))
        self.ui.leResultFile.setText(self.main_path)


    @pyqtSlot()
    def select_file_result(self):
        self.main_path = str(qtg.QFileDialog.getExistingDirectory(self, "Selecione o diretorio para o arquivo de resultados"))
        self.ui.leResultFile.setText(self.main_path)


    @pyqtSlot()
    def monta_id(self):
        self.ui.leIdDataset.setText(self.ui.cbWave.currentText()+'x'+self.ui.cbWave2.currentText()+'_'+
                                    self.ui.cbWMae.currentText()+
                                    '_'+self.ui.cbN1.currentText()+'_'+self.ui.cbN2.currentText()+'_70')
        return



    @pyqtSlot()
    def make_h5(self):
        path =  conf['file_hd5']+self.ui.cbEspectro.currentText()+'_'+self.ui.cbCanal.currentText()+'.h5'
        self.ui.leResultFile.setText(str(path).lower())
        return


    @pyqtSlot()
    def make_path(self):

        path = conf['img_path']+self.ui.cbEspectro.currentText()+'/'+self.ui.cbCanal.currentText()+'/'

        self.ui.leMainPath.setText(str(path).lower())
        self.monta_id()
        self.make_h5()
        return


    @pyqtSlot()
    def save_to_database(self):
        self.set_dataset()
        if self.idnum==None:
            ct.addDataset(self.dataset)
        else:
            ct.editDataset(self.idnum, self.dataset)
        # self.statusBar().showMessage("Registro gravado", 5000)
        # self.ui.btSalvar.setEnabled(False)
        print ("Registro gravado")
        return


    def set_dataset(self):

        if self.dataset==None:
            self.dataset = {}

        self.dataset['id_dataset'] = str(self.ui.leIdDataset.text())


        self.dataset['descricao'] = str(self.ui.leDescricao.text())
        self.dataset['main_path'] = str(self.ui.leMainPath.text())

        self.dataset['espectro'] = str(self.ui.cbEspectro.currentText())
        self.dataset['canal'] = str(self.ui.cbCanal.currentText())

        self.dataset['wavelet1'] = str(self.ui.cbWave.currentText())
        self.dataset['wavelet2'] = str(self.ui.cbWave2.currentText())

        self.dataset['wmae'] = str(self.ui.cbWMae.currentText())
        self.dataset['nivel'] = str(self.ui.cbN1.currentText())
        self.dataset['file_hdf'] = str(self.ui.leSubbandFile.text())

        self.dataset['file_hdf_result'] = str(self.ui.leResultFile.text())

        self.dataset['target0'] = str(self.ui.leClasse0.text())
        self.dataset['target1'] = str(self.ui.leClasse1.text())
        self.dataset['target2'] = str(self.ui.leClasse2.text())

        # Redutores
        self.dataset['redutor1'] = str(self.ui.leRedutor1.text())
        self.dataset['redutor2'] = str(self.ui.leRedutor2.text())

        self.dataset['fredutor1'] = 'S'
        self.dataset['fredutor2'] = 'S'

        self.dataset['dataset'] = ''
        self.dataset['detalhes'] = ''


        # Chave para o arquivo hdf de subbanda
        self.dataset['key'] = str(self.ui.leIdDataset.text())


        return


    def set_edit(self):
        ds = ct.searchRecords(self.idnum)

        self.dataset = ct.dataset2dict(ds[0])

        self.ui.leIdDataset.setText(self.dataset['id_dataset'])
        self.ui.leDescricao.setText(self.dataset['descricao'])
        self.ui.leMainPath.setText(self.dataset['main_path'])

        index = self.ui.cbEspectro.findText(self.dataset['espectro'])
        self.ui.cbEspectro.setCurrentIndex(index)
        index = self.ui.cbCanal.findText(self.dataset['canal'])
        self.ui.cbCanal.setCurrentIndex(index)

        index = self.ui.cbWave.findText(self.dataset['wavelet1'])
        self.ui.cbWave.setCurrentIndex(index)
        index = self.ui.cbWave2.findText(self.dataset['wavelet2'])
        self.ui.cbWave2.setCurrentIndex(index)

        index = self.ui.cbWMae.findText(self.dataset['wmae'])
        self.ui.cbWMae.setCurrentIndex(index)

        index = self.ui.cbN1.findText(self.dataset['nivel'])
        self.ui.cbN1.setCurrentIndex(index)

        self.ui.leSubbandFile.setText(self.dataset['file_hdf'])
        self.ui.leResultFile.setText(self.dataset['file_hdf_result'])


        self.ui.leClasse0.setText(self.dataset['target0'])
        self.ui.leClasse1.setText(self.dataset['target1'])
        self.ui.leClasse2.setText(self.dataset['target2'])

        # Chave para o arquivo hdf
        self.ui.leIdDataset.setText(self.dataset['id_dataset'])

        # Redutores
        self.ui.leRedutor1.setText(self.dataset['redutor1'])
        self.ui.leRedutor2.setText(self.dataset['redutor2'])




        return


    @pyqtSlot()
    def encerrar(self):
        self.close()


if __name__ == '__main__':

    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('Wavelets Sidon 2014')

    # create widget
    w = InclusaoWindow()
    w.setWindowTitle('UFABC Posinfo 2014 :: Wavelets :: Datasets [Inclusao/Edicao]  :: Sidon')
    w.show()

    # connection
    QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    sys.exit(app.exec_())