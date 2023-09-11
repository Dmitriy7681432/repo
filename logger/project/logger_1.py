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
        self.count = self.tabWidget.count()  # Количество вкладок
        self.com_port = QtWidgets.QComboBox(self.centralwidget) # Раскрывающийся список
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(25)
        self.label_com = QtWidgets.QLabel(self.centralwidget) # Надпись
        self.label_com.setText("Выбор com_port")
        self.label_com.setGeometry(QtCore.QRect(0, 0, 700, 31))
        self.label_com.setFont(font)
        self.label_com.move(220,320)
        # self.label_com.setStyleSheet("background-color: rgb(176, 176, 176);\n") # Фон
        self.label_com.setObjectName("label_com")

        self.vbox1 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.vbox1.addWidget(self.label_com)
        self.vbox1.addWidget(self.com_port)
        self.vbox1.setContentsMargins(0,100,0,0)
        self.com_port.move(200,400)
        self.setLayout(self.vbox1)

        # grid = QtWidgets.QGridLayout()
        # grid.addLayout(vbox1, 0, 0)
        # self.setLayout(grid)

        self.resize(840,680)
        # self.setWindowTitle("logger")
        self.show()

        # self.retranslateUi(win)
        # QtCore.QMetaObject.connectSlotsByName(win)

    # def retranslateUi(self, win):
    #     _translate = QtCore.QCoreApplication.translate
    #     win.setWindowTitle(_translate("win", "logger"))
    #     self.label_com.setText(_translate("win", "Выбор com_port"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win1 = MyWindow()
    sys.exit(app.exec_())
