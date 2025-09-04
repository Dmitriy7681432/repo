# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication,QDesktopWidget)
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
import sys
from PyQt5.QtCore import QAbstractEventDispatcher

class SignalErr():
    def __init__(self,app = False):
        super().__init__()

        if app:
            app = QApplication(sys.argv)

        self.widget = QWidget()

        #Шрифт
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)


        # Цветовой фон
        pal = self.widget.palette()
        # Если use 1-й аргумент, то цвет будет пропадать при переходе на др окно
        # pal.setColor(QtGui.QPalette.Window, QtGui.QColor(191, 245, 234))
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor(220, 254, 225))
        self.widget.setPalette(pal)

        self.widget.setWindowTitle("Warning")
        self.widget.setGeometry(100, 100, 300, 50)

        self.center()
        self.lbl = QLabel("Не нашел com_port!!!",self.widget)
        self.lbl.move(50,10)
        self.lbl.setFont(font)
        self.lbl.setStyleSheet('color: red;')
        self.widget.show()

        if app:
            sys.exit(app.exec_())

    def center(self):
        qr = self.widget.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.widget.move(qr.topLeft())
