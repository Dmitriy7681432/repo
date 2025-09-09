# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QLineEdit, QApplication,QPushButton,QDesktopWidget)
from PyQt5 import QtGui,QtCore
from PyQt5 import QtWidgets
import sys
from PyQt5.QtCore import QObject, pyqtSignal,Qt

class NumberProduct(QObject):
    signal_numb = pyqtSignal(list)
    cur_elem = 0
    nmb_product =0
    nmb_cb = 0

    def __init__(self,app = False):
        if app:
            app = QApplication(sys.argv)
        super().__init__()
        self.widget = QWidget()
        self.widget.setWindowTitle("Зав.№ изделия и блока")
        self.widget.setGeometry(100, 100, 400, 200)

        #Шрифт
        font_lbl = QtGui.QFont()
        font_lbl.setFamily("Times New Roman")
        font_lbl.setPointSize(14)
        font_lbl.setWeight(75)
        # font.setBold(True)

        font_line = QtGui.QFont()
        font_line.setFamily("Times New Roman")
        font_line.setPointSize(14)

        label_product = 'Введите заводской номер изделия'
        self.lbl = QLabel(label_product, self.widget)
        self.lbl.move(20, 10)
        self.lbl.setFont(font_lbl)

        line_product = QLineEdit(self.widget)
        # line.addItems(lst_combo)
        line_product.move(20,30)
        line_product.setFont(font_line)
        line_product.resize(350,30)
        line_product.setPlaceholderText('Пример: Н06001')

        label_cb = 'Введите заводской номер блока'
        self.lbl = QLabel(label_cb, self.widget)
        self.lbl.move(20,70)
        self.lbl.setFont(font_lbl)

        line_cb = QLineEdit(self.widget)
        line_cb.move(20,90)
        line_cb.setFont(font_line)
        line_cb.resize(350,30)
        line_cb.setPlaceholderText('Пример: Н06001')

        self.center()

        # self.move(x_, y_)
        line_product.textChanged[str].connect(self.onActivated_product)
        line_cb.textChanged[str].connect(self.onActivated_cb)

        self.open_button = QPushButton("OK", self.widget)
        self.open_button.clicked.connect(self.closeOk)
        self.open_button.move(150, 150)
        self.open_button.setFont(font_lbl)

        # Цветовой фон
        pal = self.widget.palette()
        # Если use 1-й аргумент, то цвет будет пропадать при переходе на др окно
        # pal.setColor(QtGui.QPalette.Window, QtGui.QColor(191, 245, 234))
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor(220, 254, 225))
        self.widget.setPalette(pal)
        self.widget.setWindowModality(QtCore.Qt.ApplicationModal)
        self.widget.show()

        # self.cur_elem = line.text()

        if app:
            sys.exit(app.exec_())

    def center(self):
        qr = self.widget.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.widget.move(qr.topLeft())
    def onActivated_product(self, text):
        self.nmb_product= text

    def onActivated_cb(self, text):
        self.nmb_cb = text
        # self.lbl.adjustSize()

    def closeOk(self):
        # self.second_window = Main(self.cur_elem)
        # self.second_window.show()
        lst_nmb = []
        lst_nmb.append(self.nmb_product)
        lst_nmb.append(self.nmb_cb)
        self.signal_numb.emit(lst_nmb)
        self.widget.close()  # Закрывает текущее (первое) окно
