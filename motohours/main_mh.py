# -*- coding: utf-8 -*-
# Модули библиотечные
import sys,serial,struct,math
import time,json

from PyQt5.QtWidgets import (QWidget, QPushButton, QStackedWidget, QToolBar, QToolButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QAction, QMainWindow,QDialog,QLabel,QProgressBar,
                             QDesktopWidget,QLineEdit,QGridLayout,QSpacerItem, QSizePolicy)

from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot,QTimer,QBasicTimer, QRegularExpression
import serial.tools.list_ports
from PyQt5.QtGui import QRegularExpressionValidator

from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication)
# Модули разработчика
from pars_mh_init_h import ParsInitMh
from read_mh import ReadDataMh
from write_mh import WriteDataMh
import warning_mh,subprocess_mh
from debug_mh import *

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
        # printf('updata_pr')
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
        # printf('doAction', self.timer.isActive())
        if self.timer.isActive():
            self.timer.stop()
            # self.btn.setText('Начать')
        else:
            self.val = 0
            self.timer.start(1000, self)
            # self.btn.setText('Стоп')

class ThreadCalibrator(QtCore.QThread):
    finished2 = pyqtSignal()
    mysignal = QtCore.pyqtSignal()
    flag_err = 0
    finished_err = pyqtSignal()
    finished_abort = pyqtSignal()

    def __init__(self, obj_method):
        super().__init__()
        self.obj_method = obj_method

    def run(self):
        i = 1
        self.flag_err = self.obj_method()
        # self.obj.trigger.emit()
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
            self.finished2.emit()
        # self.finished2.emit()
class ComPort(QWidget):
    def __init__(self):
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
        self.resize(x_size_desktop, y_size_desktop)
        # Вывод окна по центру
        x_ = (desktop.width() - self.frameSize().width()) // 2
        y_ = (desktop.height() - self.frameSize().height()) // 2
        self.move(x_, y_)

        combo = QComboBox(self)
        lst_combo = []
        label = 'Выберите изделие:'
        # Чтение данных с configs
        with open('configs.json', 'r') as file_configs:
            self.configs = json.load(file_configs)
            self.product = self.configs.get('default_product')
            if self.product=='SES200M':
                lst_combo = ['SES200M','SEP30M_BUSEP','SEP30M_BU400','SES150','TOR_ARCTICA']
            elif self.product =='SEP30M_BUSEP':
                lst_combo = ['SEP30M_BUSEP','SEP30M_BU400','SES200M','SES150','TOR_ARCTICA']
            elif self.product == 'SEP30M_BU400':
                lst_combo = ['SEP30M_BU400', 'SEP30M_BUSEP', 'SES200M', 'SES150', 'TOR_ARCTICA']
            elif self.product =='SES150':
                lst_combo = ['SES150','SEP30M_BU400', 'SEP30M_BUSEP', 'SES200M', 'TOR_ARCTICA']
            else:
                lst_combo = ['TOR_ARCTICA','SES150','SEP30M_BU400', 'SEP30M_BUSEP', 'SES200M']

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

        # Вызов парсера наименования параметров наработки памяти
        self.name_params_mh = ParsInitMh(self.cur_elem).pars()
        print(self.name_params_mh)
        # self.com = ComPort()
        # self.com.show()

        self.read_obj =ReadDataMh(len(self.name_params_mh))

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

        self.version = QLabel(f'<i>{self.cur_elem} version: 1.0.5  </i>')
        self.version.setFont(font)
        self.version.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter )
        self.version.setStyleSheet('color: rgba(105,105,105,0.5)')
        # Кнопки действия
        self.buttonAction1 = QToolButton()
        self.buttonAction1.setText('Считать')
        self.buttonAction2 = QToolButton()
        self.buttonAction2.setText('Записать')
        self.buttonAction1.setFont(font)
        self.buttonAction2.setFont(font)
        self.buttonAction1.setMaximumSize(QtCore.QSize(500, 30))
        self.buttonAction2.setMaximumSize(QtCore.QSize(600, 30))
        self.buttonAction1.setObjectName("buttonAction1")
        self.buttonAction2.setObjectName("buttonAction2")
        self.buttonAction1.setStyleSheet('background-color:rgb(255,240,157);')
        self.buttonAction2.setStyleSheet('background-color:rgb(255,240,157);')

        self.lblLayout = QHBoxLayout()
        self.lblLayout.setGeometry(QtCore.QRect(20,20,20,20))
        self.lblLayout.setObjectName("lblLayout")
        self.lblLayout.addWidget(self.version)
        self.actionLayout = QHBoxLayout()

        self.actionLayout.setContentsMargins(0, 0, 0, 0)
        self.actionLayout.setSpacing(0)
        self.actionLayout.setObjectName("actionLayout")
        self.actionLayout.addWidget(self.buttonAction1)
        self.actionLayout.addWidget(self.buttonAction2)



        font_lbl = QtGui.QFont()
        font_lbl.setFamily("Times New Roman")
        font_lbl.setPointSize(14)
        font_lbl.setWeight(75)
        # font.setBold(True)

        font_line = QtGui.QFont()
        font_line.setFamily("Times New Roman")
        font_line.setPointSize(14)

        self.mh_hbox = []
        self.gridlayout =QGridLayout()

        # spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.gridlayout.addItem(spacer, 0, 0)
        # Строки наработки
        for i, name in enumerate(self.name_params_mh):
            self.lbl = QLabel(name)
            # self.lbl.move(20, 10)
            self.lbl.setFont(font_lbl)
            self.mh_sec = QLineEdit()
            # line.addItems(lst_combo)
            # self.mh_sec.move(20, 30)
            self.mh_sec.setFont(font_line)
            # self.mh_sec.resize(350, 30)
            self.mh_sec.setPlaceholderText('сек')
            self.mh_sec.setMaximumWidth(200)
            self.lbl_sec = QLabel('сек')
            self.lbl_sec.setFont(font_lbl)
            self.mh_hour = QLineEdit()
            # self.mh_hour.move(20 90)
            self.mh_hour.setFont(font_line)
            # self.mh_hour.resize(350, 30)
            self.mh_hour.setPlaceholderText('ч')
            self.mh_hour.setMaximumWidth(100)
            self.lbl_hour = QLabel('ч')
            self.lbl_hour.setFont(font_lbl)
            # Вставить только числа
            rx = QRegularExpression("[0-9]+")
            validator = QRegularExpressionValidator(rx)
            self.mh_sec.setValidator(validator)
            self.mh_hour.setValidator(validator)

            self.gridlayout.addWidget(self.lbl,i,0)
            self.gridlayout.addWidget(self.mh_sec,i,1)
            # self.gridlayout.setColumnStretch(1,2)
            self.gridlayout.addWidget(self.lbl_sec,i,2)
            self.gridlayout.addWidget(self.mh_hour,i,3)
            self.gridlayout.addWidget(self.lbl_hour,i,4)
            self.gridlayout.setHorizontalSpacing(5)
            # self.gridlayout.setColumnMinimumWidth(1,50)

        self.vbox.addLayout(self.gridlayout)
        # self.vbox.setAlignment(self.gridlayout, QtCore.Qt.AlignLeft)
        self.vbox.addStretch()
        self.vbox.setContentsMargins(0, 50, 0, 0)
        self.vbox.setSpacing(0)
        self.vbox.addLayout(self.lblLayout)
        self.vbox.addLayout(self.actionLayout)

        self.buttonAction1.clicked.connect(self.readData)
        self.buttonAction2.clicked.connect(self.writeData)

        self.centralwidget.setLayout(self.vbox)

        self.setCentralWidget(self.centralwidget)

        self.setObjectName("MainWindow")
        self.setWindowTitle(f'Калибратор {self.cur_elem}')
        self.show()

    def thread_start(self,obj_method,mode):
        self.th =ThreadCalibrator(obj_method)
        # self.read_obj.moveToThread(self.th)
        # self.read_obj.trigger.connect(self.read_obj.read)
        self.th.start()
        self.th.finished_err.connect(self.signal_thread_stop)
        self.th.finished_abort.connect(self.signal_thread_abort)
        if mode =='r':
            self.th.finished2.connect(self.next_main_thread_read)
        else:
            self.th.finished2.connect(self.next_main_thread_write)

    def signal_thread_abort(self):
        self.read_obj.flag_abort =0

    # Сообщение об отсутствии com_port
    def signal_thread_stop(self):
        self.worker.flag_err_work=1
        self.sign = warning_mh.SignalErr('Нет соединения !!!')
    def next_main_thread_read(self):
        cnt_sec=1
        cnt_hour=3
        for indx, value in enumerate(self.read_obj.value_list):
            self.gridlayout.itemAt(indx+cnt_sec).widget().setText(str(value))
            self.gridlayout.itemAt(indx+cnt_hour).widget().setText(str(math.floor(value/3600)))
            cnt_sec+=4
            cnt_hour+=4

        self.worker.time_stop()

    def next_main_thread_write(self):
        # for indx, value in enumerate(self.read_obj.value_list):
        #     self.mh_hbox[indx].itemAt(3).widget().setText(str(value))
        #     self.mh_hbox[indx].itemAt(5).widget().setText(str(value/3600))
        self.worker.time_stop()
    def readData(self):
        self.worker = Worker(self.read_obj, 'Чтение')
        self.worker.run1()

        self.subprocess_mh = subprocess_mh.SubprocessMh(self.cur_elem,'read')
        self.subprocess_mh.finished_success.connect(lambda: self.on_success('read'))
        self.subprocess_mh.finished_with_error.connect(self.on_error)
        self.subprocess_mh.start()

    def writeData(self):
        cnt_sec=1
        flag =0
        list_interface_params =[]

        self.read_obj.read()
        if len(self.read_obj.data_list)*4 >0x20:
            self.read_obj.clear_data_list()
            flag =1
        for indx, value in enumerate(self.read_obj.value_list):
            list_interface_params.append(int(self.gridlayout.itemAt(indx+cnt_sec).widget().text()))
            cnt_sec+=4
        self.read_obj.data_list.extend(list_interface_params)

        # self.write_obj =WriteDataMh(self.cur_elem,len(self.name_params_mh),
        #                             self.read_obj.data_list)
        self.write_obj =WriteDataMh(self.read_obj.data_list)

        self.worker = Worker(self.write_obj, 'Запись')
        self.worker.run1()
        self.thread_start(self.write_obj.write,'w')

        if flag ==0:
            self.subprocess_mh = subprocess_mh.SubprocessMh(self.cur_elem,'write')
            self.subprocess_mh.finished_success.connect(lambda: self.on_success('write'))
            self.subprocess_mh.finished_with_error.connect(self.on_error)
            self.subprocess_mh.start()
        else:
            self.subprocess_mh = subprocess_mh.SubprocessMh(self.cur_elem,'erase')
            self.subprocess_mh.finished_success.connect(lambda: self.on_success('erase'))
            self.subprocess_mh.finished_with_error.connect(self.on_error)
            self.subprocess_mh.start()
            flag =0

        self.worker.window_abort.connect(self.progress_bar_stop)

    def progress_bar_stop(self):
        self.read_obj.flag_abort =1

    def on_success(self, mode):
        # QMessageBox.information(self, "Успех", f"Процесс завершен успешно:\n\n{output}")
        if mode =='read':
            self.thread_start(self.read_obj.read,'r')
        else:
            self.thread_start(self.write_obj.write, 'w')

        self.worker.window_abort.connect(self.progress_bar_stop)

    def on_error(self, error_message):
        # Выводим окно с ошибкой в главном GUI потоке
        # QMessageBox.critical(self, "Ошибка таймаута", error_message)
        self.worker.flag_err_work=1
        self.sign = warning_mh.SignalErr('Нет соединения !!!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # ex = Main('SES200M')
    ex = ComPort()
    ex.show()
    sys.exit(app.exec_())
