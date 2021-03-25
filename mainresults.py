#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Sidon'
# import PyQt4 QtCore and QtGui modules
import etc.rgb2hsv as rgb2hsv
import etc.splitrgb as splitrgb
import etc.togray as togray
from qtutil import *


from clfs.matrix2 import *
from clfs.clf_full import *
from datasets.build import build_subbandas as dsb
from datasets.build import atribs_subbandas as atsb
from database import ct_datasets
from database import ct_results as ctr
from clfs.clf_reduct import *
from PyQt4 import QtGui, QtCore

(Ui_MainWindow, QMainWindow) = uic.loadUiType('mainresults.ui')

class MainWindow(QMainWindow):

    '''
    experimentos = cte.getallExperimentos()
    rows_experimentos = []
    for experimento in experimentos:
        rows_experimentos.append([experimento.id_dataset, experimento.experimento_id, experimento.select])
    '''

    results = ctr.getallresults()
    rows_datasets = []
    for result in results:
        rows_datasets.append([result.id, result.wavelet, result.wavemae, result.subbanda, result.fator,
                             results.espectro, result.canal, result.atributos])

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect(self.ui.actBrowseds, SIGNAL("triggered()"), SLOT('browseds()'))
        self.connect(self.ui.actIncluiExp, SIGNAL("triggered()"), SLOT('inclui_exp()'))
        self.connect(self.ui.actrgb2hsv, SIGNAL("triggered()"), SLOT('rgb2hsv()'))
        self.connect(self.ui.actSplitRGB, SIGNAL("triggered()"), SLOT('split_rgb()'))
        self.connect(self.ui.actToGray, SIGNAL("triggered()"), SLOT('to_gray()'))
        self.connect(self.ui.actCalcAtributos, SIGNAL("triggered()"), SLOT('calc_atributos()'))

        self.connect(self.ui.btfiltrar, SIGNAL('clicked()'), SLOT('filtrar()'))

        # Datasets

        # set table model (Dataset)
        header = ['ID', 'Wavelet', 'Wavelet Mãe', 'Subbanda', 'Indice', 'Espectro', 'Canal', 'Atributos']
        self.ui.tbResults.setModel(DatasetTableModel(self.rows_datasets, header, self))
        self.ui.tbResults.doubleClicked.connect(self.carregar_ds)
        self.ui.tbResults.resizeColumnsToContents()


    @pyqtSlot()
    def filtrar(self):

        waves = []
        for checkbox in  self.ui.gbwave.findChildren(QtGui.QCheckBox):
            if checkbox.isChecked():
                waves.append(checkbox.text())

        wmaes = []
        for checkbox in  self.ui.gbwmae.findChildren(QtGui.QCheckBox):
            if checkbox.isChecked():
                wmaes.append(checkbox.text())

        subbandas = []
        for checkbox in  self.ui.gbsubbanda.findChildren(QtGui.QCheckBox):
            if checkbox.isChecked():
                subbandas.append(checkbox.text())

        deltas = []
        for checkbox in  self.ui.gbdelta.findChildren(QtGui.QCheckBox):
            if checkbox.isChecked():
                deltas.append(checkbox.text())

        metricas = []
        for checkbox in self.ui.gbmetrica.findChildren(QtGui.QCheckBox):
            if checkbox.isChecked():
                metricas.append(checkbox.text())



    @pyqtSlot()
    def gerar_ds(self):
       '''
       self.dataset['path_cll'] = self.dataset['main_path']+'CLL'
       self.dataset['path_fl'] = self.dataset['main_path']+'FL'
       self.dataset['path_mcl'] = self.dataset['main_path']+'MCL'
       '''

       ds =  ct_datasets.dataset2dict(self.datasets[self.ui.tbResults.currentIndex().row()])
       dsb.build0(ds)
       # dsb.build0(ds)
       return




    @pyqtSlot()
    def calc_atributos(self):
        ds =  ct_datasets.dataset2dict(self.datasets[self.ui.tbResults.currentIndex().row()])
        atsb.calc_atr_sb(ds)
        return


    @pyqtSlot()
    def results1(self):
        ds =  ct_datasets.dataset2dict(self.datasets[self.ui.tbResults.currentIndex().row()])
        #stores = pd.HDFStore(ds['file_hdf'])
        storer = pd.HDFStore(ds['file_hdf_result'])

        row = {}

        for wavelet in ('DWT2', 'SWT2'):
            key =  ds['id_dataset']+'/'+wavelet+'/Detalhes/Atributos'

            atributos_subbandas = 0
            if wavelet=='DWT2':
                atributos_subbandas = 362095
            elif wavelet=='SWT2':
                atributos_subbandas = 1443520

            atributos_full = (1388*1040)

            for redutor in ('Anova-02', 'Anova-005', 'Anova-05', 'Anova-001', 'Anova-09', 'Full'):
                for subbanda in ('Aproximacao', 'Horizontais', 'Verticais', 'Diagonais'):
                    for kernel in ('poly', 'linear', 'rbf'):
                        key = ds['id_dataset']+'/'+wavelet+'/Resultados/'+redutor+'/'+subbanda+'/'

                        if redutor!='Full':
                            shape = int(((storer[key+'Shape']).tolist())[1])
                            row['atributos'] = shape
                            row['reducao'] = ((shape*1.0)/atributos_subbandas)*100
                            fator = (storer[key+'Fator'])[0]
                        else:
                            row['atributos'] = atributos_full
                            row['reducao'] = 0.0
                            fator = 0.0

                        recall = 0
                        f1 = 0
                        precision = 0
                        accuracy = 0
                        std = 0

                        # scores = (stores[key+kernel+'/scores']).tolist()
                        if (key+kernel+'/metrics') in storer:
                            metricas = (storer[key+kernel+'/metrics']).as_matrix()
                            recall = metricas[0].mean()
                            f1 = metricas[1].mean()
                            precision = metricas[2].mean()
                            accuracy = metricas[3].mean()
                            std = metricas[3].std()


                        if (key+kernel+'/cost_time') in storer:
                            cost_time = (storer[key+kernel+'/cost_time'])[0][4]/60 * -1
                        else:
                            cost_time = 0


                        row['id_dataset'] = ds['id_dataset']
                        row['wavelet'] = wavelet
                        row['wavemae'] = ds['wmae']
                        row['redutor'] = redutor

                        row['subbanda'] = subbanda
                        row['atributos_subbanda'] = atributos_subbandas

                        row['kernel'] = kernel
                        row['espectro'] = ds['espectro']
                        row['canal'] = ds['canal']

                        row['acuracia'] = accuracy
                        row['f1'] = f1
                        row['precisao'] = precision
                        row['recall'] = recall

                        row['desvio'] = std

                        row['time'] = cost_time
                        row['fator'] = fator

                        row['key_kernel'] = key+kernel+'/metrics'

                        print(('Salvando: ', key+kernel))
                        ct_results.addresult(row)


        print('Operação realizada com sucesso')
        print('Fechando arquivo')
        storer.close()
        # exit(0)
        return


    @pyqtSlot()
    def browseds(self):
        self.child = bds.BrowseWindow()
        self.child.setWindowTitle('UFABC Posinfo 2014 :: Lymphoms :: Browse Datasets :: Sidon')
        self.child.show()

    @pyqtSlot()
    def inclui_exp(self):
        self.child = InclusaoExperimento(self)
        self.child.setWindowTitle('UFABC Posinfo 2014 :: Lymphoms :: Inclusao Experimento :: Sidon')
        self.child.show()
        # self.hide()

    @pyqtSlot()
    def editar_ex(self):

        pk_dataset = self.experimentos[self.ui.tbExperimentos.currentIndex().row()].id_dataset

        ex = self.experimentos[self.ui.tbExperimentos.currentIndex().row()]
        print((ctds.searchRecords(pk_dataset)[0].id_dataset))
        self.child = InclusaoExperimento(self, idnum=ex.id, id_dataset=ctds.searchRecords(pk_dataset)[0].id_dataset)

        self.child.setWindowTitle('UFABC Posinfo 2014 :: Wavelets :: Experimentos [Inclusao/Edicao]  :: Sidon')
        self.child.show()
        # self.hide()


    @pyqtSlot()
    def rgb2hsv(self):
        self.child = rgb2hsv.rgb2hsvwindow(self)
        self.child.setWindowTitle('UFABC Posinfo 2014 :: Lymphoms :: Util :: Colortraking :: Sidon')
        self.child.show()
        # self.hide()

    @pyqtSlot()
    def split_rgb(self):
        self.child = splitrgb.splitrgbwindow(self)
        self.child.setWindowTitle('UFABC Posinfo 2014 :: Lymphoms :: Util :: Split RGB :: Sidon')
        self.child.show()
        # self.hide()


    @pyqtSlot()
    def to_gray(self):
        self.child = togray.tograywindow(self)
        self.child.setWindowTitle('UFABC Posinfo 2014 :: Lymphoms :: Util :: To Gray :: Sidon')
        self.child.show()
        # self.hide()


    @pyqtSlot()
    def carregar_ds(self):

        ds = self.datasets[self.ui.tbResults.currentIndex().row()]
        self.ui.leIDDataset.setText(ds.id_dataset)
        self.ui.leDescricaoDataset.setText(ds.descricao)
        self.ui.leImagens.setText(ds.main_path)
        self.ui.leDatasetOutput.setText(ds.file_hdf)
        self.ui.leResultFile.setText(ds.file_hdf_result)

if __name__ == '__main__':

    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('Wavelets Sidon 2014')

    # create widget
    w = MainWindow()
    w.setWindowTitle('UFABC Posinfo 2014 :: Lymphoms :: Main Window :: Sidon')
    w.show()

    # connection
    QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    sys.exit(app.exec_())

