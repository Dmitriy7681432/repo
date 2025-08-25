# -*- coding: utf-8 -*-
import sys,serial,struct
import time

from PyQt5.QtWidgets import (QWidget, QPushButton, QStackedWidget, QToolBar, QToolButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QAction, QMainWindow,QDialog,QLabel,QProgressBar,
                             QDesktopWidget)

from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot,QTimer
from unit_interface import Unit,Param
from class_read_data import Connect,Calibrator
from debug import printf
from PyQt5.QtCore import QBasicTimer
# from debug1.test1 import Testing

class Worker(QThread):
    finished = pyqtSignal()
    window_created = pyqtSignal(QWidget)

    def __init__(self,obj_main):
        super().__init__()
        self.window = None
        self.obj_main = obj_main

    def run1(self):
        # Здесь создается второе окно
        # self.window = QWidget()
        # layout = QVBoxLayout()
        # label = QLabel("Второе окно")
        # layout.addWidget(label)
        # self.window.setLayout(layout)
        # self.window.setWindowTitle("Второе окно")
        # self.window = test_qt1.Example()

        self.window = QWidget()
        self.pbar = QProgressBar(self.window)
        self.pbar.setGeometry(30, 40, 200, 25)

        # self.btn = QPushButton('Начать', self.window)
        # self.btn.move(30, 80)
        # self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0

        layout = QVBoxLayout()
        layout.addWidget(self.pbar)
        # layout.addWidget(self.btn)
        self.window.setLayout(layout)

        self.window.setGeometry(100, 100, 280, 70)
        self.center() # Центрируем окно
        self.window.setWindowTitle('Загрузка')
        # Блокировка главного окна
        self.window.setWindowModality(Qt.Qt.ApplicationModal)
        # Убрать значок закрытия окна
        self.window.setWindowFlags(Qt.Qt.CustomizeWindowHint | Qt.Qt.WindowTitleHint)
        self.window.show()
        self.obj_main.cal_signal.connect(self.update_progress_bar)

        self.doAction()

    def time_stop(self):
        self.val =100

    def update_progress_bar(self,val):
        printf('updata_pr')
        self.val = val
        # self.step = self.step +self.val
        self.pbar.setValue(self.val)

    def center(self):
        qr = self.window.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.window.move(qr.topLeft())


        # self.window_created.emit(self.window)  # Отправляем сигнал о создании окна
        # self.finished.emit()  # Отправляем сигнал об окончании работы
        printf('3')

    # Вновь
    # def closeEvent(self):
    #     self.window.setWindowModality(Qt.Qt.NonModal)
    def timerEvent(self, e):
        printf(self.val, self.timer.isActive())
        self.pbar.setValue(self.val)
        if self.val >= 100:
            self.timer.stop()
            self.window.close()
            self.window.setWindowModality(Qt.Qt.NonModal)
            # self.btn.setText('Закончено')
            return

        # self.step = self.step + self.val
        # self.step = self.step + 1

    def doAction(self):
        printf('doAction', self.timer.isActive())
        if self.timer.isActive():
            self.timer.stop()
            # self.btn.setText('Начать')
        else:
            self.val = 0
            self.timer.start(1000, self)
            # self.btn.setText('Стоп')



class ThreadCalibrator(QtCore.QThread):
    finished2 = pyqtSignal(str)
    mysignal = QtCore.pyqtSignal()

    def __init__(self, obj,name_obj,mode):
        super().__init__()
        self.obj = obj
        self.name_obj = name_obj
        self.mode = mode

    def run(self):
        i = 1
        printf('Thread start')
        self.obj.main_data_read(self.mode)
        # while True:
        # for i in range(0,10):
        #     self.sleep(1)
            # self.mysignal.emit('%s'% i)
        # self.obj.rest()
        self.finished2.emit('%s' % self.name_obj)
        # self.finished2.emit()


class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.main = QMainWindow()
        self.timer = QTimer()

        #Шрифт
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        desktop = QtWidgets.QApplication.desktop()
        x = desktop.width();
        y = desktop.height()
        printf(x, y)
        # x_size_desktop = int(x / 2.2);
        x_size_desktop = 885
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
        printf(self.stackedWidget.size().height())
        self.stackedWidget.setObjectName("stackedWidget")

        printf(stack_size_x,stack_size_y,stack_size_yy,stack_size_xx)
        # self.centralwidget.setGeometry(800,800,800,800)
        # self.centralwidget.setGeometry(0,0,768,50)

        # Вычисляем размер экрана
        self.main.resize(x_size_desktop, y_size_desktop)
        # Вывод окна по центру
        x_ = (desktop.width() - self.main.frameSize().width()) // 2
        y_ = (desktop.height() - self.main.frameSize().height()) // 2
        self.main.move(x_, y_)

        # Цветовой фон
        pal = self.main.palette()
        # Если use 1-й аргумент, то цвет будет пропадать при переходе на др окно
        # pal.setColor(QtGui.QPalette.Window, QtGui.QColor(191, 245, 234))
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor(220, 254, 225))
        self.main.setPalette(pal)

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
        self.buttonUst.setMaximumSize(QtCore.QSize(300, 50))
        self.buttonCalibr.setMaximumSize(QtCore.QSize(300, 50))
        self.buttonPar.setMaximumSize(QtCore.QSize(300, 50))
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
        self.buttonUnit1.setMaximumSize(QtCore.QSize(300, 50))
        self.buttonUnit2.setMaximumSize(QtCore.QSize(300, 50))
        self.buttonUnit3.setMaximumSize(QtCore.QSize(300, 50))
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
        self.buttonAction2.setEnabled(False)
        self.buttonAction3 = QToolButton()
        self.buttonAction3.setText('Сохранить')
        # buttonAction1.clicked.connect()
        # buttonAction2.clicked.connect()
        # buttonAction3.clicked.connect()
        self.buttonAction1.setFont(font)
        self.buttonAction2.setFont(font)
        self.buttonAction3.setFont(font)
        self.buttonAction1.setMaximumSize(QtCore.QSize(300, 50))
        self.buttonAction2.setMaximumSize(QtCore.QSize(300, 50))
        self.buttonAction3.setMaximumSize(QtCore.QSize(300, 50))
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

        self.ser = Connect()
        self.data_dict_bu400= Calibrator(self.ser.ser, 'SES200M', 'BU_400')
        self.data_dict_bu50= Calibrator(self.ser.ser, 'SES200M', 'BU_50')
        self.data_dict_buses= Calibrator(self.ser.ser, 'SES200M', 'BU_SES')
        # self.testing = Testing(self.ser.ser, 'SES200M', 'BU_400')

        self.unit_bu400_preset = Unit(self.data_dict_bu400.data_dict, 'preset', 'BU400',y)
        self.unit_bu50_preset = Unit(self.data_dict_bu50.data_dict, 'preset', 'BU50',y)
        self.unit_buses_preset = Unit(self.data_dict_buses.data_dict, 'preset', 'BUSES',y)
        self.unit_bu400_calibr = Unit(self.data_dict_bu400.data_dict, 'calibr', 'BU400',y)
        self.unit_bu50_calibr = Unit(self.data_dict_bu50.data_dict, 'calibr', 'BU50',y)
        self.unit_buses_calibr = Unit(self.data_dict_buses.data_dict, 'calibr', 'BUSES',y)
        self.param_bu400 = Param(self.data_dict_bu400.param_dict,'BU_400',int(y/2))
        self.param_bu50 = Param(self.data_dict_bu50.param_dict,'BU_50',int(y/2))
        self.param_buses = Param(self.data_dict_buses.param_dict,'BU_SES',int(y/2))

        self.stackedWidget.addWidget(self.unit_bu400_preset)
        self.stackedWidget.addWidget(self.unit_bu50_preset)
        self.stackedWidget.addWidget(self.unit_buses_preset)
        self.stackedWidget.addWidget(self.unit_bu400_calibr)
        self.stackedWidget.addWidget(self.unit_bu50_calibr)
        self.stackedWidget.addWidget(self.unit_buses_calibr)
        self.stackedWidget.addWidget(self.param_bu400)
        self.stackedWidget.addWidget(self.param_bu50)
        self.stackedWidget.addWidget(self.param_buses)
        self.stackedWidget.setCurrentIndex(0)
        # self.vbox.addWidget(self.stackedWidget)

        # self.buttonAction1.clicked.connect(lambda: self.readData_bu400(self.data_dict_bu400))
        # self.buttonAction1.clicked.connect(lambda: self.readData_bu50(self.data_dict_buses))
        # self.buttonAction1.clicked.connect(lambda: self.readData_buses(self.data_dict_bu50))

        # self.buttonAction1.clicked.connect(self.open_second_window)
        self.buttonAction1.clicked.connect(self.readData_bu400)
        self.buttonAction1.clicked.connect(self.readData_bu50)
        self.buttonAction1.clicked.connect(self.readData_buses)
        self.buttonAction2.clicked.connect(self.writeData_bu400)
        self.buttonAction2.clicked.connect(self.writeData_bu50)
        self.buttonAction2.clicked.connect(self.writeData_buses)
        self.buttonAction3.clicked.connect(self.saveData_bu400)
        self.buttonAction3.clicked.connect(self.saveData_bu50)
        self.buttonAction3.clicked.connect(self.saveData_buses)
        # self.buttonAction2.clicked.connect(self.readData_bu50)
        # self.buttonAction2.clicked.connect(self.readData_buses)

        self.readData_bu400_flag = 0
        self.readData_bu50_flag = 0
        self.readData_buses_flag = 0

        self.count_read_bu400 =-4
        self.count_read_bu50 =-4
        self.count_read_buses =-4

        self.centralwidget.setLayout(self.vbox)
        # self.centralwidget.setLayout(self.actionLayout)

        self.main.setCentralWidget(self.centralwidget)

        # self.setCentralWidget(self.centralwidget)
        self.main.setObjectName("MainWindow")
        self.main.setWindowTitle('Calibrator')
        self.main.show()

        # self.open_second_window()

    def UnitWidget(self):
        if self.buttonCalibr.isChecked():
            self.stackedWidget.setCurrentIndex(3)
        elif self.buttonPar.isChecked():
            self.stackedWidget.setCurrentIndex(6)
        else:
            self.stackedWidget.setCurrentIndex(0)
        self.buttonUnit1.setCheckable(True)
        self.buttonUnit1.setDown(True)
        self.buttonUnit2.setChecked(False)
        self.buttonUnit3.setChecked(False)
        self.buttonUnit2.setDown(False)
        self.buttonUnit3.setDown(False)
        if self.readData_bu400_flag ==0:
            self.buttonAction2.setEnabled(False)
        else:
            self.buttonAction2.setEnabled(True)

    def UnitWidget2(self):
        if self.buttonCalibr.isChecked():
            self.stackedWidget.setCurrentIndex(4)
        elif self.buttonPar.isChecked():
            self.stackedWidget.setCurrentIndex(7)
        else:
            self.stackedWidget.setCurrentIndex(1)
        self.buttonUnit2.setCheckable(True)
        self.buttonUnit2.setDown(True)
        self.buttonUnit1.setChecked(False)
        self.buttonUnit3.setChecked(False)
        self.buttonUnit1.setDown(False)
        self.buttonUnit3.setDown(False)
        if self.readData_bu50_flag ==0:
            self.buttonAction2.setEnabled(False)
        else:
            self.buttonAction2.setEnabled(True)

    def UnitWidget3(self):
        if self.buttonCalibr.isChecked():
            self.stackedWidget.setCurrentIndex(5)
        elif self.buttonPar.isChecked():
            self.stackedWidget.setCurrentIndex(8)
        else:
            self.stackedWidget.setCurrentIndex(2)
        self.buttonUnit3.setCheckable(True)
        self.buttonUnit3.setDown(True)
        self.buttonUnit1.setChecked(False)
        self.buttonUnit2.setChecked(False)
        self.buttonUnit1.setDown(False)
        self.buttonUnit2.setDown(False)
        if self.readData_buses_flag ==0:
            self.buttonAction2.setEnabled(False)
        else:
            self.buttonAction2.setEnabled(True)

    def UstWidget(self):
        if self.buttonUnit1.isChecked():
            self.stackedWidget.setCurrentIndex(0)
        elif self.buttonUnit2.isChecked():
            self.stackedWidget.setCurrentIndex(1)
        elif self.buttonUnit3.isChecked():
            self.stackedWidget.setCurrentIndex(2)
        else:
            self.stackedWidget.setCurrentIndex(0)
        self.buttonUst.setCheckable(True)
        self.buttonUst.setDown(True)
        self.buttonCalibr.setChecked(False)
        self.buttonPar.setChecked(False)
        self.buttonCalibr.setDown(False)
        self.buttonPar.setDown(False)

    def CalibrWidget(self):
        if self.buttonUnit1.isChecked():
            self.stackedWidget.setCurrentIndex(3)
        elif self.buttonUnit2.isChecked():
            self.stackedWidget.setCurrentIndex(4)
        elif self.buttonUnit3.isChecked():
            self.stackedWidget.setCurrentIndex(5)
        else:
            self.stackedWidget.setCurrentIndex(3)
        self.buttonCalibr.setCheckable(True)
        self.buttonCalibr.setDown(True)
        self.buttonUst.setChecked(False)
        self.buttonPar.setChecked(False)
        self.buttonUst.setDown(False)
        self.buttonPar.setDown(False)

    def ParWidget(self):
        # self.stackedWidget.setCurrentIndex(6)
        if self.buttonUnit1.isChecked():
            self.stackedWidget.setCurrentIndex(6)
        elif self.buttonUnit2.isChecked():
            self.stackedWidget.setCurrentIndex(7)
        elif self.buttonUnit3.isChecked():
            self.stackedWidget.setCurrentIndex(8)
        else:
            self.stackedWidget.setCurrentIndex(6)
        self.buttonPar.setCheckable(True)
        self.buttonPar.setDown(True)
        self.buttonUst.setChecked(False)
        self.buttonCalibr.setChecked(False)
        self.buttonUst.setDown(False)
        self.buttonCalibr.setDown(False)

        # self.button.setEnabled(True) # Включаем кнопку, когда второе окно отображено
    def readData_bu400(self):
        # printff('readData_bu400',self.buttonUnit1.isChecked())
        if not self.buttonUnit2.isChecked() and not self.buttonUnit3.isChecked():
            # self.worker = Worker(self.data_dict_bu400)
            # self.worker.run1()
            # self.thread_start(self.data_dict_bu400,"BU_400",'r')
            # self.readData_bu400_flag = 1
            # test
            self.read_data_dict_bu400 = self.data_dict_bu400.test_data_dict('calibr')
            self.unit_bu400_preset.readData(self.read_data_dict_bu400, 'preset',1)
            self.unit_bu400_calibr.readData(self.read_data_dict_bu400, 'calibr',1)

    def thread_start(self,obj, name_obj,mode):
        # self.th =ThreadCalibrator(self.testing)
        self.th =ThreadCalibrator(obj,name_obj,mode)
        self.th.start()
        # self.th.mysignal.connect(self.on_change,QtCore.Qt.QueuedConnection)
        if mode =='r':
            self.th.finished2.connect(self.next_main_thread_read)
        else:
            self.th.finished2.connect(self.next_main_thread_write)

    def next_main_thread_read(self,name_obj):
        printf('next main thread read',name_obj)
        if name_obj =='BU_400':
            self.count_read_bu400 += 4
            self.obj_cal_bu400 = self.data_dict_bu400
            self.read_data_dict_bu400 = self.data_dict_bu400.data_dict
            self.unit_bu400_preset.readData(self.read_data_dict_bu400,'preset',self.count_read_bu400)
            self.unit_bu400_calibr.readData(self.read_data_dict_bu400,'calibr',self.count_read_bu400)
        if name_obj =='BU_50':
            self.count_read_bu50 += 4
            self.obj_cal_bu50 = self.data_dict_bu50
            self.read_data_dict_bu50 = self.data_dict_bu50.data_dict
            self.unit_bu50_preset.readData(self.read_data_dict_bu50,'preset',self.count_read_bu50)
            self.unit_bu50_calibr.readData(self.read_data_dict_bu50,'calibr',self.count_read_bu50)
        if name_obj =='BU_SES':
            self.count_read_buses += 4
            self.obj_cal_buses = self.data_dict_buses
            self.read_data_dict_buses = self.data_dict_buses.data_dict
            self.unit_buses_preset.readData(self.read_data_dict_buses,'preset',self.count_read_buses)
            self.unit_buses_calibr.readData(self.read_data_dict_buses,'calibr',self.count_read_buses)
            # pass
        # self.buttonAction2.setEnabled(True)
        self.worker.time_stop()

    def next_main_thread_write(self,name_obj):
        printf('next main thread write',name_obj)
        if name_obj =='BU_400':
            self.unit_bu400_preset.writeData(self.read_data_dict_bu400,'preset')
            data_dict = self.unit_bu400_calibr.writeData(self.read_data_dict_bu400,'calibr')
            self.data_dict_bu400.update_data_dict(data_dict)
        if name_obj =='BU_50':
            self.unit_bu50_preset.writeData(self.read_data_dict_bu50,'preset')
            data_dict = self.unit_bu50_calibr.writeData(self.read_data_dict_bu50,'calibr')
            self.data_dict_bu50.update_data_dict(data_dict)
        if name_obj =='BU_SES':
            self.unit_buses_preset.writeData(self.read_data_dict_buses,'preset')
            data_dict = self.unit_buses_calibr.writeData(self.read_data_dict_buses,'calibr')
            self.data_dict_buses.update_data_dict(data_dict)
        self.buttonAction2.setEnabled(True)
        self.worker.time_stop()
    # def on_change(self,s):
    #     self.unit_bu400_preset.readData(self.read_data_dict_bu400,'preset')
    #     self.unit_bu400_calibr.readData(self.read_data_dict_bu400,'calibr')

    def readData_bu50(self):
        # printff('readData_bu50',self.buttonUnit2.isChecked())
        if self.buttonUnit2.isChecked():
            self.worker = Worker(self.data_dict_bu50)
            self.worker.run1()
            self.thread_start(self.data_dict_bu50,"BU_50",'r')
            self.readData_bu50_flag = 1

    def readData_buses(self):
        # printff('readData_buses',self.buttonUnit3.isChecked())
        if self.buttonUnit3.isChecked():
            self.worker = Worker(self.data_dict_buses)
            self.worker.run1()
            self.thread_start(self.data_dict_buses,"BU_SES",'r')
            self.readData_buses_flag = 1

    def writeData_bu400(self):
        if not self.buttonUnit2.isChecked() and not self.buttonUnit3.isChecked():
            # self.unit_bu400_preset.writeData(self.read_data_dict_bu400,'preset')
            # data_dict = self.unit_bu400_calibr.writeData(self.read_data_dict_bu400,'calibr')
            # self.data_dict_bu400.update_data_dict(data_dict)
            self.worker = Worker(self.data_dict_bu400)
            self.worker.run1()
            self.thread_start(self.data_dict_bu400,"BU_400",'w')

    def writeData_bu50(self):
        if self.buttonUnit2.isChecked():
            # self.unit_bu50_preset.writeData(self.read_data_dict_bu50,'preset')
            # data_dict = self.unit_bu50_calibr.writeData(self.read_data_dict_bu50,'calibr')
            # self.data_dict_bu50.update_data_dict(data_dict)
            self.worker = Worker(self.data_dict_bu50)
            self.worker.run1()
            self.thread_start(self.data_dict_bu50,"BU_50",'w')

    def writeData_buses(self):
        if self.buttonUnit3.isChecked():
            # self.unit_buses_preset.writeData(self.read_data_dict_buses,'preset')
            # data_dict = self.unit_buses_calibr.writeData(self.read_data_dict_buses,'calibr')
            # self.data_dict_buses.update_data_dict(data_dict)
            self.worker = Worker(self.data_dict_buses)
            self.worker.run1()
            self.thread_start(self.data_dict_buses,"BU_SES",'w')

    def saveData_bu400(self):
        if not self.buttonUnit2.isChecked() and not self.buttonUnit3.isChecked():
            printf('saveData_bu400')
            # self.unit_bu400_preset.saveData(self.obj_cal_bu400,'preset','bu400')
            # self.unit_bu400_calibr.saveData(self.obj_cal_bu400,'calibr','bu400')
            # self.unit_bu400_calibr.saveData(self.obj_cal_bu400,'filter','bu400')
            #test
            self.unit_bu400_preset.saveDatatest('preset','bu400')
            self.unit_bu400_calibr.saveDatatest('calibr','bu400')

    def saveData_bu50(self):
        if self.buttonUnit2.isChecked():
            printf('saveData_bu50')
            self.unit_bu50_preset.saveData(self.obj_cal_bu50,'preset','bu50')
            self.unit_bu50_calibr.saveData(self.obj_cal_bu50,'calibr','bu50')
            # self.unit_bu50_calibr.saveData(self.obj_cal_bu50,'filter','bu50')

    def saveData_buses(self):
        if self.buttonUnit3.isChecked():
            printf('saveData_buses')
            self.unit_buses_preset.saveData(self.obj_cal_buses,'preset','buses')
            self.unit_buses_calibr.saveData(self.obj_cal_buses,'calibr','buses')
            # self.unit_buses_calibr.saveData(self.obj_cal_buses,'filter','buses')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Main()
    sys.exit(app.exec_())
