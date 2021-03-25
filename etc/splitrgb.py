# -*- coding: utf-8 -*-
import platform
import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from utils import *
from qtutil import *
import cv2
import os
import numpy as np

window = 'splitrgb.ui'

if __name__!='__main__':
    window = 'etc/splitrgb.ui'

(Ui_MainWindow, QMainWindow) = uic.loadUiType(window)

class splitrgbwindow(QMainWindow):

    """MainWindow inherits QMainWindow"""

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect(self.ui.btExecutar, SIGNAL('clicked()'), SLOT('converter()'))
        self.connect(self.ui.btEncerrar, SIGNAL('clicked()'), SLOT('encerrar()'))


    def __del__(self):
        self.ui = None

    @pyqtSlot()
    def converter(self):
        self.buildimages(str(self.ui.leMainPath.text()), 'CLL/', str(self.ui.leResultPath.text()))
        self.buildimages(str(self.ui.leMainPath.text()), 'FL/', str(self.ui.leResultPath.text()))
        self.buildimages(str(self.ui.leMainPath.text()), 'MCL/', str(self.ui.leResultPath.text()))

        print('Ok!')
        return


    def buildimages(self, main_path, subpath, resultpath):

        number = 0

        for img in os.listdir(main_path+subpath):

            number+=1
            idname = str(number).zfill(3)+'_'+subpath[:-1]+'_'

            image = cv2.imread(main_path+subpath+img)

            # Split nos canais rgb
            channel_b, channel_g, channel_r = image[:,:,0], image[:,:,1], image[:,:,2]

            print(('Gravando Canal Blue: ', resultpath+'blue/'+subpath+str(number).zfill(3)+'_BLU_'+img[:-4]+'.png'))
            cv2.imwrite(resultpath+'blue/'+subpath+idname+'BLU_'+img[:-4]+'.png', channel_b)

            print(('Gravando Canal Green: ', resultpath+'green/'+subpath+str(number).zfill(3)+'_GRN_'+img[:-4]+'.png'))
            cv2.imwrite(resultpath+'green/'+subpath+idname+'GRN_'+img[:-4]+'.png', channel_g)

            print(('Gravando Canal Red: ', resultpath+'red/'+subpath+str(number).zfill(3)+'_RED_'+img[:-4]+'.png'))
            cv2.imwrite(resultpath+'red/'+subpath+idname+'RED_'+img[:-4]+'.png', channel_r)


        return

    @pyqtSlot()
    def encerrar(self):
        self.close()


if __name__ == '__main__':

    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('Wavelets Sidon 2014')

    # create widget
    w = rgb2hsvwindow()
    w.setWindowTitle('UFABC Posinfo 2014 :: Lymphoms :: RGB2HSV :: Sidon')
    w.show()

    # connection
    QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    sys.exit(app.exec_())
