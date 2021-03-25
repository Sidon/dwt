# -*- coding: utf-8 -*-

##
# Converte imagens rgb para grayscale
# Por Sidon 2014
###

from qtutil import *
import cv2
import os
from PyQt4 import QtGui as qtg
import sys

window = 'splitrgb.ui'

if __name__!='__main__':
    window = 'etc/togray.ui'

(Ui_MainWindow, QMainWindow) = uic.loadUiType(window)

class tograywindow(QMainWindow):

    """MainWindow inherits QMainWindow"""

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect(self.ui.btExecutar, SIGNAL('clicked()'), SLOT('converter()'))
        self.connect(self.ui.btImagens, SIGNAL('clicked()'), SLOT('select_images()'))
        self.connect(self.ui.btResultPath, SIGNAL('clicked()'), SLOT('result_path()'))
        self.connect(self.ui.btEncerrar, SIGNAL('clicked()'), SLOT('encerrar()'))
        #

    def __del__(self):
        self.ui = None

    @pyqtSlot()
    def converter(self):

        self.buildimages(str(self.ui.leMainPath.text()), 'CLL/', str(self.ui.leResultPath.text()))
        self.buildimages(str(self.ui.leMainPath.text()), 'FL/', str(self.ui.leResultPath.text()))
        self.buildimages(str(self.ui.leMainPath.text()), 'MCL/', str(self.ui.leResultPath.text()))

        print('Ok!')
        return


    def buildimages(self, main_path, subpath, resultpath ):
        number = 0
        print((main_path+subpath))

        for img in os.listdir(main_path+subpath):
            number+=1
            print(('Salvando: ' + resultpath+subpath+str(number).zfill(3)+'_'+subpath[:-1]+'_'+'GRAY_'+img[:-4]+'.png'))
            image = cv2.imread(main_path+subpath+img, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            cv2.imwrite(resultpath+subpath+str(number).zfill(3)+'_'+subpath[:-1]+'_'+'GRAY_'+img[:-4]+'.png', image)
        return
        

    @pyqtSlot()
    def select_images(self):
        self.main_path = str(qtg.QFileDialog.getExistingDirectory(self, "Selecione o diretorio de imagens de entrada"))
        self.ui.leMainPath.setText(self.main_path)

    @pyqtSlot()
    def result_path(self):
        self.main_path = str(qtg.QFileDialog.getExistingDirectory(self, "Selecione o diretorio para as imagens de saida"))
        self.ui.leResultPath.setText(self.main_path)


    @pyqtSlot()
    def encerrar(self):
        self.close()

if __name__ == '__main__':

    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('Wavelets Sidon 2014')

    # create widget
    w = rgb2hsvwindow()
    w.setWindowTitle('UFABC Posinfo 2014 :: Lymphoms :: ToGray :: Sidon')
    w.show()

    # connection
    QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    sys.exit(app.exec_())
