__author__ = 'sidon'

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from utils import *


class MyTableModel1(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])


    def data(self, index, role):
        if not index.isValid():
            return
        # vvvv this is the magic part
        elif role == Qt.BackgroundRole:
            if index.row() % 2 == 0:
                return QColor(60, 63, 65)
            else:
                return QColor(49, 54, 59)
        # ^^^^ this is the magic part
        elif role != Qt.DisplayRole:
            return
        return self.arraydata[index.row()][index.column()]


    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerdata[col]
        return


    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))



class DatasetTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])


    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        # vvvv this is the magic part
        elif role == Qt.BackgroundRole:
            if index.row() % 2 == 0:
                return QColor(60, 63, 65)
            else:
                return QColor(49, 54, 59)
        # ^^^^ this is the magic part
        elif role != Qt.DisplayRole:
            return
        return self.arraydata[index.row()][index.column()]


    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerdata[col]
        return  #QVariant()


    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))

