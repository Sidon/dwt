__author__ = 'Sidon'

import yaml
import sys
import io
import platform
from PyQt4.QtCore import *
import os.path
import sys


slash_os = '/'
if platform.system() == 'Windows':
    slash_os = '\\'


def getconfig(_path):

    fconf = os.path.dirname(__file__)+'/'+'etc'+'/'+'lymphoma.conf'
    f=open(fconf)
    conf = yaml.load(f)
    f.close()
    return  conf


class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

