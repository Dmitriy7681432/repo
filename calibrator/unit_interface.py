# -*- coding: utf-8 -*-
import sys,re
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

        len_data_dict =len(data_dict[data].items())

        count =0; count1=0;count2=0
        self.data_tab =QtWidgets.QTabWidget()
        self.model = QtGui.QStandardItemModel()
        table = QtWidgets.QTableView()

        self.lst_table = []
        self.lst_model = []
        for i in data_dict[data].items():

            item1 = QtGui.QStandardItem(i[0])
            item2 = QtGui.QStandardItem(i[1][0])
            if data == 'preset':
                if i[1][1] == 'int':
                    self.item3 = QtGui.QStandardItem(str(0))
                else:
                    self.item3 = QtGui.QStandardItem(str(0.0))
            else:
                self.item3 = QtGui.QStandardItem(str(0.0))

            item1.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.item3.setTextAlignment(QtCore.Qt.AlignHCenter)
            item1.setEditable(False)
            item2.setEditable(False)
            self.item3.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            item1.setSelectable(False)
            item2.setSelectable(False)
            self.item3.setSelectable(False)

            self.model.appendRow([item1,item2,self.item3])
            table.setModel(self.model)
            table.setRowHeight(count, 12)
            count +=1
            count2 +=1
            if count ==34 or count2 == len_data_dict:
                table.setColumnWidth(0, 190)
                table.setColumnWidth(1, 450)
                table.setColumnWidth(2, 154)
                self.model.setHorizontalHeaderLabels(['Обозначение', 'Наименование', 'Значение'])
                table.setFont(font)
                table.verticalHeader().setVisible(False)
                count1 +=1
                self.data_tab.addTab(table,f"Вкладка {count1}")
                self.lst_table.append(table)
                self.lst_model.append(self.model)
                count =0
                self.model = QtGui.QStandardItemModel()
                table = QtWidgets.QTableView()

        self.index_data_tab = self.data_tab.currentIndex()
        for i in range(0,self.data_tab.count()):
            self.lst_table[i].clicked.connect(self.selectRow)
            self.lst_model[i].itemChanged.connect(self.changedValue)
            self.lst_table[i].entered.connect(self.pressedValue)
            # self.lst_model[i].intered.connect(self.presedValue)
        self.data_tab.currentChanged.connect(self.selectDataTab)
        printf(self.lst_model[0].item(0,0).text())
        printf(self.lst_model)

        # Вкладки
        self.data_tab.setStyleSheet('background-color:rgb(220,254,225);')\
                               # gridline-color:gray;')
        self.horizontLayout.addWidget(self.data_tab)
        self.horizontLayout.setAlignment(QtCore.Qt.AlignHCenter)
        # self.horizontLayout.addWidget(table)
        self.setLayout(self.horizontLayout)
        print('Unit1')

        # return self.page

    def is_valid_email(self,data):
        return re.match('^[0-9]*[.][0-9]+$', data) is not None

    def changedValue(self, value):
        if self.readData_flag ==0:
            item = self.lst_model[self.index_data_tab].item(value.row(), value.column())
            # if not value.text().isalpha() and '.' in self.checkValue and '.' in value.text():
            if self.is_valid_email(self.checkValue) and self.is_valid_email(value.text()):
                printf('Data_float', value.text(), value.row())
                item.setBackground(QtGui.QBrush(QtGui.QColor(255,255,9)))
            elif value.text().isdigit() and (not '.' in self.checkValue and not '.' in value.text()):
                printf('Data_int', value.text(), value.row())
                item.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 9)))
            else:
                printf('CHANGE',value.row(),value.column(),self.checkValue)
                item.setChild(value.row(),value.column(), item.setText(self.checkValue))


    def selectRow(self, data):
        self.checkValue = data.data()
        printf('SELECT', data.row(), data.column(), data.data())


    def selectDataTab(self,index):
        self.index_data_tab = index

    def pressedValue(self,value):
        printf(value.data())

    def readData(self,data_dict,data):
        self.readData_flag =1
        # self.lst_model[0].itemChanged.disconnect()
        count =0;count1 =0;num=0
        cnt_row = self.lst_model[0].rowCount()
        printf(cnt_row)
        # for i in self.data_tab.count():
        for i in data_dict[data].items():
            item = self.lst_model[num].item(count, 2)
            if data =='preset':
                self.checkValue = str(i[1][2])
                item.setChild(count, 2, item.setText(str(i[1][2])))
            else:
                self.checkValue = str(i[1][1])
                item.setChild(count, 2, item.setText(str(i[1][1])))
            count+=1
            if count == cnt_row:
                count =0
                count1+=1
                num+=1
                if count1 == self.data_tab.count():
                    self.readData_flag = 0
                    return 0
                    # printf(num)
                    # item = self.lst_model[num].item(count, 2)
                # else: printf(data_dict); return 0
        self.readData_flag = 0

        # printf(data_dict)
    def writeData(self,data_dict,data):
        # for i in range(0,self.data_tab.count()):
        #     for j in range(0, self.lst_model[0].rowCount()):
        #         item = self.lst_model[self.index_data_tab].item(j, 2)
        #         data_dict[data].items()[1][2] =

        dt = data_dict[data].keys()
        print(dt)


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
        table.setRowHeight(0,10)
        table.setColumnWidth(0, 80)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 74)
        table.setFont(font)
        table.horizontalHeader().hide()
        table.verticalHeader().hide()
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        data_tab.setStyleSheet('background-color:rgb(220,254,225);')
        table.setStyleSheet('background-color:rgb(255,255,255);')
        self.widget = QtWidgets.QWidget(self.centr_widget)
        self.widget.setContentsMargins(400,0,0,0)
        self.widget.setGeometry(0,0,750,230)
        # self.widget.setGeometry(QtCore.QRect(0,500,0,0))
        self.vbox = QtWidgets.QVBoxLayout(self.widget)
        self.vbox.addWidget(QtWidgets.QLabel('Таблица 1'))
        self.vbox.addWidget(table)

        model1 = QtGui.QStandardItemModel()
        table1 = QtWidgets.QTableView()
        self.item =[]
        for i in range (1,4):
            item1 = QtGui.QStandardItem(f'N_I_B{i}')
            item2 = QtGui.QStandardItem(f'Ток{i}')
            self.item3 = QtGui.QStandardItem(str(i))
            item1.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.item3.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.item3.setBackground(QtGui.QBrush(QtGui.QColor(255,255,9)))
            self.item.append(item1)
            self.item.append(item2)
            self.item.append(self.item3)
            # model1.appendRow([item1, item2, self.item3])
            model1.appendRow([item1,item2,self.item3])
        # model.setHorizontalHeaderLabels(['Обозначение', 'Наименование', 'Значение'])
        table1.setModel(model1)
        table1.setColumnWidth(0, 80)
        table1.setColumnWidth(1, 100)
        table1.setColumnWidth(2, 74)
        table1.setRowHeight(0,10)
        table1.setFont(font)
        table1.horizontalHeader().hide()
        table1.verticalHeader().hide()
        printf(model1.item(1,0).text())
        # table1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # table1.setGridStyle(0)

        self.widget1 = QtWidgets.QWidget(self.centr_widget)
        self.vbox1 = QtWidgets.QVBoxLayout(self.widget1)
        self.vbox1.addWidget(QtWidgets.QLabel('Таблица 2'))
        self.vbox1.addWidget(table1)
        data_tab.addTab(self.centr_widget, "Вкладка 1")

        data_tab.setCurrentIndex(0)
        data_tab.setStyleSheet('background-color:rgb(220,254,225);')\
                               #gridline-color:black;')
        table1.setStyleSheet('background-color:rgb(255,255,255);')
        self.horizontLayout.addWidget(data_tab)

        table1.clicked.connect(self.selectRow)
        model1.itemChanged.connect(self.on1_click)
        self.setLayout(self.horizontLayout)
        print('Unit2')

    def on1_click(self,value):
        if value.text().isdigit():
            print('Data',value.text(),value.row())
        else:
            # self.item3.setChild(value.row(),value.column(),self.item3.setText(self.checkValue))
            self.item[2].setChild(value.row(),value.column(),self.item[2].setText(self.checkValue))

    def selectRow(self,data):
        self.checkValue = data.data()
        printf('SELECT',data.row(),data.column(),data.data())
