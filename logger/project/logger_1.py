# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QApplication,
                             QAction, QWidget)
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)
        self.tabWidget = QtWidgets.QTabWidget()
        count = self.tabWidget.count()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MyWindow()
    win.resize(840, 680)
    win.show()
    sys.exit(app.exec_())
