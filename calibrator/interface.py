# -*- coding: utf-8 -*-
import sys,serial
from PyQt5.QtWidgets import (QWidget, QPushButton, QStackedWidget, QToolBar, QToolButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QAction, QMainWindow)

from PyQt5 import QtCore, QtGui, QtWidgets
from unit_interface import Unit,Unit2
from class_read_data import Connect,Calibrator
from debug import printf


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
        self.buttonUst = QToolButton()
        self.buttonUst.setText('Уставки')
        self.buttonCalibr = QToolButton()
        self.buttonCalibr.setText('Калибровки')
        self.buttonPar = QToolButton()
        self.buttonPar.setText('Параметры')
        self.buttonUst.setFont(font)
        self.buttonCalibr.setFont(font)
        self.buttonPar.setFont(font)
        self.buttonUst.setMaximumSize(QtCore.QSize(267, 50))
        self.buttonCalibr.setMaximumSize(QtCore.QSize(267, 50))
        self.buttonPar.setMaximumSize(QtCore.QSize(267, 50))
        self.buttonUst.setObjectName("buttonUst")
        self.buttonCalibr.setObjectName("buttonCalibr")
        self.buttonPar.setObjectName("buttonPar")
        self.buttonUst.setStyleSheet('background-color:rgb(153,173,232);')
        self.buttonCalibr.setStyleSheet('background-color:rgb(153,173,232);')
        self.buttonPar.setStyleSheet('background-color:rgb(153,173,232);')
        self.buttonUst.setDown(True)
        self.buttonUst.setCheckable(True)
        self.buttonUst.setChecked(False)
        self.buttonUst.clicked.connect(self.UstWidget)
        self.buttonCalibr.setCheckable(True)
        self.buttonCalibr.clicked.connect(self.CalibrWidget)
        self.buttonPar.setCheckable(True)
        self.buttonPar.setChecked(False)
        self.buttonPar.clicked.connect(self.ParWidget)
        # self.buttonCalibr.setCheckable(True)
        # self.buttonPar.setCheckable(True)
        # self.buttonPar.setChecked(False)

        # Кнопки вкладки
        self.buttonUnit1 = QToolButton()
        self.buttonUnit1.setText('БУ400')
        self.buttonUnit2 = QToolButton()
        self.buttonUnit2.setText('БУ50')
        self.buttonUnit3 = QToolButton()
        self.buttonUnit3.setText('БУСЭС')
        self.buttonUnit1.setDown(True)
        self.buttonUnit1.setCheckable(True)
        self.buttonUnit1.setChecked(False)
        self.buttonUnit1.clicked.connect(self.UnitWidget)
        self.buttonUnit2.setCheckable(True)
        self.buttonUnit2.clicked.connect(self.UnitWidget2)
        self.buttonUnit3.setCheckable(True)
        self.buttonUnit3.setChecked(False)
        self.buttonUnit3.clicked.connect(self.UnitWidget3)
        self.buttonUnit1.setFont(font)
        self.buttonUnit2.setFont(font)
        self.buttonUnit3.setFont(font)
        self.buttonUnit1.setStyleSheet('background-color:rgb(153,173,232);')
        self.buttonUnit2.setStyleSheet('background-color:rgb(153,173,232);')
        self.buttonUnit3.setStyleSheet('background-color:rgb(153,173,232);')
        # self.buttonUnit1.setGeometry(100,100,100,100)
        # self.buttonUnit2.setGeometry(100,100,100,100)

        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(buttonUnit1.sizePolicy().hasHeightForWidth())
        # buttonUnit1.setSizePolicy(sizePolicy)
        # buttonUnit2.setSizePolicy(sizePolicy)
        # buttonUnit3.setSizePolicy(sizePolicy)
        self.buttonUnit1.setMaximumSize(QtCore.QSize(270, 50))
        self.buttonUnit2.setMaximumSize(QtCore.QSize(270, 50))
        self.buttonUnit3.setMaximumSize(QtCore.QSize(270, 50))
        self.buttonUnit1.setObjectName("buttonUnit1")
        self.buttonUnit2.setObjectName("buttonUnit2")
        self.buttonUnit3.setObjectName("buttonUnit3")
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
        self.buttonAction1 = QToolButton()
        self.buttonAction1.setText('Считать')
        self.buttonAction2 = QToolButton()
        self.buttonAction2.setText('Записать')
        self.buttonAction3 = QToolButton()
        self.buttonAction3.setText('Сохранить')
        # buttonAction1.clicked.connect()
        # buttonAction2.clicked.connect()
        # buttonAction3.clicked.connect()
        self.buttonAction1.setFont(font)
        self.buttonAction2.setFont(font)
        self.buttonAction3.setFont(font)
        self.buttonAction1.setMaximumSize(QtCore.QSize(270, 50))
        self.buttonAction2.setMaximumSize(QtCore.QSize(270, 50))
        self.buttonAction3.setMaximumSize(QtCore.QSize(270, 50))
        self.buttonAction1.setObjectName("buttonAction1")
        self.buttonAction2.setObjectName("buttonAction2")
        self.buttonAction3.setObjectName("buttonAction3")
        self.buttonAction1.setStyleSheet('background-color:rgb(255,240,157);')
        self.buttonAction2.setStyleSheet('background-color:rgb(255,240,157);')
        self.buttonAction3.setStyleSheet('background-color:rgb(255,240,157);')


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
        self.ustcalLayout.addWidget(self.buttonUst)
        self.ustcalLayout.addWidget(self.buttonCalibr)
        self.ustcalLayout.addWidget(self.buttonPar)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.mainLayout.setContentsMargins(0, 0, 0, 10)
        # self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.addWidget(self.buttonUnit1)
        self.mainLayout.addWidget(self.buttonUnit2)
        self.mainLayout.addWidget(self.buttonUnit3)
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
        self.actionLayout.addWidget(self.buttonAction1)
        self.actionLayout.addWidget(self.buttonAction2)
        self.actionLayout.addWidget(self.buttonAction3)

        self.vbox.addLayout(self.ustcalLayout)
        self.vbox.addLayout(self.mainLayout)
        self.vbox.addLayout(self.stackLayout)
        self.vbox.addLayout(self.actionLayout)

        # Main()
        # self.main = Unit().initUI(self.vbox)
        # self.stackedWidget.addWidget(self.main)

        ser = Connect()
        data_dict_bu400= Calibrator(ser.ser, 'SES200M', 'BU_400')
        data_dict_bu50= Calibrator(ser.ser, 'SES200M', 'BU_50')
        data_dict_buses= Calibrator(ser.ser, 'SES200M', 'BU_SES')

        self.stackedWidget.addWidget(Unit(data_dict_bu400.data_dict,'preset','BU400'))
        self.stackedWidget.addWidget(Unit(data_dict_bu50.data_dict,'preset','BU50'))
        self.stackedWidget.addWidget(Unit(data_dict_buses.data_dict,'preset','BUSES'))
        self.stackedWidget.addWidget(Unit(data_dict_bu400.data_dict,'calibr','BU400'))
        self.stackedWidget.addWidget(Unit(data_dict_bu50.data_dict,'calibr','BU50'))
        self.stackedWidget.addWidget(Unit(data_dict_buses.data_dict,'calibr','BUSES'))
        self.stackedWidget.setCurrentIndex(0)
        # self.vbox.addWidget(self.stackedWidget)


        self.centralwidget.setLayout(self.vbox)
        # self.centralwidget.setLayout(self.actionLayout)

        self.setCentralWidget(self.centralwidget)

        # self.setCentralWidget(self.centralwidget)
        self.setObjectName("MainWindow")
        self.setWindowTitle('Calibrator')
        self.show()


    def UnitWidget(self):
        if self.buttonCalibr.isChecked():
            self.stackedWidget.setCurrentIndex(3)
        else:
            self.stackedWidget.setCurrentIndex(0)
        self.buttonUnit1.setCheckable(True)
        self.buttonUnit2.setChecked(False)
        self.buttonUnit3.setChecked(False)

    def UnitWidget2(self):
        if self.buttonCalibr.isChecked():
            self.stackedWidget.setCurrentIndex(4)
        else:
            self.stackedWidget.setCurrentIndex(1)
        self.buttonUnit2.setCheckable(True)
        self.buttonUnit1.setChecked(False)
        self.buttonUnit3.setChecked(False)
        self.buttonUnit1.setDown(False)

    def UnitWidget3(self):
        if self.buttonCalibr.isChecked():
            self.stackedWidget.setCurrentIndex(5)
        else:
            self.stackedWidget.setCurrentIndex(2)
        self.buttonUnit3.setCheckable(True)
        self.buttonUnit1.setChecked(False)
        self.buttonUnit2.setChecked(False)
        self.buttonUnit1.setDown(False)

    def UstWidget(self):
        if self.buttonUnit1.isChecked():
            self.stackedWidget.setCurrentIndex(0)
        if self.buttonUnit2.isChecked():
            self.stackedWidget.setCurrentIndex(1)
        if self.buttonUnit3.isChecked():
            self.stackedWidget.setCurrentIndex(2)
        self.buttonUst.setCheckable(True)
        self.buttonCalibr.setChecked(False)
        self.buttonPar.setChecked(False)

    def CalibrWidget(self):
        if self.buttonUnit1.isChecked():
            self.stackedWidget.setCurrentIndex(3)
        if self.buttonUnit2.isChecked():
            self.stackedWidget.setCurrentIndex(4)
        if self.buttonUnit3.isChecked():
            self.stackedWidget.setCurrentIndex(5)
        self.buttonCalibr.setCheckable(True)
        self.buttonUst.setChecked(False)
        self.buttonPar.setChecked(False)
        self.buttonUst.setDown(False)

    def ParWidget(self):
        # self.stackedWidget.setCurrentIndex(2)
        self.buttonPar.setCheckable(True)
        self.buttonUst.setChecked(False)
        self.buttonCalibr.setChecked(False)
        self.buttonUst.setDown(False)


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
