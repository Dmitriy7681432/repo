# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QStackedWidget,
                             QHBoxLayout, QVBoxLayout, QApplication, QAction, QMainWindow)

from PyQt5 import QtCore, QtGui, QtWidgets

class Unit(QWidget):

    def __init__(self):
        super().__init__()

    def initUI(self,centr):
        # Шрифт
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        # font.setBold(True)
        # font.setWeight(75)

        # self.centralwidget = centr
        # self.centralwidget.setObjectName("centralWidget")

        # Порт
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.page.setGeometry(QtCore.QRect(0,0,0,0))

        # self.horizontWidget = QtWidgets.QWidget(self.page)
        # self.horizontWidget.setGeometry(QtCore.QRect(20, 20, 210, 40))
        # self.horizontWidget.setObjectName("horizontWidget")
        self.horizontLayout = QtWidgets.QVBoxLayout(self.page)
        self.horizontLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontLayout.setObjectName("horizontLayout")
        # self.horizontLayout.addStretch(1)

        # Таблица
        model = QtGui.QStandardItemModel()
        lst1 = ['s_1','s_2','s_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3',
                's_1', 's_2', 's_3'
                ]
        lst2 = ['Максимальное занчение','Минимальное значение','Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                'Максимальное занчение', 'Минимальное значение', 'Среднее значение',
                ]
        lst3=[564,12.1,120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              564, 12.1, 120,
              ]
        table = QtWidgets.QTableView()
        for i in range(0,22):
            item1 = QtGui.QStandardItem(lst1[i])
            item2 = QtGui.QStandardItem(lst2[i])
            item3 = QtGui.QStandardItem(str(lst3[i]))
            model.appendRow([item1,item2,item3])
        model.setHorizontalHeaderLabels(['Обозначение','Наименование','Значение'])
        table.setModel(model)
        table.setColumnWidth(0,140)
        table.setColumnWidth(1,520)
        table.setColumnWidth(2,120)
        table.setFont(font)

        # model1 = QtGui.QStandardItemModel()
        for i in range(23,45):
            item1 = QtGui.QStandardItem(lst1[i])
            item2 = QtGui.QStandardItem(lst2[i])
            item3 = QtGui.QStandardItem(str(lst3[i]))
            model.appendRow([item1,item2,item3])
        # model1.setHorizontalHeaderLabels(['Обозначение','Наименование','Значение'])
        table1 = QtWidgets.QTableView()
        table1.setModel(model)
        table1.setColumnWidth(0,140)
        table1.setColumnWidth(1,520)
        table1.setColumnWidth(2,120)
        table1.setFont(font)



        # Вкладки
        data_tab =QtWidgets.QTabWidget()
        data_tab.addTab(table, "Вкладка 1")
        data_tab.addTab(table1, "Вкладка 2")
        # data_tab.insertTab(1,QtWidgets.QLabel('Таблица 1'),"Вкладка 2")
        # data_tab.addTab(QtWidgets.QLabel('Таблица 2'), "Калибровки")
        data_tab.setCurrentIndex(0)
        data_tab.setDocumentMode(True)
        # data_tab.tabBar().setStyleSheet('background-color:rgb(255,255,0);')
        data_tab.setStyleSheet('background-color:rgb(220,254,225);')
        self.horizontLayout.addWidget(data_tab)

        return self.page

class Unit2(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Шрифт
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        # self.centralwidget = centr
        # self.centralwidget.setObjectName("centralWidget")

        # Порт
        # self.page = QtWidgets.QWidget()
        # self.page.setObjectName("page")
        # self.page.setGeometry(QtCore.QRect(300,300,300,300))

        # self.horizontWidget = QtWidgets.QWidget(self.page)
        # self.horizontWidget.setGeometry(QtCore.QRect(20, 20, 210, 40))
        # self.horizontWidget.setObjectName("horizontWidget")
        self.horizontLayout = QtWidgets.QHBoxLayout()
        self.horizontLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontLayout.setObjectName("horizontLayout")
        # self.horizontLayout.addStretch(1)
        # self.horizontLayout.setContentsMargins(0, 0, 0, 0)
        # self.horizontLayout.setObjectName("horizontLayout")

        data_tab =QtWidgets.QTabWidget()
        data_tab.addTab(QtWidgets.QLabel('Таблица 2'), "Вкладка 1")
        # data_tab.addTab(QtWidgets.QLabel('Таблица 4'), "Калибровки")
        data_tab.setCurrentIndex(0)
        self.horizontLayout.addWidget(data_tab)
        self.setLayout(self.horizontLayout)
        print('Unit2')
