# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QStackedWidget, QToolBar, QToolButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QAction, QMainWindow)

from PyQt5 import QtCore, QtGui, QtWidgets

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        #Шрифт
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        desktop = QtWidgets.QApplication.desktop()
        x = desktop.width();
        y = desktop.height()
        print(x, y)
        x_size_desktop = int(x / 2.4);
        y_size_desktop = int(y / 1.3)

        # Вычисляем размер экрана
        self.resize(x_size_desktop, y_size_desktop)
        # Вывод окна по центру
        x_ = (desktop.width() - self.frameSize().width()) // 2
        y_ = (desktop.height() - self.frameSize().height()) // 2
        self.move(x_, y_)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralWidget")
        self.centralwidget.setGeometry(0,0,800,50)

        # self.mainWidget = QWidget(self.centralwidget)
        self.mainLayout = QHBoxLayout(self.centralwidget)

        # Кнопки вкладки
        buttonUnit1 = QToolButton(self.centralwidget)
        buttonUnit1.setText('Б400')
        buttonUnit2 = QToolButton(self.centralwidget)
        buttonUnit2.setText('БУ50')
        buttonUnit1.setFont(font)
        buttonUnit2.setFont(font)
        buttonUnit1.setGeometry(QtCore.QRect(100,100,100,100))
        buttonUnit2.setGeometry(QtCore.QRect(100,100,100,100))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(buttonUnit1.sizePolicy().hasHeightForWidth())
        buttonUnit1.setSizePolicy(sizePolicy)
        buttonUnit2.setSizePolicy(sizePolicy)
        buttonUnit1.setMaximumSize(QtCore.QSize(750, 300))
        buttonUnit2.setMaximumSize(QtCore.QSize(750, 300))

        self.mainLayout.addWidget(buttonUnit1)
        self.mainLayout.addWidget(buttonUnit2)
        # self.mainWidget.setGeometry(0,-30,150,100)
        # self.mainLayout.setGeometry(QtCore.QRect(100,300,300,300))

        self.setObjectName("MainWindow")
        self.setWindowTitle('Calibrator')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Main()
    sys.exit(app.exec_())
