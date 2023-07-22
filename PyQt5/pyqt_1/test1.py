# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

import random
class Main(object):

    def setup(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(683,540)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 0, 211, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Тест"))
        self.label.setText(_translate("MainWindow", "Трекер события"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Main()
    ui.setup(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


"""
        self.button1 = QtWidgets.QPushButton("One")
        self.button2 = QtWidgets.QPushButton("Two")
        self.button3 = QtWidgets.QPushButton("Three")
        self.button4 = QtWidgets.QPushButton("Four")
        self.button5 = QtWidgets.QPushButton("Five")
        # self.button5.setGeometry(650,495,239,239)

        self.left_container = QtWidgets.QWidget(self.centralwidget)
        self.left_container.setFixedWidth(130)

        self.layout = QtWidgets.QHBoxLayout(self.left_container)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button4)
        self.layout.addWidget(self.button5)
"""

