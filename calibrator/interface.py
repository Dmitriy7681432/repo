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
# from debug import print
from PyQt5.QtCore import QBasicTimer
# from debug1.test1 import Testing
import serial.tools.list_ports

from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication)
import warning


class Worker(QThread):
    finished = pyqtSignal()
    window_created = pyqtSignal(QWidget)
    flag_err_work =0

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
        print('updata_pr')
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
        print('3')

    # Вновь
    # def closeEvent(self):
    #     self.window.setWindowModality(Qt.Qt.NonModal)
    def timerEvent(self, e):
        print('timer_event',self.val, self.timer.isActive())
        self.pbar.setValue(self.val)
        if self.val >= 100 or self.flag_err_work:
            self.timer.stop()
            self.window.close()
            self.window.setWindowModality(Qt.Qt.NonModal)
            # self.btn.setText('Закончено')
            return

        # self.step = self.step + self.val
        # self.step = self.step + 1

    def doAction(self):
        print('doAction', self.timer.isActive())
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
    flag_err = 0
    finished_err = pyqtSignal()

    def __init__(self, obj,name_obj,mode):
        super().__init__()
        self.obj = obj
        self.name_obj = name_obj
        self.mode = mode

    def run(self):
        i = 1
        print('Thread start')
        self.flag_err = self.obj.main_data_read(self.mode)
        # while True:
        # for i in range(0,10):
        #     self.sleep(1)
            # self.mysignal.emit('%s'% i)
        # self.obj.rest()
        if self.flag_err=='ERR':
            self.finished_err.emit()
        else:
            self.finished2.emit('%s' % self.name_obj)
        # self.finished2.emit()


class ComPort(QWidget):
    def __init__(self,arg='product'):
        super().__init__()
        self.setWindowTitle("Выбор изделия")
        self.setGeometry(100, 100, 300, 200)

        #Шрифт
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        # font.setBold(True)
        # font.setWeight(75)

        desktop = QtWidgets.QApplication.desktop()
        x = desktop.width()
        y = desktop.height()
        x_size_desktop = 255
        y_size_desktop = int(y / 14)
        print(x_size_desktop,y_size_desktop)
        self.resize(x_size_desktop, y_size_desktop)
        # Вывод окна по центру
        x_ = (desktop.width() - self.frameSize().width()) // 2
        y_ = (desktop.height() - self.frameSize().height()) // 2
        self.move(x_, y_)

        combo = QComboBox(self)
        lst_combo = []
        if arg =='com':
            ports = serial.tools.list_ports.comports()
            for port in ports:
                lst_combo.append(port.name)
                print(port.hwid,port.name,port.vid,port.pid,port.serial_number,port.location,port.manufacturer,port.product,port.interface)
            label = 'Выберите com port:'
        else:
            label = 'Выберите изделие:'
            lst_combo = ['SES200M','SEP30M']


        # layout = QVBoxLayout(self)

        self.lbl = QLabel(label, self)
        self.lbl.move(int(x_size_desktop/8.0),10)
        combo.addItems(lst_combo)
        combo.move(int(x_size_desktop/8.0), 30)

        # self.move(x_, y_)
        combo.activated[str].connect(self.onActivated)

        self.open_button = QPushButton("OK", self)
        self.open_button.clicked.connect(self.open_second_window)
        self.open_button.move(140, 30)
        self.open_button.setFont(font)
        combo.setFont(font)
        font.setPointSize(12)
        font.setWeight(75)
        self.lbl.setFont(font)

        # layout.addWidget(self.lbl)
        # layout.addWidget(combo)
        # layout.addWidget(self.open_button)
        # Цветовой фон
        pal = self.palette()
        # Если use 1-й аргумент, то цвет будет пропадать при переходе на др окно
        # pal.setColor(QtGui.QPalette.Window, QtGui.QColor(191, 245, 234))
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor(220, 254, 225))
        self.setPalette(pal)

        self.cur_elem = combo.currentText()


    def onActivated(self, text):
        self.cur_elem= text

        # self.lbl.adjustSize()

    def open_second_window(self):
        self.second_window = Main(self.cur_elem)
        # self.second_window.show()
        self.close()  # Закрывает текущее (первое) окно


class Main(QWidget):
    def __init__(self,cur_elem):
        self.cur_elem = cur_elem
        super().__init__()

        if self.cur_elem =='SES200M': self.lst_cb = ['BU_400','BU_50','BU_SES']; size_button =300
        else: self.lst_cb = ['BU_SEP','BU_400'];size_button =500
        self.calibr_obj = []
        self.unit_obj_preset = []
        self.unit_obj_calibr = []
        self.param_obj = []
        self.button_obj = []

        self.main = QMainWindow()
        self.timer = QTimer()

        #Шрифт
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        desktop = QtWidgets.QApplication.desktop()
        x = desktop.width()
        y = desktop.height()
        # print(x, y)
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
        # print(self.stackedWidget.size().height())
        self.stackedWidget.setObjectName("stackedWidget")

        # print(stack_size_x,stack_size_y,stack_size_yy,stack_size_xx)
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
        for i,v in enumerate(self.lst_cb):
            self.button_obj.append(QToolButton())
            self.button_obj[i].setText(v)
            self.button_obj[i].setCheckable(True)
            if i ==0:
                self.button_obj[i].setDown(True)
                self.button_obj[i].setChecked(False)
            self.button_obj[i].setFont(font)
            self.button_obj[i].setStyleSheet('background-color:rgb(153,173,232);')
            self.button_obj[i].setMaximumSize(QtCore.QSize(size_button, 50))
            self.button_obj[i].setObjectName(f"buttonUnit{i+1}")

        for i,v in enumerate(self.lst_cb):
            # self.button_obj[i].clicked.connect(lambda: self.UnitWidgetMain(i))
            if i ==0:
                self.button_obj[0].clicked.connect(self.UnitWidget)
            elif i ==1:
                self.button_obj[1].clicked.connect(self.UnitWidget2)
            else:
                self.button_obj[2].clicked.connect(self.UnitWidget3)

        # self.buttonUnit1 = QToolButton()
        # self.buttonUnit1.setText('БУ400')
        # self.buttonUnit1.setDown(True)
        # self.buttonUnit1.setCheckable(True)
        # self.buttonUnit1.setChecked(False)
        # self.buttonUnit1.clicked.connect(self.UnitWidgMainet)
        # self.buttonUnit1.setFont(font)
        # self.buttonUnit1.setStyleSheet('background-color:rgb(153,173,232);')
        # self.buttonUnit1.setMaximumSize(QtCore.QSize(300, 50))
        # self.buttonUnit1.setObjectName("buttonUnit1")

        # self.buttonUnit2 = QToolButton()
        # self.buttonUnit2.setText('БУ50')
        # self.buttonUnit2.setCheckable(True)
        # self.buttonUnit2.clicked.connect(self.UnitWidget2)
        # self.buttonUnit2.setFont(font)
        # self.buttonUnit2.setStyleSheet('background-color:rgb(153,173,232);')
        # self.buttonUnit2.setMaximumSize(QtCore.QSize(300, 50))
        # self.buttonUnit2.setObjectName("buttonUnit2")

        # self.buttonUnit3 = QToolButton()
        # self.buttonUnit3.setText('БУСЭС')
        # self.buttonUnit3.setCheckable(True)
        # self.buttonUnit3.setChecked(False)
        # self.buttonUnit3.clicked.connect(self.UnitWidget3)
        # self.buttonUnit3.setFont(font)
        # self.buttonUnit3.setStyleSheet('background-color:rgb(153,173,232);')
        # self.buttonUnit3.setMaximumSize(QtCore.QSize(300, 50))
        # self.buttonUnit3.setObjectName("buttonUnit3")
        # self.buttonUnit3.deleteLater()

        # Кнопки действия
        self.buttonAction1 = QToolButton()
        self.buttonAction1.setText('Считать')
        self.buttonAction2 = QToolButton()
        self.buttonAction2.setText('Записать')
        self.buttonAction2.setEnabled(False)
        self.buttonAction3 = QToolButton()
        self.buttonAction3.setText('Сохранить')
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


        self.vbox.setContentsMargins(0,0,0, 0)
        self.vbox.setSpacing(0)

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
        for i,v in enumerate(self.lst_cb):
            self.mainLayout.addWidget(self.button_obj[i])
        # self.mainLayout.addWidget(self.buttonUnit1)
        # self.mainLayout.addWidget(self.buttonUnit2)
        # self.mainLayout.addWidget(self.buttonUnit3)
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

        self.ser = Connect(self.cur_elem)

        # Инициализация объекта Calibrator
        for i in self.lst_cb:
            self.calibr_obj.append(Calibrator(self.ser, cur_elem, i))

        # self.testing = Testing(self.ser.ser, 'SES200M', 'BU_400')

        # Инициализация объекта Unit, Param
        for i,v in enumerate(self.lst_cb):
            self.unit_obj_preset.append(Unit(self.calibr_obj[i].data_dict, 'preset', v,y))
            self.unit_obj_calibr.append(Unit(self.calibr_obj[i].data_dict, 'calibr', v,y))
            self.param_obj.append(Param(self.calibr_obj[i].param_dict, v,int(y/2)))
            self.stackedWidget.addWidget(self.unit_obj_preset[i])

        for i,v in enumerate(self.lst_cb):
            self.stackedWidget.addWidget(self.unit_obj_calibr[i])
        for i, v in enumerate(self.lst_cb):
            self.stackedWidget.addWidget(self.param_obj[i])

        self.stackedWidget.setCurrentIndex(0)


        for i, v in enumerate(self.lst_cb):
            if i ==0:
                self.buttonAction1.clicked.connect(self.readData_bu1)
                self.buttonAction2.clicked.connect(self.writeData_bu1)
                self.buttonAction3.clicked.connect(self.saveData_bu1)
            elif i ==1:
                self.buttonAction1.clicked.connect(self.readData_bu2)
                self.buttonAction2.clicked.connect(self.writeData_bu2)
                self.buttonAction3.clicked.connect(self.saveData_bu2)
            else:
                self.buttonAction1.clicked.connect(self.readData_bu3)
                self.buttonAction2.clicked.connect(self.writeData_bu3)
                self.buttonAction3.clicked.connect(self.saveData_bu3)

        self.button_obj[0].animateClick()

        self.readData_bu1_flag = 0
        self.readData_bu2_flag = 0
        self.readData_bu3_flag = 0

        self.count_read_bu400 =-4
        self.count_read_bu50 =-4
        self.count_read_buses =-4

        self.centralwidget.setLayout(self.vbox)

        self.main.setCentralWidget(self.centralwidget)

        self.main.setObjectName("MainWindow")
        self.main.setWindowTitle(f'Calibrator {self.cur_elem}')
        self.main.show()

    def UnitWidgetMain(self, i):
        print('UnitW')
        if i ==0:
            print('UnitW1')
            self.UnitWidget()
        elif i ==1:
            print('UnitW2')
            self.UnitWidget2()
        else:
            print('UnitW3')
            self.UnitWidget3()

    def UnitWidget(self):

        for i,v in enumerate(self.lst_cb):
            if self.buttonCalibr.isChecked():
                self.stackedWidget.setCurrentIndex(len(self.lst_cb))
            elif self.buttonPar.isChecked():
                self.stackedWidget.setCurrentIndex(len(self.lst_cb)+len(self.lst_cb))
            else:
                self.stackedWidget.setCurrentIndex(0)

            if i==0:
                self.button_obj[i].setCheckable(True)
                self.button_obj[i].setDown(True)
            else:
                self.button_obj[i].setChecked(False)
                self.button_obj[i].setDown(False)

        # self.buttonUnit1.setCheckable(True)
        # self.buttonUnit1.setDown(True)
        # self.buttonUnit2.setChecked(False)
        # self.buttonUnit2.setDown(False)
        # self.buttonUnit3.setChecked(False)
        # self.buttonUnit3.setDown(False)

        if self.readData_bu1_flag ==0:
            self.buttonAction2.setEnabled(False)
        else:
            self.buttonAction2.setEnabled(True)

    def UnitWidget2(self):
        for i,v in enumerate(self.lst_cb):
            if self.buttonCalibr.isChecked():
                self.stackedWidget.setCurrentIndex(len(self.lst_cb)+1)
            elif self.buttonPar.isChecked():
                self.stackedWidget.setCurrentIndex(len(self.lst_cb)+len(self.lst_cb)+1)
            else:
                self.stackedWidget.setCurrentIndex(1)

            if i==1:
                self.button_obj[i].setCheckable(True)
                self.button_obj[i].setDown(True)
            else:
                self.button_obj[i].setChecked(False)
                self.button_obj[i].setDown(False)

        # self.buttonUnit1.setChecked(False)
        # self.buttonUnit1.setDown(False)
        # self.buttonUnit2.setCheckable(True)
        # self.buttonUnit2.setDown(True)
        # self.buttonUnit3.setChecked(False)
        # self.buttonUnit3.setDown(False)

        if self.readData_bu2_flag ==0:
            self.buttonAction2.setEnabled(False)
        else:
            self.buttonAction2.setEnabled(True)

    def UnitWidget3(self):
        for i,v in enumerate(self.lst_cb):
            if self.buttonCalibr.isChecked():
                self.stackedWidget.setCurrentIndex(len(self.lst_cb)+2)
            elif self.buttonPar.isChecked():
                self.stackedWidget.setCurrentIndex(len(self.lst_cb)+len(self.lst_cb)+2)
            else:
                self.stackedWidget.setCurrentIndex(2)

            if i==2:
                self.button_obj[i].setCheckable(True)
                self.button_obj[i].setDown(True)
            else:
                self.button_obj[i].setChecked(False)
                self.button_obj[i].setDown(False)

        # self.buttonUnit1.setChecked(False)
        # self.buttonUnit1.setDown(False)
        # self.buttonUnit2.setChecked(False)
        # self.buttonUnit2.setDown(False)
        # self.buttonUnit3.setCheckable(True)
        # self.buttonUnit3.setDown(True)

        if self.readData_bu3_flag ==0:
            self.buttonAction2.setEnabled(False)
        else:
            self.buttonAction2.setEnabled(True)

    def UstWidget(self):
        flag =0
        for i,v in enumerate(self.lst_cb):
            if self.button_obj[i].isChecked():
                self.stackedWidget.setCurrentIndex(i)
                flag = 1
            if flag==0:
                self.stackedWidget.setCurrentIndex(0)

        # if self.buttonUnit1.isChecked():
        #     self.stackedWidget.setCurrentIndex(0)
        # elif self.buttonUnit2.isChecked():
        #     self.stackedWidget.setCurrentIndex(1)
        # elif self.buttonUnit3.isChecked():
        #     self.stackedWidget.setCurrentIndex(2)
        # else:
        #     self.stackedWidget.setCurrentIndex(0)

        self.buttonUst.setCheckable(True)
        self.buttonUst.setDown(True)
        self.buttonCalibr.setChecked(False)
        self.buttonCalibr.setDown(False)
        self.buttonPar.setChecked(False)
        self.buttonPar.setDown(False)

    def CalibrWidget(self):
        flag =0
        for i,v in enumerate(self.lst_cb):
            if self.button_obj[i].isChecked():
                self.stackedWidget.setCurrentIndex(i+len(self.lst_cb))
                flag = 1
            if flag==0:
                self.stackedWidget.setCurrentIndex(len(self.lst_cb))


        # if self.buttonUnit1.isChecked():
        #     self.stackedWidget.setCurrentIndex(3)
        # elif self.buttonUnit2.isChecked():
        #     self.stackedWidget.setCurrentIndex(4)
        # elif self.buttonUnit3.isChecked():
        #     self.stackedWidget.setCurrentIndex(5)
        # else:
        #     self.stackedWidget.setCurrentIndex(3)

        self.buttonUst.setChecked(False)
        self.buttonUst.setDown(False)
        self.buttonCalibr.setCheckable(True)
        self.buttonCalibr.setDown(True)
        self.buttonPar.setChecked(False)
        self.buttonPar.setDown(False)

    def ParWidget(self):
        flag =0
        for i,v in enumerate(self.lst_cb):
            if self.button_obj[i].isChecked():
                self.stackedWidget.setCurrentIndex(i+len(self.lst_cb)+len(self.lst_cb))
                flag = 1
            if flag==0:
                self.stackedWidget.setCurrentIndex(len(self.lst_cb)+len(self.lst_cb))

        # if self.buttonUnit1.isChecked():
        #     self.stackedWidget.setCurrentIndex(6)
        # elif self.buttonUnit2.isChecked():
        #     self.stackedWidget.setCurrentIndex(7)
        # elif self.buttonUnit3.isChecked():
        #     self.stackedWidget.setCurrentIndex(8)
        # else:
        #     self.stackedWidget.setCurrentIndex(6)

        self.buttonUst.setChecked(False)
        self.buttonUst.setDown(False)
        self.buttonCalibr.setChecked(False)
        self.buttonCalibr.setDown(False)
        self.buttonPar.setCheckable(True)
        self.buttonPar.setDown(True)

        # self.button.setEnabled(True) # Включаем кнопку, когда второе окно отображено
    def readData_bu1(self):
        # if not self.button_obj[1].isChecked() and not self.button_obj[2].isChecked():
        if self.button_obj[0].isChecked():
            self.worker = Worker(self.calibr_obj[0])
            self.worker.run1()
            self.thread_start(self.calibr_obj[0],"BU_400",'r')
            self.readData_bu1_flag = 1
            # test
            # self.read_data_dict_bu400 = self.data_dict_bu400.test_data_dict('calibr')
            # self.unit_bu400_preset.readData(self.read_data_dict_bu400, 'preset',1)
            # self.unit_bu400_calibr.readData(self.read_data_dict_bu400, 'calibr',1)

    def readData_bu2(self):
        # printf('readData_bu50',self.buttonUnit2.isChecked())
        if self.button_obj[1].isChecked():
            self.worker = Worker(self.calibr_obj[1])
            self.worker.run1()
            self.thread_start(self.calibr_obj[1],"BU_50",'r')
            self.readData_bu2_flag = 1

    def readData_bu3(self):
        # printf('readData_buses',self.buttonUnit3.isChecked())
        if self.button_obj[2].isChecked():
            self.worker = Worker(self.calibr_obj[2])
            self.worker.run1()
            self.thread_start(self.calibr_obj[2],"BU_SES",'r')
            self.readData_bu3_flag = 1
    def thread_start(self,obj, name_obj,mode):
        # self.th =ThreadCalibrator(self.testing)
        self.th =ThreadCalibrator(obj,name_obj,mode)
        self.th.start()
        # self.th.mysignal.connect(self.on_change,QtCore.Qt.QueuedConnection)
        if self.th.flag_err =='ERR':
            print()
            self.th.quit()
        self.th.finished_err.connect(self.signal_thread_stop)
        if mode =='r':
            self.th.finished2.connect(self.next_main_thread_read)
        else:
            self.th.finished2.connect(self.next_main_thread_write)

    def signal_thread_stop(self):
        self.worker.flag_err_work=1
        # sign = Worker(self.data_dict_bu400)
        self.sign = warning.SignalErr()
    def next_main_thread_read(self,name_obj):
        print('next main thread read',name_obj)
        if name_obj =='BU_400':
            self.count_read_bu400 += 4
            self.obj_cal_bu400 = self.calibr_obj[0]
            self.read_data_dict_bu400 = self.calibr_obj[0].data_dict
            self.unit_obj_preset[0].readData(self.read_data_dict_bu400,'preset',self.count_read_bu400)
            self.unit_obj_calibr[0].readData(self.read_data_dict_bu400,'calibr',self.count_read_bu400)
        if name_obj =='BU_50':
            self.count_read_bu50 += 4
            self.obj_cal_bu50 = self.calibr_obj[1]
            self.read_data_dict_bu50 = self.calibr_obj[1].data_dict
            self.unit_obj_preset[1].readData(self.read_data_dict_bu50,'preset',self.count_read_bu50)
            self.unit_obj_calibr[1].readData(self.read_data_dict_bu50,'calibr',self.count_read_bu50)
        if name_obj =='BU_SES':
            self.count_read_buses += 4
            self.obj_cal_buses = self.calibr_obj[2]
            self.read_data_dict_buses = self.calibr_obj[2].data_dict
            self.unit_obj_preset[2].readData(self.read_data_dict_buses,'preset',self.count_read_buses)
            self.unit_obj_calibr[2].readData(self.read_data_dict_buses,'calibr',self.count_read_buses)
            # pass
        self.buttonAction2.setEnabled(True)
        self.worker.time_stop()

    def next_main_thread_write(self,name_obj):
        print('next main thread write',name_obj)
        if name_obj =='BU_400':
            self.unit_obj_preset[0].writeData(self.read_data_dict_bu400,'preset')
            data_dict = self.unit_bu400_calibr.writeData(self.read_data_dict_bu400,'calibr')
            self.calibr_obj[0].update_data_dict(data_dict)
        if name_obj =='BU_50':
            self.unit_obj_preset[1].writeData(self.read_data_dict_bu50,'preset')
            data_dict = self.unit_bu50_calibr.writeData(self.read_data_dict_bu50,'calibr')
            self.calibr_obj[1].update_data_dict(data_dict)
        if name_obj =='BU_SES':
            self.unit_obj_preset[2].writeData(self.read_data_dict_buses,'preset')
            data_dict = self.unit_buses_calibr.writeData(self.read_data_dict_buses,'calibr')
            self.calibr_obj[2].update_data_dict(data_dict)
        self.buttonAction2.setEnabled(True)
        self.worker.time_stop()
    # def on_change(self,s):
    #     self.unit_bu400_preset.readData(self.read_data_dict_bu400,'preset')
    #     self.unit_bu400_calibr.readData(self.read_data_dict_bu400,'calibr')


    def writeData_bu1(self):
        # if not self.button_obj[1].isChecked() and not self.button_obj[2].isChecked():
        if self.button_obj[0].isChecked():
            # self.unit_bu400_preset.writeData(self.read_data_dict_bu400,'preset')
            # data_dict = self.unit_bu400_calibr.writeData(self.read_data_dict_bu400,'calibr')
            # self.data_dict_bu400.update_data_dict(data_dict)
            self.worker = Worker(self.calibr_obj[0])
            self.worker.run1()
            self.thread_start(self.calibr_obj[0],"BU_400",'w')

    def writeData_bu2(self):
        if self.button_obj[1].isChecked():
            # self.unit_bu50_preset.writeData(self.read_data_dict_bu50,'preset')
            # data_dict = self.unit_bu50_calibr.writeData(self.read_data_dict_bu50,'calibr')
            # self.data_dict_bu50.update_data_dict(data_dict)
            self.worker = Worker(self.calibr_obj[1])
            self.worker.run1()
            self.thread_start(self.calibr_obj[1],"BU_50",'w')

    def writeData_bu3(self):
        if self.button_obj[2].isChecked():
            # self.unit_buses_preset.writeData(self.read_data_dict_buses,'preset')
            # data_dict = self.unit_buses_calibr.writeData(self.read_data_dict_buses,'calibr')
            # self.data_dict_buses.update_data_dict(data_dict)
            self.worker = Worker(self.calibr_obj[2])
            self.worker.run1()
            self.thread_start(self.calibr_obj[2],"BU_SES",'w')

    def saveData_bu1(self):
        # if not self.button_obj[1].isChecked() and not self.button_obj[2].isChecked():
        if self.button_obj[0].isChecked():
            print('saveData_bu1')
            self.unit_obj_preset[0].saveData(self.obj_cal_bu400,'preset','bu400')
            self.unit_obj_calibr[0].saveData(self.obj_cal_bu400,'calibr','bu400')
            self.unit_obj_calibr[0].saveData(self.obj_cal_bu400,'filter','bu400')
            #test
            # self.unit_bu400_preset.saveDatatest('preset','bu400')
            # self.unit_bu400_calibr.saveDatatest('calibr','bu400')

    def saveData_bu2(self):
        if self.button_obj[1].isChecked():
            print('saveData_bu2')
            self.unit_obj_preset[1].saveData(self.obj_cal_bu50,'preset','bu50')
            self.unit_obj_calibr[1].saveData(self.obj_cal_bu50,'calibr','bu50')
            self.unit_obj_calibr[1].saveData(self.obj_cal_bu50,'filter','bu50')

    def saveData_bu3(self):
        if self.button_obj[2].isChecked():
            print('saveData_bu3')
            self.unit_obj_preset[2].saveData(self.obj_cal_buses,'preset','buses')
            self.unit_obj_calibr[2].saveData(self.obj_cal_buses,'calibr','buses')
            self.unit_obj_calibr[2].saveData(self.obj_cal_buses,'filter','buses')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # ex = Main('COM')
    ex = ComPort()
    ex.show()
    sys.exit(app.exec_())
    # app.exec_()
