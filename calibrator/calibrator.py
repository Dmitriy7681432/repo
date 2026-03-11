# -*- coding: utf-8 -*-
import sys,serial,struct
import time,json

from PyQt5.QtWidgets import (QWidget, QPushButton, QStackedWidget, QToolBar, QToolButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QAction, QMainWindow,QDialog,QLabel,QProgressBar,
                             QDesktopWidget)

from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot,QTimer
from unit_interface import Unit,Param
from class_read_data import Connect,Calibrator
# from debug import printf
from PyQt5.QtCore import QBasicTimer
# from debug1.test1 import Testing
import serial.tools.list_ports

from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication)
import warning,number_product

from debug import *
import typing
# from unit_interface import *
# from class_read_data import *
# from number_product import *
# from warning import *


class Worker(QThread):
    finished = pyqtSignal()
    window_abort = pyqtSignal()
    flag_err_work =0

    def __init__(self,obj_main,action):
        super().__init__()
        self.window = None
        self.obj_main = obj_main
        self.action = action

    def run1(self):
        # Здесь создается второе окно
        self.main_window = QWidget()
        # layout = QVBoxLayout()
        # label = QLabel("Второе окно")
        # layout.addWidget(label)
        # self.window.setLayout(layout)
        # self.window.setWindowTitle("Второе окно")
        # self.window = test_qt1.Example()

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        # font.setBold(True)

        self.window0 = QWidget(self.main_window)
        self.window0.setGeometry(110, -10, 240, 55)
        self.lbl = QLabel(f'<i>{self.action}</i>', self.window0)
        self.window = QWidget(self.main_window)
        self.window.setGeometry(20, 20, 240, 55)
        self.pbar = QProgressBar(self.window)
        self.pbar.setGeometry(20, 40, 200, 55)
        self.window2 = QWidget(self.main_window)
        self.window2.setGeometry(65, 60, 140, 45)
        self.button = QPushButton('Прервать',self.window2)
        self.button.setGeometry(90, 60, 80, 25)
        self.button.setFont(font)
        self.button.clicked.connect(self.button_clicked)
        # font.setBold(True)
        self.lbl.setStyleSheet('color: rgba(8,8,8,0.7)')
        self.lbl.setFont(font)
        # self.btn = QPushButton('Начать', self.window)
        # self.btn.move(30, 80)
        # self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0

        layout0 = QVBoxLayout(self.window0)
        layout0.addWidget(self.lbl)
        layout0.setContentsMargins(0,0,0,0)
        # layout0.setGeometry(QtCore.QRect(30,40,200,55))
        layout = QVBoxLayout(self.window)
        layout.addWidget(self.pbar)
        # layout.setContentsMargins(10,0,10,10)
        layout.setContentsMargins(0,0,0,0)
        layout.setGeometry(QtCore.QRect(30,40,200,55))
        layout.addWidget(self.pbar)
        layout2 = QVBoxLayout(self.window2)
        # layout2.setContentsMargins(50,0,50,0)
        layout2.setContentsMargins(0,0,0,0)
        layout2.addWidget(self.button)
        # layout2.setGeometry(QtCore.QRect(35,60,200,25))
        # # layout.addWidget(self.button)
        # layout.addWidget(self.btn)
        # self.window.setLayout(layout2)

        self.main_window.setGeometry(100, 100, 280, 100)
        self.center() # Центрируем окно
        self.main_window.setWindowTitle('Загрузка')
        # Блокировка главного окна
        self.main_window.setWindowModality(Qt.Qt.ApplicationModal)
        # Убрать значок закрытия окна
        self.main_window.setWindowFlags(Qt.Qt.CustomizeWindowHint | Qt.Qt.WindowTitleHint)
        self.main_window.show()
        self.obj_main.cal_signal.connect(self.update_progress_bar)

        self.doAction()

    def button_clicked(self):
        self.window_abort.emit()
        self.flag_err_work =1

    def time_stop(self):
        self.val =100

    def update_progress_bar(self,val):
        printf('updata_pr')
        self.val = val
        # self.step = self.step +self.val
        self.pbar.setValue(self.val)

    def center(self):
        qr = self.main_window.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.main_window.move(qr.topLeft())


        # self.window_created.emit(self.window)  # Отправляем сигнал о создании окна
        # self.finished.emit()  # Отправляем сигнал об окончании работы
        # printf('3')

    def timerEvent(self, e):
        # printf('timer_event',self.val, self.timer.isActive())
        self.pbar.setValue(self.val)
        if self.val >= 100 or self.flag_err_work:
            self.timer.stop()
            self.main_window.close()
            self.main_window.setWindowModality(Qt.Qt.NonModal)
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
    finished2 = pyqtSignal(str,str)
    mysignal = QtCore.pyqtSignal()
    flag_err = 0
    finished_err = pyqtSignal()
    finished_abort = pyqtSignal()

    def __init__(self, obj,name_product,name_cb,mode):
        super().__init__()
        self.obj = obj
        self.name_product = name_product
        self.name_cb = name_cb
        self.mode = mode

    def run(self):
        printf('RUN')
        i = 1
        printf('Thread start')
        self.flag_err = self.obj.main_data_read(self.mode)
        # while True:
        # for i in range(0,10):
        #     self.sleep(1)
            # self.mysignal.emit('%s'% i)
        # self.obj.rest()
        if self.flag_err=='ERR':
            self.finished_err.emit()
        elif self.flag_err =='ABORT':
            self.finished_abort.emit()
        else:
            self.finished2.emit('%s' % self.name_product,'%s' % self.name_cb)
        # self.finished2.emit()

class ThreadUnit(QtCore.QThread):
    finished_th_unit = pyqtSignal()

    def __init__(self,calibr_obj,obj_preset, obj_calibr, preset,calibr,filter,lst_cb,cur_elem,text):
        super().__init__()
        self.calibr_obj = calibr_obj
        self.obj_preset = obj_preset
        self.obj_calibr = obj_calibr
        self.preset = preset
        self.calibr = calibr
        self.filter = filter
        self.lst_cb = lst_cb
        self.cur_elem = cur_elem
        self.text = text

    def run(self):
        printf('ThreadUnit start')
        # self.flag_err = self.obj.main_data_read(self.mode)
        self.obj_preset.saveData(self.calibr_obj,self.preset,self.lst_cb,self.cur_elem,self.text)
        self.obj_calibr.saveData(self.calibr_obj,self.calibr,self.lst_cb,self.cur_elem,self.text)
        self.obj_calibr.saveData(self.calibr_obj,self.filter,self.lst_cb,self.cur_elem,self.text)
        self.finished_th_unit.emit()


class ComPort(QWidget):
    def __init__(self,arg='product'):
        super().__init__()
        self.setWindowTitle("Выбор изделия")
        self.setGeometry(100, 100, 300, 500)

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
        y_size_desktop = int(y / 12)
        printf(x_size_desktop,y_size_desktop)
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
                printf(port.hwid,port.name,port.vid,port.pid,port.serial_number,port.location,port.manufacturer,port.product,port.interface)
            label = 'Выберите com port:'
        else:
            label = 'Выберите изделие:'
            # Чтение данных с configs
            with open('configs.json', 'r') as file_configs:
                self.configs = json.load(file_configs)
                self.product = self.configs.get('default_product')
                if self.product=='SES200M':
                    lst_combo = ['SES200M','SEP30M','SES150','TOR-ARCTICA']
                elif self.product =='SEP30M':
                    lst_combo = ['SEP30M','SES200M','SES150','TOR-ARCTICA']
                elif self.product =='SES150':
                    lst_combo = ['SES150','SES200M','SEP30M','TOR-ARCTICA']
                else:
                    lst_combo = ['TOR-ARCTICA','SES200M','SEP30M','SES150']



        # layout = QVBoxLayout(self)

        self.lbl = QLabel(label, self)
        self.lbl.move(int(x_size_desktop/18.0),10)
        combo.addItems(lst_combo)
        combo.move(int(x_size_desktop/19.0), 30)
        combo.resize(135,27)

        # self.move(x_, y_)
        combo.activated[str].connect(self.onActivated)

        self.open_button = QPushButton("OK", self)
        self.open_button.clicked.connect(self.open_second_window)
        self.open_button.move(150, 30)
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
        self.configs['default_product'] = text

        # self.lbl.adjustSize()

    def open_second_window(self):
        if self.product!=self.cur_elem:
            with open('configs.json', 'w') as file_configs:
                json.dump(self.configs, file_configs, ensure_ascii=False, indent=4)
        self.second_window = Main(self.cur_elem)
        # self.second_window.show()
        self.close()  # Закрывает текущее (первое) окно

# class MyWin(QWidget,)
class Main(QMainWindow):
    def __init__(self,cur_elem):
        self.cur_elem = cur_elem
        super().__init__()
        self.th_unit =0
        self.cnt_save_data = 0

        # self.com = ComPort()
        # self.com.show()
        if self.cur_elem =='SES200M':
            self.lst_cb = ['BU_400','BU_50','BU_SES']
            self.lst_cb_rus = ['БУ 400','БУ 50','БУ СЭС']
            size_button =300
        elif self.cur_elem =='SEP30M':
            self.lst_cb = ['BU_SEP','BU_400']
            self.lst_cb_rus = ['БУ СЭП','БУ 400']
            size_button =500
        elif self.cur_elem =='SES150':
            self.lst_cb = ['BU_SES']
            self.lst_cb_rus = ['БУ СЭC']
            size_button =1000
        elif self.cur_elem =='TOR-ARCTICA':
            self.lst_cb = ['BU_EA']
            self.lst_cb_rus = ['БУ ЭА']
            size_button =1000

        self.calibr_obj = []
        self.unit_obj_preset = []
        self.unit_obj_calibr = []
        self.param_obj = []
        self.button_obj = []

        # self.main = QMainWindow()
        #Отключение размера окна на весь экран
        flags = self.windowFlags()  # получаем все флаги которые есть
        flags &= ~QtCore.Qt.WindowMaximizeButtonHint  # отключаем ненужный нам флаг
        self.setWindowFlags(flags)

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
        # printf(x, y)
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
        # printf(self.stackedWidget.size().height())
        self.stackedWidget.setObjectName("stackedWidget")

        # printf(stack_size_x,stack_size_y,stack_size_yy,stack_size_xx)
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
        for i,v in enumerate(self.lst_cb_rus):
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
        self.lbl = QLabel(f'<i>{self.cur_elem} version: 1.0.3  </i>')
        self.lbl.setFont(font)
        self.lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter )
        self.lbl.setStyleSheet('color: rgba(105,105,105,0.5)')
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
        self.stackLayout.setContentsMargins(0, 0, 0, 10)

        self.lblLayout = QHBoxLayout()
        # self.lblLayout.setContentsMargins(0, 0, 0, 0)
        self.lblLayout.setGeometry(QtCore.QRect(20,20,20,20))
        self.lblLayout.setObjectName("lblLayout")
        self.lblLayout.addWidget(self.lbl)


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
        self.vbox.addLayout(self.lblLayout)
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
        self.buttonUst.animateClick()
        self.button_obj[0].setStyleSheet('background-color:rgb(153,186,168);')
        self.buttonUst.setStyleSheet('background-color:rgb(153,186,168);')

        self.readData_bu1_flag = 0
        self.readData_bu2_flag = 0
        self.readData_bu3_flag = 0

        self.count_read_bu400 =-4
        self.count_read_bu50 =-4
        self.count_read_buses =-4

        self.centralwidget.setLayout(self.vbox)

        self.setCentralWidget(self.centralwidget)

        self.setObjectName("MainWindow")
        self.setWindowTitle(f'Калибратор {self.cur_elem}')
        self.show()
        # self.main.hide()

    def closeEvent(self,event):
        printf('closeEvent1')
        if self.th_unit:
            # self.th_unit.quit()
            # self.th_unit.wait(1)
            self.th_unit.setTerminationEnabled(True)
            self.th_unit.terminate()
            self.th_unit.wait(1)
        # del self.th_unit
        super().closeEvent(event)

    def UnitWidgetMain(self, i):
        printf('UnitW')
        if i ==0:
            self.UnitWidget()
        elif i ==1:
            self.UnitWidget2()
        else:
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
                self.button_obj[i].setStyleSheet('background-color:rgb(145,250,192);')
            else:
                self.button_obj[i].setChecked(False)
                self.button_obj[i].setDown(False)
                self.button_obj[i].setStyleSheet('background-color:rgb(153,173,232);')

        # self.buttonUnit1.setCheckable(True)
        # self.buttonUnit1.setDown(True)
        # self.buttonUnit2.setChecked(False)
        # self.buttonUnit2.setDown(False)
        # self.buttonUnit3.setChecked(False)
        # self.buttonUnit3.setDown(False)

        if self.readData_bu1_flag ==0:
            self.buttonAction2.setEnabled(False)
            self.buttonAction3.setEnabled(False)
        else:
            self.buttonAction2.setEnabled(True)
            self.buttonAction3.setEnabled(True)

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
                self.button_obj[i].setStyleSheet('background-color:rgb(145,250,192);')
            else:
                self.button_obj[i].setChecked(False)
                self.button_obj[i].setDown(False)
                self.button_obj[i].setStyleSheet('background-color:rgb(153,173,232);')

        # self.buttonUnit1.setChecked(False)
        # self.buttonUnit1.setDown(False)
        # self.buttonUnit2.setCheckable(True)
        # self.buttonUnit2.setDown(True)
        # self.buttonUnit3.setChecked(False)
        # self.buttonUnit3.setDown(False)

        if self.readData_bu2_flag ==0:
            self.buttonAction2.setEnabled(False)
            self.buttonAction3.setEnabled(False)
        else:
            self.buttonAction2.setEnabled(True)
            self.buttonAction3.setEnabled(True)

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
                self.button_obj[i].setStyleSheet('background-color:rgb(145,250,192);')
            else:
                self.button_obj[i].setChecked(False)
                self.button_obj[i].setDown(False)
                self.button_obj[i].setStyleSheet('background-color:rgb(153,173,232);')

        # self.buttonUnit1.setChecked(False)
        # self.buttonUnit1.setDown(False)
        # self.buttonUnit2.setChecked(False)
        # self.buttonUnit2.setDown(False)
        # self.buttonUnit3.setCheckable(True)
        # self.buttonUnit3.setDown(True)

        if self.readData_bu3_flag ==0:
            self.buttonAction2.setEnabled(False)
            self.buttonAction3.setEnabled(False)
        else:
            self.buttonAction2.setEnabled(True)
            self.buttonAction3.setEnabled(True)

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
        self.buttonUst.setStyleSheet('background-color:rgb(145,250,192);')
        self.buttonCalibr.setChecked(False)
        self.buttonCalibr.setDown(False)
        self.buttonCalibr.setStyleSheet('background-color:rgb(153,173,232);')
        self.buttonPar.setChecked(False)
        self.buttonPar.setDown(False)
        self.buttonPar.setStyleSheet('background-color:rgb(153,173,232);')

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
        self.buttonUst.setStyleSheet('background-color:rgb(153,173,232);')
        self.buttonCalibr.setCheckable(True)
        self.buttonCalibr.setDown(True)
        self.buttonCalibr.setStyleSheet('background-color:rgb(145,250,192);')
        self.buttonPar.setChecked(False)
        self.buttonPar.setDown(False)
        self.buttonPar.setStyleSheet('background-color:rgb(153,173,232);')

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
        self.buttonUst.setStyleSheet('background-color:rgb(153,173,232);')
        self.buttonCalibr.setChecked(False)
        self.buttonCalibr.setDown(False)
        self.buttonCalibr.setStyleSheet('background-color:rgb(153,173,232);')
        self.buttonPar.setCheckable(True)
        self.buttonPar.setDown(True)
        self.buttonPar.setStyleSheet('background-color:rgb(145,250,192);')

        # self.button.setEnabled(True) # Включаем кнопку, когда второе окно отображено
    def readData_bu1(self):
        # if not self.button_obj[1].isChecked() and not self.button_obj[2].isChecked():
        if self.button_obj[0].isChecked():
            self.worker = Worker(self.calibr_obj[0],'Чтение')
            self.worker.run1()
            self.thread_start(self.calibr_obj[0],self.cur_elem,self.lst_cb[0],'r')
            self.readData_bu1_flag = 1
            self.worker.window_abort.connect(lambda: self.progress_bar_stop('bu1'))
            # test
            # self.read_data_dict_bu400 = self.calibr_obj[0].test_data_dict('calibr')
            # self.unit_obj_preset[0].readData(self.read_data_dict_bu400, 'preset',1)
            # self.unit_obj_calibr[0].readData(self.read_data_dict_bu400, 'calibr',1)
            # self.readData_bu1_flag = 1
            self.buttonAction3.setEnabled(True)

    def readData_bu2(self):
        # printff('readData_bu50',self.buttonUnit2.isChecked())
        if self.button_obj[1].isChecked():
            self.worker = Worker(self.calibr_obj[1],'Чтение')
            self.worker.run1()
            self.thread_start(self.calibr_obj[1],self.cur_elem,self.lst_cb[1],'r')
            self.readData_bu2_flag = 1
            self.worker.window_abort.connect(lambda: self.progress_bar_stop('bu2'))
            # test
            # self.read_data_dict_bu50 = self.calibr_obj[1].test_data_dict('calibr')
            # self.unit_obj_preset[1].readData(self.read_data_dict_bu50, 'preset',1)
            # self.unit_obj_calibr[1].readData(self.read_data_dict_bu50, 'calibr',1)
            # self.readData_bu2_flag = 1
            self.buttonAction3.setEnabled(True)

    def readData_bu3(self):
        # printff('readData_buses',self.buttonUnit3.isChecked())
        if self.button_obj[2].isChecked():
            self.worker = Worker(self.calibr_obj[2],'Чтение')
            self.worker.run1()
            self.thread_start(self.calibr_obj[2],self.cur_elem,self.lst_cb[2],'r')
            self.readData_bu3_flag = 1
            self.worker.window_abort.connect(lambda: self.progress_bar_stop('bu3'))
            # test
            # self.read_data_dict_buses = self.calibr_obj[2].test_data_dict('calibr')
            # self.unit_obj_preset[2].readData(self.read_data_dict_buses, 'preset',1)
            # self.unit_obj_calibr[2].readData(self.read_data_dict_buses, 'calibr',1)
            # self.readData_bu3_flag = 1
            self.buttonAction3.setEnabled(True)

    def thread_start(self,obj, name_product,name_cb,mode):
        # self.th =ThreadCalibrator(self.testing)
        self.th =ThreadCalibrator(obj,name_product,name_cb,mode)
        self.th.start()
        # self.th.mysignal.connect(self.on_change,QtCore.Qt.QueuedConnection)
        # if self.th.flag_err =='ERR':
        #     printf()
        #     self.th.quit()
        self.th.finished_err.connect(self.signal_thread_stop)
        self.th.finished_abort.connect(self.signal_thread_abort)
        if mode =='r':
            self.th.finished2.connect(self.next_main_thread_read)
        else:
            self.th.finished2.connect(self.next_main_thread_write)

    # Сброс флага кнопки прервать в ноль
    def signal_thread_abort(self):
        printf('signal_thread_abort')
        for i,v in enumerate(self.lst_cb):
            self.calibr_obj[i].flag_abort =0

    # Сообщение об отсутствии com_port
    def signal_thread_stop(self):
        self.worker.flag_err_work=1
        # sign = Worker(self.data_dict_bu400)
        self.sign = warning.SignalErr('Нет связи с can!!!')

    def next_main_thread_read(self,name_product,name_cb):
        printf('next main thread read',name_cb)
        for i,v in enumerate(self.lst_cb):
            if name_cb ==v:
                self.count_read_bu400 += 4
                self.obj_cal_bu400 = self.calibr_obj[i]
                self.unit_obj_preset[i].readData(self.calibr_obj[i].data_dict,'preset',self.count_read_bu400)
                self.unit_obj_calibr[i].readData(self.calibr_obj[i].data_dict,'calibr',self.count_read_bu400)

        # if name_obj =='BU_50':
        #     self.count_read_bu50 += 4
        #     self.obj_cal_bu50 = self.calibr_obj[1]
        #     self.read_data_dict_bu50 = self.calibr_obj[1].data_dict
        #     self.unit_obj_preset[1].readData(self.read_data_dict_bu50,'preset',self.count_read_bu50)
        #     self.unit_obj_calibr[1].readData(self.read_data_dict_bu50,'calibr',self.count_read_bu50)
        # if name_obj =='BU_SES':
        #     self.count_read_buses += 4
        #     self.obj_cal_buses = self.calibr_obj[2]
        #     self.read_data_dict_buses = self.calibr_obj[2].data_dict
        #     self.unit_obj_preset[2].readData(self.read_data_dict_buses,'preset',self.count_read_buses)
        #     self.unit_obj_calibr[2].readData(self.read_data_dict_buses,'calibr',self.count_read_buses)
        #     # pass
        self.buttonAction2.setEnabled(True)
        self.buttonAction3.setEnabled(True)
        self.worker.time_stop()

    def next_main_thread_write(self,name_product,name_cb):
        printf('next main thread write',name_cb)
        # if name_product =='SES200M':
        for i,v in enumerate(self.lst_cb):
            if name_cb ==v:
                self.unit_obj_preset[i].writeData(self.calibr_obj[i].data_dict,'preset')
                data_dict = self.unit_obj_calibr[i].writeData(self.calibr_obj[i].data_dict,'calibr')
                self.calibr_obj[i].update_data_dict(data_dict)

        # if name_obj =='BU_50':
        #     self.unit_obj_preset[1].writeData(self.read_data_dict_bu50,'preset')
        #     data_dict = self.unit_obj_calibr[1].writeData(self.read_data_dict_bu50,'calibr')
        #     self.calibr_obj[1].update_data_dict(data_dict)
        # if name_obj =='BU_SES':
        #     self.unit_obj_preset[2].writeData(self.read_data_dict_buses,'preset')
        #     data_dict = self.unit_obj_calibr[2].writeData(self.read_data_dict_buses,'calibr')
        #     self.calibr_obj[2].update_data_dict(data_dict)
        # self.buttonAction2.setEnabled(True)
        # self.buttonAction3.setEnabled(True)
        self.worker.time_stop()
    # def on_change(self,s):
    #     self.unit_bu400_preset.readData(self.read_data_dict_bu400,'preset')
    #     self.unit_bu400_calibr.readData(self.read_data_dict_bu400,'calibr')

    def progress_bar_stop(self,cb):
        if cb =='bu1':
            self.calibr_obj[0].flag_abort =1
        elif cb =='bu2':
            self.calibr_obj[1].flag_abort =1
        elif cb =='bu3':
            self.calibr_obj[2].flag_abort =1


    def writeData_bu1(self):
        # if not self.button_obj[1].isChecked() and not self.button_obj[2].isChecked():
        if self.button_obj[0].isChecked():
            self.unit_obj_preset[0].writeData(self.calibr_obj[0].data_dict,'preset')
            data_dict = self.unit_obj_calibr[0].writeData(self.calibr_obj[0].data_dict,'calibr')
            self.calibr_obj[0].update_data_dict(data_dict)
            self.worker = Worker(self.calibr_obj[0],'Запись')
            self.worker.run1()
            self.thread_start(self.calibr_obj[0],self.cur_elem,self.lst_cb[0],'w')
            self.worker.window_abort.connect(lambda: self.progress_bar_stop('bu1'))

    def writeData_bu2(self):
        if self.button_obj[1].isChecked():
            # self.unit_bu50_preset.writeData(self.read_data_dict_bu50,'preset')
            # data_dict = self.unit_bu50_calibr.writeData(self.read_data_dict_bu50,'calibr')
            # self.data_dict_bu50.update_data_dict(data_dict)
            self.unit_obj_preset[1].writeData(self.calibr_obj[1].data_dict,'preset')
            data_dict = self.unit_obj_calibr[1].writeData(self.calibr_obj[1].data_dict,'calibr')
            self.calibr_obj[1].update_data_dict(data_dict)
            self.worker = Worker(self.calibr_obj[1],'Запись')
            self.worker.run1()
            self.thread_start(self.calibr_obj[1],self.cur_elem,self.lst_cb[1],'w')
            self.worker.window_abort.connect(lambda: self.progress_bar_stop('bu2'))

    def writeData_bu3(self):
        if self.button_obj[2].isChecked():
            # self.unit_buses_preset.writeData(self.read_data_dict_buses,'preset')
            # data_dict = self.unit_buses_calibr.writeData(self.read_data_dict_buses,'calibr')
            # self.data_dict_buses.update_data_dict(data_dict)
            self.unit_obj_preset[2].writeData(self.calibr_obj[2].data_dict,'preset')
            data_dict = self.unit_obj_calibr[2].writeData(self.calibr_obj[2].data_dict,'calibr')
            self.worker = Worker(self.calibr_obj[2],'Запись')
            self.worker.run1()
            self.thread_start(self.calibr_obj[2],self.cur_elem,self.lst_cb[2],'w')
            self.worker.window_abort.connect(lambda: self.progress_bar_stop('bu3'))

    def saveData_bu1(self):
        printf('saveData_bu1')
        if self.button_obj[0].isChecked():
            self.cnt_save_data+=1
            self.number_product = number_product.NumberProduct()
            self.number_product.signal_numb.connect(self.nmb_product_bu1)

    def nmb_product_bu1(self,text):
        if self.button_obj[0].isChecked():
            self.worker = Worker(self.unit_obj_preset[0],'Сохранение')
            self.worker.run1()
            self.th_unit  = ThreadUnit(self.calibr_obj[0],self.unit_obj_preset[0],self.unit_obj_calibr[0],\
                                       'preset','calibr', 'filter',self.lst_cb[0],self.cur_elem,text)

            self.th_unit.start()
            self.unit_obj_calibr[0].saveDataval()
            if self.cnt_save_data == 3:
                self.cnt_save_data = 0
                self.unit_obj_calibr[0].saveDatapdf(self.cur_elem,self.unit_obj_calibr,text)
                self.unit_obj_calibr[0].saveDatapdf(self.cur_elem,self.unit_obj_calibr,text,2)

            # self.unit_obj_preset[0].saveData(self.calibr_obj[0],'preset',self.lst_cb[0],self.cur_elem,text)
            # self.unit_obj_calibr[0].saveData(self.calibr_obj[0],'calibr',self.lst_cb[0],self.cur_elem,text)
            # self.unit_obj_calibr[0].saveData(self.calibr_obj[0],'filter',self.lst_cb[0],self.cur_elem,text)
            # self.th_unit  = ThreadUnit(self.calibr_obj[0],self.unit_obj_preset[0],self.unit_obj_calibr[0],'preset','calibr',\
            #                            'filter',self.lst_cb[0],self.cur_elem,text)
            # self.th_unit.start()
            # self.th_unit.finished_th_unit.connect(self.signal_thread_unit_stop)
            #test
            # self.worker = Worker(self.unit_obj_calibr[0],'Сохранение')
            # self.worker.run1()
            # # self.unit_obj_preset[0].saveDatatest('preset',self.lst_cb[0],self.cur_elem,text)
            # # self.unit_obj_calibr[0].saveDatatest('calibr',self.lst_cb[0],self.cur_elem,text)
            # self.unit_obj_calibr[0].saveDataval()
            # self.unit_obj_calibr[1].saveDataval()
            # self.unit_obj_calibr[2].saveDataval()
            # self.unit_obj_calibr[0].saveDatapdf(self.cur_elem,self.unit_obj_calibr,text)
            # self.unit_obj_calibr[0].saveDatapdf(self.cur_elem, self.unit_obj_calibr, text,2)
        # printf('text',text)

    # if i == 0:
    #     t.setStyle(TableStyle([
    #         ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    #         ('SPAN', (0, 1), (0, 6)), ('SPAN', (0, 7), (0, 18)), ('SPAN', (0, 19), (0, 30)),
    #         ('SPAN', (0, 31), (0, 36)), ('SPAN', (0, 37), (0, 48)), ('SPAN', (0, 49), (0, 54)),
    #         ('SPAN', (0, 55), (0, 56)), ('SPAN', (0, 57), (0, 58)), ('SPAN', (0, 59), (0, 60)),
    #         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #         ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
    #     story.append(p,bin1)
    #     story.append(p2)
    #     story.append(p_bu1)
    # elif i == 1:
    #     t.setStyle(TableStyle([
    #         ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    #         ('SPAN', (0, 1), (0, 9)), ('SPAN', (0, 10), (0, 18)),
    #         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #         ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

    def saveData_bu2(self):
        if self.button_obj[1].isChecked():
            self.cnt_save_data+=1
            self.number_product = number_product.NumberProduct()
            self.number_product.signal_numb.connect(self.nmb_product_bu2)

    def nmb_product_bu2(self,text):
        if self.button_obj[1].isChecked():
            self.worker = Worker(self.unit_obj_preset[1],'Сохранение')
            self.worker.run1()
            self.th_unit = ThreadUnit(self.calibr_obj[1],self.unit_obj_preset[1],self.unit_obj_calibr[1],\
                                       'preset','calibr', 'filter',self.lst_cb[1],self.cur_elem,text)

            self.th_unit.start()
            self.unit_obj_calibr[1].saveDataval()
            if self.cnt_save_data == 3:
                self.cnt_save_data = 0
                self.unit_obj_calibr[0].saveDatapdf(self.cur_elem,self.unit_obj_calibr,text)
                self.unit_obj_calibr[0].saveDatapdf(self.cur_elem,self.unit_obj_calibr,text,2)

            # self.unit_obj_preset[1].saveData(self.calibr_obj[1],'preset',self.lst_cb[1],self.cur_elem,text)
            # self.unit_obj_calibr[1].saveData(self.calibr_obj[1],'calibr',self.lst_cb[1],self.cur_elem,text)
            # self.unit_obj_calibr[1].saveData(self.calibr_obj[1],'filter',self.lst_cb[1],self.cur_elem,text)

    def saveData_bu3(self):
        if self.button_obj[2].isChecked():
            self.cnt_save_data += 1
            self.number_product = number_product.NumberProduct()
            self.number_product.signal_numb.connect(self.nmb_product_bu3)

    def nmb_product_bu3(self,text):
        if self.button_obj[2].isChecked():
            self.worker = Worker(self.unit_obj_preset[2],'Сохранение')
            self.worker.run1()
            self.th_unit  = ThreadUnit(self.calibr_obj[2],self.unit_obj_preset[2],self.unit_obj_calibr[2],\
                                       'preset','calibr','filter',self.lst_cb[2],self.cur_elem,text)

            self.th_unit.start()
            self.unit_obj_calibr[2].saveDataval()
            if self.cnt_save_data == 3:
                self.cnt_save_data = 0
                self.unit_obj_calibr[0].saveDatapdf(self.cur_elem,self.unit_obj_calibr,text)
                self.unit_obj_calibr[0].saveDatapdf(self.cur_elem, self.unit_obj_calibr, text, 2)
            # self.unit_obj_preset[2].saveData(self.calibr_obj[2],'preset',self.lst_cb[2],self.cur_elem,text)
            # self.unit_obj_calibr[2].saveData(self.calibr_obj[2],'calibr',self.lst_cb[2],self.cur_elem,text)
            # self.unit_obj_calibr[2].saveData(self.calibr_obj[2],'filter',self.lst_cb[2],self.cur_elem,text)

    def signal_thread_unit_stop(self):
        printf('signa_unit_stop')
        # self.th_unit.quit()
        # self.th_unit.wait(1000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # ex = Main('SES200M')
    ex = ComPort()
    ex.show()
    sys.exit(app.exec_())
    # sys.exit(0)
    # app.exec_()
