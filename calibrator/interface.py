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



        stack_size_y = int(y / 35)
        stack_size_x = int(x / 75)

        stack_size_yy = int(y/1.35)
        stack_size_xx = int(x / 2.65)

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralWidget")
        self.vbox = QVBoxLayout()
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.stackedWidget.setGeometry(QtCore.QRect(0, 68, stack_size_yy, stack_size_xx))
        self.stackedWidget.setObjectName("stackedWidget")

        print(stack_size_x,stack_size_y,stack_size_yy,stack_size_xx)
        # self.centralwidget.setGeometry(800,800,800,800)
        # self.centralwidget.setGeometry(0,0,768,50)

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
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor(220, 254, 225))
        self.setPalette(pal)

        # Кнопки Уставки и Калибровки
        buttonUst = QToolButton()
        buttonUst.setText('Уставки')
        buttonCalibr = QToolButton()
        buttonCalibr.setText('Калибровки')
        buttonPar = QToolButton()
        buttonPar.setText('Параметры')
        # buttonAction1.clicked.connect()
        # buttonAction2.clicked.connect()
        buttonUst.setFont(font)
        buttonCalibr.setFont(font)
        buttonPar.setFont(font)
        buttonUst.setMaximumSize(QtCore.QSize(267, 50))
        buttonCalibr.setMaximumSize(QtCore.QSize(267, 50))
        buttonPar.setMaximumSize(QtCore.QSize(267, 50))
        buttonUst.setObjectName("buttonUst")
        buttonCalibr.setObjectName("buttonCalibr")
        buttonPar.setObjectName("buttonPar")
        buttonUst.setStyleSheet('background-color:rgb(153,173,232);')
        buttonCalibr.setStyleSheet('background-color:rgb(153,173,232);')
        buttonPar.setStyleSheet('background-color:rgb(153,173,232);')

        # Кнопки вкладки
        buttonUnit1 = QToolButton()
        buttonUnit1.setText('БУ400')
        buttonUnit2 = QToolButton()
        buttonUnit2.setText('БУ50')
        buttonUnit3 = QToolButton()
        buttonUnit3.setText('БУСЭС')
        buttonUnit1.clicked.connect(self.UnitWidget)
        buttonUnit2.clicked.connect(self.UnitWidget2)
        buttonUnit3.clicked.connect(self.UnitWidget3)
        buttonUnit1.setFont(font)
        buttonUnit2.setFont(font)
        buttonUnit3.setFont(font)
        buttonUnit1.setStyleSheet('background-color:rgb(153,173,232);')
        buttonUnit2.setStyleSheet('background-color:rgb(153,173,232);')
        buttonUnit3.setStyleSheet('background-color:rgb(153,173,232);')
        # buttonUnit1.setGeometry(100,100,100,100)
        # buttonUnit2.setGeometry(100,100,100,100)

        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(buttonUnit1.sizePolicy().hasHeightForWidth())
        # buttonUnit1.setSizePolicy(sizePolicy)
        # buttonUnit2.setSizePolicy(sizePolicy)
        # buttonUnit3.setSizePolicy(sizePolicy)
        buttonUnit1.setMaximumSize(QtCore.QSize(270, 50))
        buttonUnit2.setMaximumSize(QtCore.QSize(270, 50))
        buttonUnit3.setMaximumSize(QtCore.QSize(270, 50))
        buttonUnit1.setObjectName("buttonUnit1")
        buttonUnit2.setObjectName("buttonUnit2")
        buttonUnit3.setObjectName("buttonUnit3")
        # buttonUnit1.setToolTip("")
        # buttonUnit2.setToolTip("")
        # buttonUnit3.setToolTip("")
        # buttonUnit1.setLayoutDirection(QtCore.Qt.RightToLeft)
        # buttonUnit2.setLayoutDirection(QtCore.Qt.RightToLeft)
        # buttonUnit3.setLayoutDirection(QtCore.Qt.RightToLeft)
        # buttonUnit1.setAutoFillBackground(False)
        # buttonUnit2.setAutoFillBackground(False)
        # buttonUnit3.setAutoFillBackground(False)
        # buttonUnit1.setInputMethodHints(QtCore.Qt.ImhNone)
        # buttonUnit2.setInputMethodHints(QtCore.Qt.ImhNone)
        # buttonUnit3.setInputMethodHints(QtCore.Qt.ImhNone)
        # buttonUnit1.setAutoRepeat(False)
        # buttonUnit2.setAutoRepeat(False)
        # buttonUnit3.setAutoRepeat(False)
        # buttonUnit1.setAutoExclusive(False)
        # buttonUnit2.setAutoExclusive(False)
        # buttonUnit3.setAutoExclusive(False)
        # buttonUnit1.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        # buttonUnit2.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        # buttonUnit3.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        # buttonUnit1.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        # buttonUnit2.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        # buttonUnit3.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        # buttonUnit1.setGeometry(100,200,300,400)
        # buttonUnit2.setGeometry(200,100,200,300)

        # Кнопки действия
        buttonAction1 = QToolButton()
        buttonAction1.setText('Считать')
        buttonAction2 = QToolButton()
        buttonAction2.setText('Записать')
        buttonAction3 = QToolButton()
        buttonAction3.setText('Сохранить')
        # buttonAction1.clicked.connect()
        # buttonAction2.clicked.connect()
        # buttonAction3.clicked.connect()
        buttonAction1.setFont(font)
        buttonAction2.setFont(font)
        buttonAction3.setFont(font)
        buttonAction1.setMaximumSize(QtCore.QSize(270, 50))
        buttonAction2.setMaximumSize(QtCore.QSize(270, 50))
        buttonAction3.setMaximumSize(QtCore.QSize(270, 50))
        buttonAction1.setObjectName("buttonAction1")
        buttonAction2.setObjectName("buttonAction2")
        buttonAction3.setObjectName("buttonAction3")
        buttonAction1.setStyleSheet('background-color:rgb(255,240,157);')
        buttonAction2.setStyleSheet('background-color:rgb(255,240,157);')
        buttonAction3.setStyleSheet('background-color:rgb(255,240,157);')


        # self.mainWidget = QWidget(self.centralwidget)
        # self.mainWidget.setGeometry(QtCore.QRect(20, 100, 711, 122))
        # self.mainWidget.setObjectName("mainWidget")
        self.vbox.setContentsMargins(0,0,0, 0)
        self.vbox.setSpacing(0)
        # self.vbox.setGeometry(QtCore.QRect(250,330,200,100))

        self.ustcalLayout = QHBoxLayout()
        # self.actionLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.ustcalLayout.setContentsMargins(0, 0, 0, 0)
        self.ustcalLayout.setSpacing(0)
        self.ustcalLayout.setObjectName("ustcalLayout")
        self.ustcalLayout.addWidget(buttonUst)
        self.ustcalLayout.addWidget(buttonCalibr)
        self.ustcalLayout.addWidget(buttonPar)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.mainLayout.setContentsMargins(0, 0, 0, 10)
        # self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.addWidget(buttonUnit1)
        self.mainLayout.addWidget(buttonUnit2)
        self.mainLayout.addWidget(buttonUnit3)
        # self.mainWidget.setGeometry(0,0,800,50)
        # self.mainLayout.setGeometry(QtCore.QRect(250,330,200,100))

        self.stackLayout = QHBoxLayout()
        self.stackLayout.addWidget(self.stackedWidget)
        self.stackLayout.setContentsMargins(0, 0, 0, 25)

        self.actionLayout = QHBoxLayout()
        # self.actionLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.actionLayout.setContentsMargins(0, 0, 0, 0)
        self.actionLayout.setSpacing(0)
        self.actionLayout.setObjectName("actionLayout")
        self.actionLayout.addWidget(buttonAction1)
        self.actionLayout.addWidget(buttonAction2)
        self.actionLayout.addWidget(buttonAction3)

        self.vbox.addLayout(self.ustcalLayout)
        self.vbox.addLayout(self.mainLayout)
        self.vbox.addLayout(self.stackLayout)
        self.vbox.addLayout(self.actionLayout)

        # Main()
        self.main = Unit().initUI(self.vbox)
        self.stackedWidget.addWidget(self.main)
        self.stackedWidget.addWidget(Unit2())
        self.stackedWidget.addWidget(Unit2())
        # self.vbox.addWidget(self.stackedWidget)


        self.centralwidget.setLayout(self.vbox)
        # self.centralwidget.setLayout(self.actionLayout)

        self.setCentralWidget(self.centralwidget)

        # self.setCentralWidget(self.centralwidget)
        self.setObjectName("MainWindow")
        self.setWindowTitle('Calibrator')
        self.show()


    def UnitWidget(self):
        self.stackedWidget.setCurrentIndex(0)

    def UnitWidget2(self):
        self.stackedWidget.setCurrentIndex(1)

    def UnitWidget3(self):
        self.stackedWidget.setCurrentIndex(2)


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
