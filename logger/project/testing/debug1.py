# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QApplication,
                             QAction, QWidget)
# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets
#
#
# class MyTab(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super(MyTab, self).__init__()
#         self.parent = parent
#         self.rows = [
#             ('10.16.26.25', 2),
#             ('10.16.26.26', 3),
#             ('10.16.26.27', 1),
#             ('10.16.26.28', 4)
#         ]
#         self.lineEdit = QtWidgets.QLineEdit(
#             placeholderText='Введите номер из 4х цифр')
#
#         self.pushButton = QtWidgets.QPushButton('Создать TableWidget')
#         self.pushButton.clicked.connect(self.func_connect)
#
#         self.tableWidget = QtWidgets.QTableWidget(0, 4)
#         self.tableWidget.setHorizontalHeaderLabels(
#             ['IP', 'Number', 'SSH', 'VNC'])
#         self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
#
#         vbox = QtWidgets.QVBoxLayout(self)
#         vbox.addWidget(self.tableWidget)
#         vbox.addWidget(self.lineEdit)
#         vbox.addWidget(self.pushButton)
#
#     def func_connect(self):
#         num = self.lineEdit.text()
#         if not num.isdigit():
#             self.parent.statusBar().showMessage(
#                 'Достустимо вводить только цифры, номер состоит из 4х цифр')
#             return
#         if len(num) != 4:
#             self.parent.statusBar().showMessage('Номер состоит из 4х цифр, повторите ввод.')
#             return
#         self.parent.statusBar().showMessage('')
#
#         self.tableWidget.setRowCount(len(self.rows))
#         for row, items in enumerate(self.rows):
#             self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(items[0]))
#             self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(items[1])))
#             button = QtWidgets.QPushButton(f'SSH {row}')
#             button.clicked.connect(lambda ch, ip=items[0], n=items[1], btn=button: \
#                                        self.button_pushed_SSH(ip, n, btn))
#             self.tableWidget.setCellWidget(row, 2, button)
#
#             button = QtWidgets.QPushButton(f'VNC {row}')
#             button.clicked.connect(lambda ch, ip=items[0], n=items[1], btn=button: \
#                                        self.button_pushed_VNC(ip, n, btn))
#             self.tableWidget.setCellWidget(row, 3, button)
#         self.tableWidget.setSortingEnabled(True)
#
#     def button_pushed_SSH(self, ip, n, btn):
#         print(f'{btn.text()}: ip={ip}, n={n}, lineEdit={self.lineEdit.text()}')
#
#     def button_pushed_VNC(self, ip, n, btn):
#         print(f'{btn.text()}: ip={ip}, n={n}, lineEdit={self.lineEdit.text()}')
#
#
# class MyWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.centralwidget = QtWidgets.QWidget()
#         self.setCentralWidget(self.centralwidget)
#
#         # + vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#         self.tabWidget = QtWidgets.QTabWidget()
#         count = self.tabWidget.count()
#         self.nb = QtWidgets.QToolButton(text="Добавить", autoRaise=True)
#         self.nb.clicked.connect(self.new_tab)
#         self.tabWidget.insertTab(count, QtWidgets.QWidget(), "")
#         self.tabWidget.tabBar().setTabButton(
#             count, QtWidgets.QTabBar.RightSide, self.nb)
#
#         self.new_tab()
#
#         self.layout = QtWidgets.QGridLayout(self.centralwidget)
#         self.layout.addWidget(self.tabWidget)
#
#         self.statusBar().showMessage('Message in statusbar. '
#                                      'Будет Скрыто через 5000 миллисекунд - 5 секунды! ', 5000)
#
#     def new_tab(self):
#         index = self.tabWidget.count() - 1
#         tabPage = MyTab(self)
#         self.tabWidget.insertTab(index, tabPage, f"Tab {index}")
#         self.tabWidget.setCurrentIndex(index)
#         tabPage.lineEdit.setFocus()
#
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     app.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
#     win = MyWindow()
#     win.resize(640, 480)
#     win.show()
#     sys.exit(app.exec_())

#График в pyqt
# from PyQt5 import Qt
# import pyqtgraph as pg
# import numpy as np
#
#
# class Window(Qt.QWidget):
#
#     def __init__(self):
#         super().__init__()
#
#         layout = Qt.QVBoxLayout(self)
#
#         self.view = view = pg.PlotWidget()
#         self.curve = view.plot(name="Line")
#
#         self.btn = Qt.QPushButton("Random plot")
#         self.btn.clicked.connect(self.random_plot)
#
#         layout.addWidget(Qt.QLabel("Some text"))
#         layout.addWidget(self.view)
#         layout.addWidget(self.btn)
#
#     def random_plot(self):
#         random_array = np.random.random_sample(20)
#         self.curve.setData(random_array)
#
#
# if __name__ == "__main__":
#     app = Qt.QApplication([])
#     w = Window()
#     w.show()
#     app.exec()
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)

from PyQt5 import QtCore, QtGui, QtWidgets

class Example(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.main = QtWidgets.QMainWindow()
        self.centralwidget_1 = QtWidgets.QWidget(self.main)
        self.centralwidget = QtWidgets.QWidget(self.centralwidget_1)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 0, 0))

        hbox_port = QHBoxLayout(self.centralwidget)
        label_com = QtWidgets.QLabel()
        label_com.setText("Выбор порта")
        com_port = QtWidgets.QComboBox()
        hbox_port.addWidget(label_com)
        hbox_port.addWidget(com_port)

        # self.centralwidget_2 = QtWidgets.QWidget(self.main)
        # self.centralwidget1 = QtWidgets.QWidget(self.centralwidget_2)
        # self.centralwidget1.setGeometry(QtCore.QRect(20, 20, 20, 20))
        # hbox_cb = QHBoxLayout(self.centralwidget1)
        # label_cb = QtWidgets.QLabel("Выбор изделия")
        # cb = QtWidgets.QComboBox()
        # hbox_cb.addWidget(label_cb)
        # hbox_cb.addWidget(cb)
        #
        # self.centralwidget_3 = QtWidgets.QWidget(self.main)
        # self.centralwidget2 = QtWidgets.QWidget(self.centralwidget_3)
        # self.centralwidget2.setGeometry(QtCore.QRect(30, 30, 30, 30))
        # hbox_lb_file = QHBoxLayout(self.centralwidget)
        # label_file = QtWidgets.QLabel()
        # label_file.setText("Файл настройки")
        # hbox_lb_file.addWidget(label_file)
        #
        # self.centralwidget_4 = QtWidgets.QWidget(self.main)
        # self.centralwidget3 = QtWidgets.QWidget(self.centralwidget_3)
        # self.centralwidget3.setGeometry(QtCore.QRect(30, 30, 30, 30))
        # hbox_file = QHBoxLayout(self.centralwidget3)
        # edit_file = QtWidgets.QLineEdit()
        # save_file =QtWidgets.QPushButton()
        # save_file.setText("Сохранить")
        # hbox_file.addWidget(edit_file)
        # hbox_file.addWidget(save_file)
        #
        # self.centralwidget.raise_()
        # self.centralwidget1.raise_()
        # self.centralwidget2.raise_()
        # self.centralwidget3.raise_()
        self.setLayout(hbox_port)
        #
        self.setGeometry(650, 350, 700, 550)
        self.setWindowTitle('logger')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())