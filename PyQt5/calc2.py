# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
class Main(object):
    def setup(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(386,378)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_result = QtWidgets.QLabel(self.centralwidget)
        self.label_result.setGeometry(QtCore.QRect(0, 0, 391, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_result.setFont(font)
        self.label_result.setStyleSheet("background-color: rgb(176, 176, 176);\n"
                                        "color: rgb(255, 255, 255);")

        self.label_result.setObjectName("label_result")
        self.btn_zero = QtWidgets.QPushButton(self.centralwidget)
        self.btn_zero.setGeometry(QtCore.QRect(0, 300, 150, 80))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.btn_zero.setFont(font)
        self.btn_zero.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.btn_zero.setObjectName("btn_zero")
        self.btn_equal = QtWidgets.QPushButton(self.centralwidget)
        self.btn_equal.setGeometry(QtCore.QRect(150, 300, 150, 80))

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslate(MainWindow)



    def retranslate(self,MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Калькулятор"))
        self.label_result.setText(_translate("MainWindow", ""))
        self.btn_zero.setText(_translate("MainWindow", "0"))
        self.btn_equal.setText(_translate("MainWindow", "="))
        # self.btn_1.setText(_translate("MainWindow", "1"))
        # self.btn_2.setText(_translate("MainWindow", "2"))
        # self.btn_3.setText(_translate("MainWindow", "3"))
        # self.btn_5.setText(_translate("MainWindow", "5"))
        # self.btn_4.setText(_translate("MainWindow", "4"))
        # self.btn_6.setText(_translate("MainWindow", "6"))
        # self.btn_8.setText(_translate("MainWindow", "8"))
        # self.btn_7.setText(_translate("MainWindow", "7"))
        # self.btn_9.setText(_translate("MainWindow", "9"))
        # self.btn_plus.setText(_translate("MainWindow", "+"))
        # self.btn_minus.setText(_translate("MainWindow", "-"))
        # self.btn_mult.setText(_translate("MainWindow", "*"))
        # self.btn_divide.setText(_translate("MainWindow", "/"))





if __name__ == "__main__":
   app =QtWidgets.QApplication(sys.argv)
   MainWindow = QtWidgets.QMainWindow()
   ui = Main()
   ui.setup(MainWindow)
   MainWindow.show()
   sys.exit(app.exec_())