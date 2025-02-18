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

        count =0; count1=0
        data_tab =QtWidgets.QTabWidget()
        model = QtGui.QStandardItemModel()
        table = QtWidgets.QTableView()
        for i in data_dict[data].items():
            item1 = QtGui.QStandardItem(i[0])
            item2 = QtGui.QStandardItem(i[1][0])
            item3 = QtGui.QStandardItem(str(0))
            item1.setTextAlignment(QtCore.Qt.AlignHCenter)
            item3.setTextAlignment(QtCore.Qt.AlignHCenter)
            item1.setEditable(False)
            item2.setEditable(False)
            model.appendRow([item1,item2,item3])
            count +=1
            if count ==22 or count == len_data_dict:
                model.setHorizontalHeaderLabels(['Обозначение','Наименование','Значение'])
                table.setModel(model)
                table.setColumnWidth(0, 140)
                table.setColumnWidth(1, 500)
                table.setColumnWidth(2, 154)
                table.setRowHeight(0, 10)
                table.setRowHeight(1, 10)
                table.setFont(font)
                table.verticalHeader().setVisible(False)
                count1 +=1
                data_tab.addTab(table,f"Вкладка {count1}")
                model = QtGui.QStandardItemModel()
                table = QtWidgets.QTableView()
                count =0


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

class Param(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Шрифт
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        # font.setBold(True)
        # font.setWeight(75)

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

        self.centr_widget = QtWidgets.QWidget()
        self.centr_widget.setGeometry(QtCore.QRect(500,500,500,500))

        data_tab =QtWidgets.QTabWidget()
        model = QtGui.QStandardItemModel()
        table = QtWidgets.QTableView()
        item1 = QtGui.QStandardItem('EA_F_U_A')
        item2 = QtGui.QStandardItem('Частота')
        item3 = QtGui.QStandardItem(str(0))
        item1.setTextAlignment(QtCore.Qt.AlignHCenter)
        item3.setTextAlignment(QtCore.Qt.AlignHCenter)
        model.appendRow([item1, item2, item3])
        # model.setHorizontalHeaderLabels(['Обозначение', 'Наименование', 'Значение'])
        table.setModel(model)
        table.setColumnWidth(0, 80)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 74)
        table.setRowHeight(0,10)
        table.setFont(font)
        table.horizontalHeader().hide()
        table.verticalHeader().hide()
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.widget = QtWidgets.QWidget(self.centr_widget)
        self.widget.setContentsMargins(300,300,300,300)
        # self.widget.setGeometry(QtCore.QRect(0,500,0,0))
        self.vbox = QtWidgets.QVBoxLayout(self.widget)
        self.vbox.addWidget(QtWidgets.QLabel('Таблица 1'))
        self.vbox.addWidget(table)

        model1 = QtGui.QStandardItemModel()
        table1 = QtWidgets.QTableView()
        item1 = QtGui.QStandardItem('N_I_B')
        item2 = QtGui.QStandardItem('Ток')
        item3 = QtGui.QStandardItem(str(0))
        item1.setTextAlignment(QtCore.Qt.AlignHCenter)
        item3.setTextAlignment(QtCore.Qt.AlignHCenter)
        model1.appendRow([item1, item2, item3])
        # model.setHorizontalHeaderLabels(['Обозначение', 'Наименование', 'Значение'])
        table1.setModel(model1)
        table1.setColumnWidth(0, 80)
        table1.setColumnWidth(1, 100)
        table1.setColumnWidth(2, 74)
        table1.setRowHeight(0,10)
        table1.setFont(font)
        table1.horizontalHeader().hide()
        table1.verticalHeader().hide()
        table1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.widget1 = QtWidgets.QWidget(self.centr_widget)
        self.vbox1 = QtWidgets.QVBoxLayout(self.widget1)
        self.vbox1.addWidget(QtWidgets.QLabel('Таблица 2'))
        self.vbox1.addWidget(table1)
        data_tab.addTab(self.centr_widget, "Вкладка 1")

        data_tab.setCurrentIndex(0)
        self.horizontLayout.addWidget(data_tab)
        self.setLayout(self.horizontLayout)
        print('Unit2')
