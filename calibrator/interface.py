# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QStackedWidget, QToolBar, QToolButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QAction, QMainWindow)

from PyQt5 import QtCore, QtGui, QtWidgets
from unit_interface import Unit,Unit2


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

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralWidget")
        # self.centralwidget.setGeometry(300,300,300,300)
        self.centralwidget.setGeometry(0,0,800,50)


        stack_size_y = int(y / 35)
        stack_size_x = int(x / 75)

        stack_size_yy = y
        stack_size_xx = int(x / 1.9)

        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.stackedWidget.setGeometry(QtCore.QRect(stack_size_x, stack_size_y, stack_size_yy, stack_size_xx))
        self.stackedWidget.setObjectName("stackedWidget")

        # Вычисляем размер экрана
        self.resize(x_size_desktop, y_size_desktop)
        # Вывод окна по центру
        x_ = (desktop.width() - self.frameSize().width()) // 2
        y_ = (desktop.height() - self.frameSize().height()) // 2
        self.move(x_, y_)

        # Цветовой фон
        pal = self.palette()
        # Если use 1-й аргумент, то цвет будет пропадать при переходе на др окно
        # pal.setColor(QtGui.QPalette.Window, QtGui.QColor(191, 245, 234))
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor(24, 110, 16))
        self.setPalette(pal)

        # self.mainWidget = QWidget(self.centralwidget)
        self.mainLayout = QHBoxLayout(self.centralwidget)

        # Кнопки вкладки
        buttonUnit1 = QToolButton(self)
        buttonUnit1.setText('БУ400')
        buttonUnit2 = QToolButton(self)
        buttonUnit2.setText('БУ50')
        buttonUnit1.clicked.connect(self.UnitWidget)
        buttonUnit2.clicked.connect(self.UnitWidget2)
        buttonUnit1.setFont(font)
        buttonUnit2.setFont(font)
        # buttonUnit1.setGeometry(100,100,100,100)
        # buttonUnit2.setGeometry(100,100,100,100)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        buttonUnit1.setSizePolicy(sizePolicy)
        buttonUnit2.setSizePolicy(sizePolicy)
        buttonUnit1.setMaximumSize(QtCore.QSize(750, 50))
        buttonUnit2.setMaximumSize(QtCore.QSize(750, 50))
        buttonUnit1.setGeometry(100,200,300,400)
        buttonUnit2.setGeometry(200,100,200,300)


        # Main()
        self.main = Unit().initUI(self)
        self.stackedWidget.addWidget(self.main)
        self.stackedWidget.addWidget(Unit2())

        self.mainLayout.addWidget(buttonUnit1)
        self.mainLayout.addWidget(buttonUnit2)
        # self.mainWidget.setGeometry(0,0,800,50)
        self.mainLayout.setGeometry(QtCore.QRect(50,0,800,300))


        # self.setCentralWidget(self)
        self.setObjectName("MainWindow")
        self.setWindowTitle('Calibrator')
        self.show()


    def UnitWidget(self):
        self.stackedWidget.setCurrentIndex(0)

    def UnitWidget2(self):
        self.stackedWidget.setCurrentIndex(1)


# class Unit(QWidget):
#
#     def __init__(self):
#         super().__init__()
#
#     def initUI(self,centr):
#         # Шрифт
#         font = QtGui.QFont()
#         font.setFamily("Times New Roman")
#         font.setPointSize(14)
#         font.setBold(True)
#         font.setWeight(75)
#
#         self.centralwidget = centr
#         self.centralwidget.setObjectName("centralWidget")
#
#         # Порт
#         self.page = QtWidgets.QWidget()
#         self.page.setObjectName("page")
#         # self.page.setGeometry(QtCore.QRect(300,300,300,300))
#
#         self.horizontWidget = QtWidgets.QWidget(self.page)
#         self.horizontWidget.setGeometry(QtCore.QRect(20, 20, 210, 40))
#         self.horizontWidget.setObjectName("horizontWidget")
#         self.horizontLayout = QtWidgets.QHBoxLayout(self.horizontWidget)
#         self.horizontLayout.setContentsMargins(0, 0, 0, 0)
#         self.horizontLayout.setObjectName("horizontLayout")
#         # self.horizontLayout.addStretch(1)
#         self.horizontLayout.setContentsMargins(0, 0, 0, 0)
#         self.horizontLayout.setObjectName("horizontLayout")
#
#         data_tab =QtWidgets.QTabWidget(self.horizontWidget)
#         data_tab.addTab(QtWidgets.QLabel('Таблица 1'), "Уставки")
#         data_tab.addTab(QtWidgets.QLabel('Таблица 2'), "Калибровки")
#         data_tab.setCurrentIndex(0)
#         self.horizontLayout.addWidget(data_tab)
#         return self.page

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Main()
    sys.exit(app.exec_())
