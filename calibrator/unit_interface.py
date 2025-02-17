# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QStackedWidget,
                             QHBoxLayout, QVBoxLayout, QApplication, QAction, QMainWindow)

from PyQt5 import QtCore, QtGui, QtWidgets
from class_read_data import Connect,Calibrator
from debug import printf

class Unit(QWidget):

    def __init__(self, data_dict,data, unit):
        super().__init__()
        self.initUI(data_dict,data,unit)

    def initUI(self,data_dict, data,unit):
        # Шрифт
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        # font.setBold(True)
        # font.setWeight(75)


        # Порт
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.page.setGeometry(QtCore.QRect(0,0,0,0))

        # self.centralwidget = centr
        # self.centralwidget(self.page)
        # self.centralwidget.setObjectName("centralWidget")
        # self.horizontWidget = QtWidgets.QWidget(self.page)
        # self.horizontWidget.setGeometry(QtCore.QRect(20, 20, 210, 40))
        # self.horizontWidget.setObjectName("horizontWidget")
        self.horizontLayout = QtWidgets.QVBoxLayout(self.page)
        self.horizontLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontLayout.setObjectName("horizontLayout")
        # self.centralwidget.addLayout(self.horizontLayout)
        # self.horizontLayout.addStretch(1)


        # for i in data_dict['preset'].items():
        #     printf(i[1][0])
        printf(data_dict[data].items())
        printf(len(data_dict[data].items()))

        len_data_dict =len(data_dict[data].items())

        count =0
        data_tab =QtWidgets.QTabWidget()
        for j in range(1,len_data_dict):
            model = QtGui.QStandardItemModel()
            table = QtWidgets.QTableView()
            for i in data_dict[data].items():
                item1 = QtGui.QStandardItem(i[0])
                item2 = QtGui.QStandardItem(i[1][0])
                item3 = QtGui.QStandardItem(str(0))
                item1.setTextAlignment(QtCore.Qt.AlignHCenter)
                item3.setTextAlignment(QtCore.Qt.AlignHCenter)
                model.appendRow([item1,item2,item3])
                count +=1
                if count ==22: break
            model.setHorizontalHeaderLabels(['Обозначение','Наименование','Значение'])
            table.setModel(model)
            table.setColumnWidth(0, 140)
            table.setColumnWidth(1, 500)
            table.setColumnWidth(2, 154)
            table.setFont(font)
            table.verticalHeader().setVisible(False)
            data_tab.addTab(table,f"Вкладка {j}")
            len_data_dict -=count
            if len_data_dict <=0: break


        # Вкладки
        # data_tab.insertTab(1,QtWidgets.QLabel('Таблица 1'),"Вкладка 2")
        # data_tab.addTab(QtWidgets.QLabel('Таблица 2'), "Калибровки")
        data_tab.setCurrentIndex(0)
        # data_tab.setDocumentMode(True)
        # data_tab.tabBar().setStyleSheet('background-color:rgb(255,255,0);')
        data_tab.setStyleSheet('background-color:rgb(220,254,225);')
        self.horizontLayout.addWidget(data_tab)
        self.horizontLayout.setAlignment(QtCore.Qt.AlignHCenter)
        # self.horizontLayout.addWidget(table)
        self.setLayout(self.horizontLayout)
        print('Unit1')
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
