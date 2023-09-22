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

# График в pyqt
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
        # self.main = QtWidgets.QMainWindow()
        # self.main.setObjectName("MainWindow")
        # self.main.resize(700,500)

        self.setObjectName("MainWindow")
        #Вычисляемы размер экрана
        desktop = QtWidgets.QApplication.desktop()
        x = desktop.width(); y = desktop.height()
        x = int(x/1.7); y = int(y/1.3)
        self.resize(x, y)
        #Вывод окна по центру
        x_ = (desktop.width() - self.frameSize().width()) // 2
        y_ = (desktop.height() - self.frameSize().height()) // 2
        self.move(x_, y_)


        #Фон картинки
        # self.setAutoFillBackground(False)
        # self.setStyleSheet("background-image: url(space.jpeg);")
        # self.setStyleSheet("background-image: url(fon.jpg);")

        #Фон картинки
        # palette = QtGui.QPalette()
        # img = QtGui.QImage('fon.jpg')
        # scaled = img.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, transformMode=QtCore.Qt.SmoothTransformation) # palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(scaled)) # self.setPalette(palette)

        #Цветовой фон
        pal = self.palette()
        # Если use 1-й аргумент, то цвет будет пропадать при переходе на др окно
        pal.setColor(QtGui.QPalette.Window,QtGui.QColor(191,245,234))
        self.setPalette(pal)

        # Меню и толбары

        self.start = QAction(QtGui.QIcon('./icons/start.png'), 'Запуск логгера', self)
        self.toolbar = self.addToolBar("")
        self.toolbar.addAction(self.start)
        self.stop = QAction(QtGui.QIcon('./icons/stop2.png'), 'Остановить логгер', self)
        self.toolbar = self.addToolBar("")
        self.toolbar.addAction(self.stop)
        self.record = QAction(QtGui.QIcon('./icons/record3.png'), 'Запись данных', self)
        self.toolbar = self.addToolBar("")
        self.toolbar.addAction(self.record)

        # self.statusBar()
        # menubar = self.menuBar()
        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(exitAction)
        # self.newAcntion = QAction(self)
        # self.newAcntion.setIcon(QtGui.QIcon(":start.png"))

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralWidget")

        #Узнать доступные стили окна
        # print(QtWidgets.QStyleFactory.keys())

        #Шрифт
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        # Порт
        self.horizontWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontWidget.setGeometry(QtCore.QRect(20, 20, 210, 40))
        self.horizontWidget.setObjectName("horizontWidget")
        self.horizontLayout = QtWidgets.QHBoxLayout(self.horizontWidget)
        self.horizontLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontLayout.setObjectName("horizontLayout")
        self.label_com = QtWidgets.QLabel()
        self.label_com.setFont(font)
        self.label_com.setObjectName("label_com")
        self.label_com.setText("Выбор порта:")
        self.horizontLayout.addWidget(self.label_com)
        self.com_port = QtWidgets.QComboBox()
        self.com_port.setObjectName("com_port")
        self.horizontLayout.addWidget(self.com_port)

        # Изделие
        self.horizontWidget_1 = QtWidgets.QWidget(self.centralwidget)
        self.horizontWidget_1.setGeometry(QtCore.QRect(20, 80, 230, 40))
        self.horizontWidget_1.setObjectName("horizontWidget_1")
        self.horizontLayout_1 = QtWidgets.QHBoxLayout(self.horizontWidget_1)
        self.horizontLayout_1.setContentsMargins(0, 0, 0, 0)
        self.horizontLayout_1.setObjectName("horizontLayout_1")
        self.label_cb = QtWidgets.QLabel()
        self.label_cb.setFont(font)
        self.label_cb.setObjectName("label_cb")
        self.label_cb.setText("Выбор изделия:")
        self.horizontLayout_1.addWidget(self.label_cb)
        self.cb = QtWidgets.QComboBox()
        self.cb.setObjectName("cb")
        self.horizontLayout_1.addWidget(self.cb)

        # Файл настроек
        self.horizontWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontWidget_2.setGeometry(QtCore.QRect(20, 140, 160, 40))
        self.horizontWidget_2.setObjectName("horizontWidget_2")
        self.horizontLayout_2 = QtWidgets.QHBoxLayout(self.horizontWidget_2)
        self.horizontLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontLayout_2.setObjectName("horizontLayout_2")
        self.label_file = QtWidgets.QLabel()
        self.label_file.setFont(font)
        self.label_file.setObjectName("label_file")
        self.label_file.setText("Файл настройки:")
        self.horizontLayout_2.addWidget(self.label_file)

        # Файл настроек
        self.horizontWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontWidget_3.setGeometry(QtCore.QRect(20, 170, 190, 40))
        self.horizontWidget_3.setObjectName("horizontWidget_3")
        self.horizontLayout_3 = QtWidgets.QHBoxLayout(self.horizontWidget_3)
        self.horizontLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontLayout_3.setObjectName("horizontLayout_3")
        self.edit_file = QtWidgets.QLineEdit()
        self.edit_file.setObjectName("edit_file")
        self.horizontLayout_3.addWidget(self.edit_file)
        self.save_file = QtWidgets.QPushButton()
        self.save_file.setText("Сохранить")
        self.save_file.setObjectName("save_file")
        self.horizontLayout_3.addWidget(self.save_file)

        # Таблица с параметрами

        self.horizontWidget_4 = QtWidgets.QWidget(self.centralwidget)
        x = int(x/1.2);y=int(y/2.4)
        self.horizontWidget_4.setGeometry(QtCore.QRect(20, 280, x, y))
        self.horizontWidget_4.setObjectName("horizontWidget_4")
        self.horizontLayout_4 = QtWidgets.QHBoxLayout(self.horizontWidget_4)
        self.horizontLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontLayout_4.setObjectName("horizontLayout_4")
        self.sti = QtGui.QStandardItemModel(parent=self)
        self.lst_name = ["Напряжение сети 1","Тока ЭА","Напряжения ЭА","Частота сети 2","Угол фаза АБ сети 1"]
        self.lst_type = ["Вычисляемый","Логический","Донесение","Внешний","Команда"]
        self.lst_designation = ["N_U_AB","EA_I_AC","EA_U_AB","N2_F_U_A","N2PHI_U_AB"]
        self.lst_ctype = ["int","int","float","float","floaat"]
        self.lst_common_id = ["2051","2052","2053","2054","2055"]
        self.table_params = QtWidgets.QTableView()
        for row in range(5):
            item1 = QtGui.QStandardItem(self.lst_name[row])
            item2 = QtGui.QStandardItem(self.lst_type[row])
            item3 = QtGui.QStandardItem(self.lst_designation[row])
            item4 = QtGui.QStandardItem(self.lst_ctype[row])
            item5 = QtGui.QStandardItem(self.lst_common_id[row])
            self.sti.appendRow([item1,item2,item3,item4,item5])
        self.sti.setHorizontalHeaderLabels(["name","type","designation","ctype","common_id"])
        self.table_params.setModel(self.sti)
        self.table_params.setColumnWidth(0,int(x//5.1))
        self.table_params.setColumnWidth(1,x//6)
        self.table_params.setColumnWidth(2,x//4)
        self.table_params.setColumnWidth(3,x//6)
        self.table_params.setColumnWidth(4,x//5)
        # Меняет размер строки, чтобы поместилось все содержимое
        self.table_params.resizeRowsToContents()
        # Сортировка по заголовкам столбцов
        self.table_params.setSortingEnabled(True)
        # Сортировка по столбцу в алфавитном порядке
        self.table_params.sortByColumn(0,QtCore.Qt.AscendingOrder)
        self.horizontLayout_4.addWidget(self.table_params)

        # self.centralwidget.raise_()
        # self.centralwidget1.raise_()
        # self.centralwidget2.raise_()
        # self.centralwidget3.raise_()

        # self.setLayout(hbox_port)

        self.setCentralWidget(self.centralwidget)
        # self.setGeometry(650, 350, 700, 550)
        self.setWindowTitle('logger')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Example()
    sys.exit(app.exec_())
