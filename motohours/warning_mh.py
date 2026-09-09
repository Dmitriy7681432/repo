# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QWidget, QLabel,QMainWindow,QSizePolicy,
                             QComboBox, QApplication,QDesktopWidget)
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
import sys
from PyQt5.QtCore import QAbstractEventDispatcher
from debug_mh import *

class SignalErr():
    def __init__(self,msg,app = False,type ='err'):
        super().__init__()

        if app:
            app = QApplication(sys.argv)

        self.main = QMainWindow()
        self.main.resize(400,60)
        self.widget = QWidget(self.main)

        #Шрифт
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)


        # Цветовой фон
        pal = self.main.palette()
        # Если use 1-й аргумент, то цвет будет пропадать при переходе на др окно
        # pal.setColor(QtGui.QPalette.Window, QtGui.QColor(191, 245, 234))
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor(220, 254, 225))

        self.main.setPalette(pal)

        self.main.setWindowTitle("Предупреждение")
        # self.widget.setGeometry(100, 100, 400, 50)
        self.widget.setGeometry(QtCore.QRect(0, 10, 401, 40))

        self.center()
        self.hbox = QtWidgets.QHBoxLayout(self.widget)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.lbl = QLabel(msg,self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl.sizePolicy().hasHeightForWidth())
        self.lbl.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.lbl.setFont(font)
        if type =='err':
            self.lbl.setStyleSheet('color: rgb(219,18,18);')
        else:
            self.lbl.setStyleSheet('color: rgb(0,206,209);')
        self.lbl.setSizePolicy(sizePolicy)
        self.hbox.addWidget(self.lbl)
        self.main.show()

        if app:
            sys.exit(app.exec_())

    def center(self):
        qr = self.main.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.main.move(qr.topLeft())
