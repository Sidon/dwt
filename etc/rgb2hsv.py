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

window = 'rgb2hsv.ui'

if __name__!='__main__':
    window = 'etc/rgb2hsv.ui'


(Ui_MainWindow, QMainWindow) = uic.loadUiType(window)

class rgb2hsvwindow(QMainWindow):
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

            img_rgb = cv2.imread(main_path+subpath+img)
            image = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)

            # Split nos canais rgb
            channel_h, channel_s, channel_v = image[:,:,0], image[:,:,1], image[:,:,2]

            print(('Gravando Canal H: ', resultpath+'hue/'+subpath+str(number).zfill(3)+'_H_'+img[:-4]+'.png'))
            cv2.imwrite(resultpath+'hue/'+subpath+idname+'_H_'+img[:-4]+'.png', channel_h)

            print(('Gravando Canal S: ', resultpath+'saturation/'+subpath+str(number).zfill(3)+'_S_'+img[:-4]+'.png'))
            cv2.imwrite(resultpath+'green/'+subpath+idname+'_S_'+img[:-4]+'.png', channel_g)

            print(('Gravando Canal V: ', resultpath+'value/'+subpath+str(number).zfill(3)+'_V_'+img[:-4]+'.png'))
            cv2.imwrite(resultpath+'value/'+subpath+idname+'_V_'+img[:-4]+'.png', channel_r)

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
