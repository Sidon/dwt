# -*- coding: utf-8 -*-
# import PyQt4 QtCore and QtGui modules
from PyQt4 import uic

from PyQt4.QtCore import *
from PyQt4.QtGui import *


from database import ct_datasets as ctds
from clfs.applyclf import *


window = 'incluiex.ui'
if __name__!='__main__':
    window = 'experimentos/incluiex.ui'


(Ui_MainWindow, QMainWindow) = uic.loadUiType(window)

class InclusaoExperimento(QMainWindow):

    datasets = ctds.getAllDatasets()
    list_idsds = []
    experimento = {'experimento_id' : '', 'id_dataset' : '', 'kernel' : ''}
    idnum=id_dataset=None

    for ds in datasets:
        list_idsds.append(ds.id_dataset)

    def __init__(self, parent=None, idnum=None, id_dataset=None):
        QMainWindow.__init__(self, parent)


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect(self.ui.btExecutar, SIGNAL('clicked()'), SLOT('executar()'))
        self.connect(self.ui.btIncluir, SIGNAL('clicked()'), SLOT('save_to_database()'))
        self.connect(self.ui.tbDesc, SIGNAL('clicked()'), SLOT('monta_descricao()'))
        self.connect(self.ui.tbOutput, SIGNAL('clicked()'), SLOT('select_output()'))

        clfs = getclfs()
        self.ui.cbClassificador.clear()
        self.ui.cbClassificador.addItems(clfs)

        funcs = getfunctions()
        self.ui.cbFuncao.clear()
        self.ui.cbFuncao.addItems(funcs)

        self.ui.cbDataset.addItems(self.list_idsds)

        if idnum!=None:
            self.idnum = idnum
            self.id_dataset = id_dataset
            self.set_edit()

    @pyqtSlot()
    def executar(self):
        print('ok')


    @pyqtSlot()
    def select_output(self):
        self.result_path = str(QFileDialog.getExistingDirectory(self, "Selecione o diretorio para os resultados"))
        self.ui.leFileResult.setText(self.result_path)

    @pyqtSlot()
    def save_to_database(self):
        self.set_experimento()
        if self.idnum==None:
            cte.addexp(self.experimento)
        else:
            print((self.experimento))
            cte.edit_experimento(self.experimento, self.idnum)

        self.ui.btIncluir.setEnabled(False)
        return

    @pyqtSlot()
    def monta_descricao(self):

        self.mnt_dict_exp()
        self.experimento['experimento_id'] = self.monta_id();
        self.ui.leDescricao.setText(self.experimento['experimento_id'])
        return


    def monta_id(self):

        return str(self.experimento['id_dataset'])+'_'+ str(self.ui.cbDataset.currentText()) + '-' +\
                str(self.ui.cbDetalhe.currentText())+'-'+str(self.ui.cbClassificador.currentText())+'-'+\
                str(self.ui.cbFuncao.currentText())+self.experimento['kernel']+'-'+str(self.ui.cbSeletor.currentText())+'-'+\
                self.ui.leFolds.text()


    def mnt_dict_exp(self):
        self.experimento['id_dataset'] = (self.datasets[self.ui.cbDataset.currentIndex()]).id
        self.experimento['experimento_id'] = str(self.monta_id())
        self.experimento['descricao'] = str(self.ui.leDescricao.text())
        self.experimento['detalhe'] = str(self.ui.cbDetalhe.currentText())
        self.experimento['classificador'] = str(self.ui.cbClassificador.currentText())
        self.experimento['kernel'] = str(self.ui.cbKernel.currentText())
        self.experimento['seletor'] = str(self.ui.cbSeletor.currentText())
        self.experimento['funcao'] = str(self.ui.cbFuncao.currentText())
        self.experimento['folds'] = str(self.ui.leFolds.text())
        self.experimento['select'] = str(self.ui.leSelect.text())
        self.experimento['file_result'] = str(self.ui.leFileResult.text())


    def set_experimento(self):
        ds = self.datasets[self.ui.cbDataset.currentIndex()]


        '''if self.ui.cbClassificador.currentText()=='svm':
            kernel = '-'+str(self.ui.cbKernel.currentText())
        else:
            kernel = ''

        experimento_id = str(self.monta_id())
        '''

        # Verificar se o experimento ja foi realizado (id_experimento)
        self.mnt_dict_exp()

        return

    def set_edit(self):
        experimentos = cte.searchRecords(self.idnum, filterfield='id')
        self.experimento = cte.exp2dict(experimentos[0])

        index = self.ui.cbDataset.findText(self.id_dataset)
        self.ui.cbDataset.setCurrentIndex(index)

        self.experimento['id_dataset'] = (self.datasets[self.ui.cbDataset.currentIndex()]).id


        self.experimento['experimento_id'] = str(self.ui.leDescricao.text())

        index = self.ui.cbDetalhe.findText(self.experimento['detalhe'])
        self.ui.cbDetalhe.setCurrentIndex(index)

        index = self.ui.cbClassificador.findText(self.experimento['classificador'])
        self.ui.cbClassificador.setCurrentIndex(index)

        index = self.ui.cbFuncao.findText(self.experimento['funcao'])
        self.ui.cbFuncao.setCurrentIndex(index)

        index = self.ui.cbKernel.findText(self.experimento['kernel'])
        self.ui.cbKernel.setCurrentIndex(index)

        index = self.ui.cbSeletor.findText(self.experimento['seletor'])
        self.ui.cbSeletor.setCurrentIndex(index)

        self.ui.leDescricao.setText(self.experimento['descricao'])
        self.ui.leFolds.setText(str(self.experimento['folds']))
        self.ui.leSelect.setText(self.experimento['select'])
        self.ui.leFileResult.setText(self.experimento['file_result'])


if __name__ == '__main__':

    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('Wavelets Sidon 2014')

    # create widget
    w = InclusaoExperimento()
    w.setWindowTitle('UFABC Posinfo 2014 :: Wavelets :: Sidon')
    w.show()

    # connection
    QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    sys.exit(app.exec_())