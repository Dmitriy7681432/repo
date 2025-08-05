# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QVBoxLayout, QProgressBar, QPushButton)
from PyQt5.QtCore import QBasicTimer
from test1 import Testing,Connect
import asyncio
from PyQt5 import QtCore, QtWidgets

class MyThread(QtCore.QThread):
    # mysignal = QtCore.pyqtSignal(str)

    def __init__(self,obj):
        super().__init__()
        self.obj = obj

    def run(self):
        # i =0
        # for i in range(1, 21):
        print('Thread start')
        # testing = Testing(self.arg)
        # testing.while_func()
        self.obj.while_func('r')
        # while True:
        #     print('Thread start')
            # i+=1
            # self.sleep(1)  # "Засыпаем" на 3 секунды
            # Передача данных из потока через сигнал
            # self.mysignal.emit("i = %s" % i)
            # self.mysignal.emit('%s' %i)

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.ser = Connect()
        self.arg = Testing(self.ser.ser, 'SES200M', 'BU_400')

    def initUI(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(70, 80, 200, 25)

        self.btn = QPushButton('Начать', self)
        self.btn.move(30, 80)
        self.btn.clicked.connect(self.doAction)
        self.btn1 = QPushButton('Тест', self)
        self.btn1.move(70, 80)
        self.btn1.clicked.connect(self.test_thread)

        self.timer = QBasicTimer()
        self.step = 0

        layout = QVBoxLayout()
        layout.addWidget(self.pbar)
        layout.addWidget(self.btn)
        layout.addWidget(self.btn1)
        self.setLayout(layout)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Прогресс бар')
        self.show()

    def test_func(self):
        asyncio.run(Testing.wh_func())

    def test_thread(self):
        self.th = MyThread(self.arg)
        self.th.start()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Закончено')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        print('doAction', self.timer.isActive())
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Начать')
        else:
            self.timer.start(100, self)
            self.btn.setText('Стоп')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    # ex.show()
    sys.exit(app.exec_())
