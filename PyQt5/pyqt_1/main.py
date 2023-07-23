# # уроки - https://www.youtube.com/watch?v=M4EovcpiuNs&t=2s
# -*- coding: utf-8 -*-

# from test import *
#
# import sys
# app = QtWidgets.QApplication(sys.argv)
# MainWindow = QtWidgets.QMainWindow()
# ui = Ui_MainWindow()
# ui.setupUi(MainWindow)
# MainWindow.show()
#
# ui.label.setText("SDASDASJK")
#
# sys.exit(app.exec_())
from PyQt5.QtCore import QDate

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import sys

#Конструкция для отображения номера строки
#sys._getframe().f_lineno
Form, Window = uic.loadUiType("test.ui")

app = QApplication([])
window =Window()
form =Form()
form.setupUi(window)
window.show()

# form.label.setText("asdjhaskjgg")

n = sys._getframe


def on_click():
    print(form.plainTextEdit.toPlainText(),n().f_lineno)
    print(form.dateEdit.dateTime().toString('dd-MM-yyyy'),n().f_lineno)
    print("Clicked!!!",n().f_lineno)
    #Установка даты на календаре
    # print(form.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
    # date = QDate(2022,9,17)
    # form.calendarWidget.setSelectedDate(date)

def on_click_calendar():
    global start_date,calc_date
    # print(form.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
    form.dateEdit.setDate(form.calendarWidget.selectedDate())
    calc_date = form.calendarWidget.selectedDate()
    delta_days = start_date.daysTo(calc_date)
    print(delta_days,n().f_lineno)

def on_dateedit_change():
    # print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))
    form.calendarWidget.setSelectedDate(form.dateEdit.date())


form.pushButton.clicked.connect(on_click)
form.calendarWidget.clicked.connect(on_click_calendar)
form.dateEdit.dateChanged.connect(on_dateedit_change)

start_date = form.calendarWidget.selectedDate()
# calc_date = form.calendarWidget.selectedDate()
on_click_calendar()

app.exec_()