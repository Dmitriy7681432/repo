# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QApplication,
                             QAction, QWidget)
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        # self.main = QtWidgets.QMainWindow()
        self.widget = QtWidgets.QWidget()
        self.centralwidget = QtWidgets.QWidget(self.widget)
        self.setCentralWidget(self.widget)
        self.centralwidget.setGeometry(QtCore.QRect(200, 200, 300, 300))

        self.tabWidget = QtWidgets.QTabWidget()
        self.count = self.tabWidget.count()  # Количество вкладок

        self.com_port = QtWidgets.QComboBox(self.centralwidget) # Раскрывающийся список
        self.com_port.setEditable(True)
        self.cb = QtWidgets.QComboBox(self.centralwidget) # Раскрывающийся список

        # self.cb.setGeometry(QtCore.QRect(550, 70, 191, 211))
        self.cb.setEditable(True)

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(25)

        self.label_com = QtWidgets.QLabel(self.centralwidget) # Надпись
        self.label_com.setText("Выбор порта")
        # self.label_com.setGeometry(QtCore.QRect(200, 100, 200, 131))
        self.label_com.setFont(font)
        # self.label_com.move(220,320)
        self.label_com.setObjectName("label_com")
        # self.label_com.setStyleSheet("background-color: rgb(176, 176, 176);\n") # Фон

        self.label_cb = QtWidgets.QLabel(self.centralwidget) # Надпись
        self.label_cb.setObjectName("label_cb")
        self.label_cb = QtWidgets.QLabel(self.centralwidget)  # Надпись
        self.label_cb.setText("Выбор изделия")
        # self.label_cb.setGeometry(QtCore.QRect(200, 100, 300, 131))
        self.label_cb.setFont(font)
        # self.label_cb.move(820, 120)
        # self.label_com.setStyleSheet("background-color: rgb(176, 176, 176);\n") # Фон
        self.label_cb.setObjectName("label_cb")

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.label_com)
        self.hbox.addWidget(self.com_port)
        self.hbox.addWidget(self.label_cb)
        self.hbox.addWidget(self.cb)
        # self.hbox.insertSpacing(-250,-250)
        # self.hbox.setContentsMargins(100, 100, 120, 100)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        # self.vbox.insertSpacing(-250,-100)
        self.vbox.setContentsMargins(100, 100, 120, 100)
        self.setLayout(self.vbox)

        self.resize(840,680)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win1 = MyWindow()
    sys.exit(app.exec_())
