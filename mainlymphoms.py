#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Sidon'
# import PyQt4 QtCore and QtGui modules
# import PyQt4 QtCore and QtGui modules
import datasets.incluids as inc
import datasets.browseds as bds
import etc.rgb2hsv as rgb2hsv
import etc.splitrgb as splitrgb
import etc.togray as togray
from qtutil import *
from experimentos.icluiex import *

from clfs.applyclf import *
from clfs.matrix1 import *
from clfs.matrix2 import *
from clfs.clf_full import *
from datasets.build import build_subbandas as dsb
from datasets.build import atribs_subbandas as atsb
from database import ct_datasets
from database import ct_results
from clfs.clf_reduct import *
import clfs.clf_full2 as clf2
import clfs.clf_reduct2 as clfr2

print('carrengando..... ') 
(Ui_MainWindow, QMainWindow) = uic.loadUiType('mainlymphoms2.ui')

print('carregado') 

class MainWindow(QMainWindow):

    '''
    experimentos = cte.getallExperimentos()
    rows_experimentos = []
    for experimento in experimentos:
        rows_experimentos.append([experimento.id_dataset, experimento.experimento_id, experimento.select])
    '''

    datasets = ctds.getAllDatasets()
    rows_datasets = []
    for dataset in datasets:
        rows_datasets.append([dataset.id, dataset.id_dataset, dataset.descricao])


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

        # Datasets
        self.connect(self.ui.btCarregarDataset, SIGNAL('clicked()'), SLOT('carregar_ds()'))
        self.connect(self.ui.btGerarDataset, SIGNAL('clicked()'), SLOT('gerar_ds()'))
        self.connect(self.ui.btEditarDataset, SIGNAL('clicked()'), SLOT('editar_ds()'))
        self.connect(self.ui.actIncluiDataset, SIGNAL("triggered()"), SLOT('incluids()'))

        self.connect(self.ui.btResult1, SIGNAL('clicked()'), SLOT('results2()'))
        self.connect(self.ui.btRH5Full, SIGNAL('clicked()'), SLOT('r_h5_full()'))
        self.connect(self.ui.btRH5Reduct, SIGNAL('clicked()'), SLOT('r_h5_reduct()'))

        self.connect(self.ui.btConfusaof, SIGNAL('clicked()'), SLOT('r_confusao_full()'))
        self.connect(self.ui.btConfusaoa, SIGNAL('clicked()'), SLOT('r_confusao_anova()'))

        # set table model (Dataset)
        header = ['ID', 'Identificacao', 'Descricao']
        self.ui.tbDatasets.setModel(DatasetTableModel(self.rows_datasets, header, self))
        self.ui.tbDatasets.doubleClicked.connect(self.carregar_ds)
        self.ui.tbDatasets.resizeColumnsToContents()



    @pyqtSlot()
    def incluids(self):
        self.child = inc.InclusaoWindow(self)
        self.child.setWindowTitle('UFABC Posinfo 2014 :: Wavelets :: Datasets [Inclusao/Edicao]  :: Sidon')
        self.child.show()
        # self.hide()


    @pyqtSlot()
    def editar_ds(self):
        ds = self.datasets[self.ui.tbDatasets.currentIndex().row()]
        self.child = inc.InclusaoWindow(self, ds.id)
        self.child.setWindowTitle('UFABC Posinfo 2014 :: Wavelets :: Datasets [Inclusao/Edicao]  :: Sidon')
        self.child.show()
        # self.hide()


    @pyqtSlot()
    def gerar_ds(self):
       '''
       self.dataset['path_cll'] = self.dataset['main_path']+'CLL'
       self.dataset['path_fl'] = self.dataset['main_path']+'FL'
       self.dataset['path_mcl'] = self.dataset['main_path']+'MCL'
       '''

       ds =  ct_datasets.dataset2dict(self.datasets[self.ui.tbDatasets.currentIndex().row()])
       dsb.build0(ds)
       # dsb.build0(ds)
       return


    @pyqtSlot()
    def r_h5_full(self):
        ds =  ct_datasets.dataset2dict(self.datasets[self.ui.tbDatasets.currentIndex().row()])
        clf0(ds)
        return

    @pyqtSlot()
    def r_confusao_full(self):
        ds =  ct_datasets.dataset2dict(self.datasets[self.ui.tbDatasets.currentIndex().row()])
        clf2.clf0(ds)
        return

    @pyqtSlot()
    def r_confusao_anova(self):
        ds =  ct_datasets.dataset2dict(self.datasets[self.ui.tbDatasets.currentIndex().row()])
        clfr2.clfr0(ds)
        return

    @pyqtSlot()
    def r_h5_reduct(self):
        ds =  ct_datasets.dataset2dict(self.datasets[self.ui.tbDatasets.currentIndex().row()])
        clfr0(ds)
        return

    @pyqtSlot()
    def calc_atributos(self):
        ds =  ct_datasets.dataset2dict(self.datasets[self.ui.tbDatasets.currentIndex().row()])
        atsb.calc_atr_sb(ds)
        return


    @pyqtSlot()
    def results1(self):
        ds =  ct_datasets.dataset2dict(self.datasets[self.ui.tbDatasets.currentIndex().row()])
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
    def classificar2(self):

        for experimento in self.experimentos:
            pk_dataset = experimento.id_dataset
            ds = ctds.searchRecords(pk_dataset)[0]

            if experimento.select=='S':
                exp = {}
                exp['store'] = ds.file_hdfsem_conf
                exp['key'] = '/'+ds.id_dataset
                exp['clf'] = experimento.classificador
                exp['kernel'] = experimento.kernel
                exp['seletor'] = experimento.seletor
                exp['detalhe'] = experimento.detalhe
                exp['descricao'] = experimento.descricao
                exp['folds'] = experimento.folds_test
                exp['funcao'] = experimento.funcao
                exp['experimento_id'] = experimento.experimento_id
                exp['target0'] = ds.target0.strip()
                exp['target1'] = ds.target1.strip()
                exp['target2'] = ds.target2.strip()
                exp['fresult'] = experimento.file_result


                # apply_exp(exp)
                # gridsearch(exp)


                # exp['detalhe'] = 'Aproximacao'
                # exp['kernel'] = 'poly'
                # exp['fresult'] = 'resultados_28-07_swt2_matrix_70imgs_aproximacao_poly.txt'

                exp['reducao']='Anova'

                calcmatrix2(exp)
                sys.exit(0)


    @pyqtSlot()
    def classificar1(self):

        pk_dataset = self.experimentos[self.ui.tbExperimentos.currentIndex().row()].id_dataset
        ds = ctds.searchRecords(pk_dataset)[0]
        experimento = self.experimentos[self.ui.tbExperimentos.currentIndex().row()]

        exp = {}
        exp['store'] = ds.result_file

        exp['detalhe'] = 'Aproximacao'
        exp['kernel'] = 'poly'
        exp['fresult'] = 'resultados_28-07_swt2_matrix_70imgs_aproximacao_poly.txt'

        exp['descricao'] = experimento.descricao
        exp['folds'] = experimento.folds_test

        apply_exp(exp)

    @pyqtSlot()
    def carregar_experimento(self):

        pk_dataset = self.experimentos[self.ui.tbExperimentos.currentIndex().row()].id_dataset
        ds = ctds.searchRecords(pk_dataset)[0]
        experimento = self.experimentos[self.ui.tbExperimentos.currentIndex().row()]

        self.ui.leDataset.setText(ds.id_dataset)
        self.ui.leIDExperimento.setText(experimento.experimento_id)
        self.ui.leDescricao.setText(experimento.descricao)
        self.ui.leSelect.setText(experimento.select)
        self.ui.leFileResult.setText(experimento.file_result)


    @pyqtSlot()
    def carregar_ds(self):

        ds = self.datasets[self.ui.tbDatasets.currentIndex().row()]
        self.ui.leIDDataset.setText(ds.id_dataset)
        self.ui.leDescricaoDataset.setText(ds.descricao)
        self.ui.leImagens.setText(ds.main_path)
        self.ui.leDatasetOutput.setText(ds.file_hdf)
        self.ui.leResultFile.setText(ds.file_hdf_result)


    @pyqtSlot()
    def results2(self):
        ds =  ct_datasets.dataset2dict(self.datasets[self.ui.tbDatasets.currentIndex().row()])
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
                    for kernel in ['linear']:
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
                        num_fl = 0
                        num_mcl = 0
                        num_cll = 0

                        metricas = (storer[key+kernel+'/metrics2']).as_matrix()
                        cmtotal = (storer[key+kernel+'/cmtotal']).as_matrix()

                        recall = metricas[0].mean()
                        f1 = metricas[1].mean()
                        precision = metricas[2].mean()
                        accuracy = metricas[3].mean()
                        std = metricas[3].std()

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
                        row['fator'] = fator
                        row['key_kernel'] = key+kernel+'/metrics'

                        row['time'] = 0


                        row['num_fl'] = cmtotal[0,0]
                        row['num_mcl'] = cmtotal[1,1]
                        row['num_cll'] = cmtotal[2,2]
                    
                        row['fl_fl'] = cmtotal[0,0]
                        row['fl_mcl'] = cmtotal[0,1]
                        row['fl_cll'] = cmtotal[0,2]
                    
                        row['mcl_fl'] = cmtotal[1,0]
                        row['mcl_mcl'] = cmtotal[1,1]
                        row['mcl_cll'] = cmtotal[1,2]
                    
                        row['cll_fl'] = cmtotal[2,0]
                        row['cll_mcl'] = cmtotal[2,1]
                        row['cll_cll'] = cmtotal[2,2]

                        print(('Salvando: ', key+kernel)) 
                        ct_results.addresult(row)

        print('Operação realizada com sucesso') 
        print('Fechando arquivo') 
        storer.close()
        # exit(0)
        return




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

