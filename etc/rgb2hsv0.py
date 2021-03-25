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

    def __del__(self):
        self.ui = None

    @pyqtSlot()
    def converter(self):
        self.buildimages(str(self.ui.leMainPath.text()), 'CLL/')
        self.buildimages(str(self.ui.leMainPath.text()), 'FL/')
        self.buildimages(str(self.ui.leMainPath.text()), 'MCL/')

        print('Ok!')
        return


    def buildimages(self, main_path, subpath):

        for img in os.listdir(main_path+'RGB/'+subpath):
            print(img)

            print((main_path+'RGB/'+subpath+img))

            img_rgb = cv2.imread(main_path+'RGB/'+subpath+img)
            img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)

            mask_blue, img_hsv_blue = self.extract_color_hsv(img_rgb, img_hsv,  np.array([110,50,50]), np.array([130,255,255]) )
            mask_red, img_hsv_red = self.extract_color_hsv(img_rgb,  img_hsv,  np.array([0,50,50]),   np.array([10,255,255]) )

            img_hsv_blue_bw =  cv2.cvtColor(img_hsv_blue, cv2.COLOR_BGR2GRAY)
            img_hsv_red_bw =  cv2.cvtColor(img_hsv_red, cv2.COLOR_BGR2GRAY)

            ''' print 'Gravando: '+ main_path+'HSV/FULL/'+subpath+img[:-4]+'.png'
            cv2.imwrite(main_path+'HSV/FULL/'+subpath+img[:-4]+'.png', img_hsv)
            print('Gravando: '+ main_path+'HSV/BLUE/'+subpath+img[:-4]+'_maskblue.png')
            cv2.imwrite(main_path+'HSV/BLUE/'+subpath+img[:-4]+'_blue.png', img_hsv_blue)
            print('Gravando: '+ main_path+'HSV/RED/'+subpath+img[:-4]+'_maskred.png')
            # cv2.imwrite(main_path+'HSV/RED/'+subpath+img[:-4]+'_maskred.png', mask_red)
            cv2.imwrite(main_path+'HSV/RED/'+subpath+img[:-4]+'_red.png', img_hsv_red)'''

            print(('Gravando: '+ main_path+'HSV/BLUE/'+subpath+img[:-4]+'blue.png'))
            cv2.imwrite(main_path+'HSV/BLUE/'+subpath+img[:-4]+'_blue.png', img_hsv_blue_bw)

            print(('Gravando: '+ main_path+'HSV/RED/'+subpath+img[:-4]+'red.png'))
            cv2.imwrite(main_path+'HSV/RED/'+subpath+img[:-4]+'_red.png', img_hsv_red_bw)


        return
        

    def extract_color_hsv(self, rgb, hsv, low, upper):

        # Criaçao d mascara
        mask = cv2.inRange(hsv, low, upper)

        # Bitwise na mascara
        result = cv2.bitwise_and(rgb, rgb, mask=mask )

        return mask, result


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
