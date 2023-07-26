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
import sys, pickle,os

# Конструкция для отображения номера строки
# sys._getframe().f_lineno
# Для того чтобы запускать файл из любого места
print(os.path.realpath(__file__))
dirname,filename = os.path.split(os.path.realpath(__file__))
print(dirname)
Form, Window = uic.loadUiType(dirname+"\\test.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

n = sys._getframe


def save_to_file():
    global start_date, calc_date, description
    # start_date = QDate(2023,7,25)
    data_to_save = {"start": start_date, "end": calc_date, "desc": description}
    file1=open("config.txt","wb")
    pickle.dump(data_to_save,file1)
    file1.close()


def read_from_file():
    global start_date, calc_date, description,now_date
    try:
        file1 = open("config.txt","rb")
        data_to_load = pickle.load(file1)
        file1.close()
        start_date = data_to_load["start"]
        calc_date = data_to_load["end"]
        description = data_to_load["desc"]
        print(start_date.toString('dd-MM-yyyy'),calc_date.toString('dd-MM-yyyy'),
              description, n().f_lineno)
        form.calendarWidget.setSelectedDate(calc_date)
        form.dateEdit.setDate(calc_date)
        form.plainTextEdit.setPlainText(description)
        delta_days_left = start_date.daysTo(now_date) # прошло дней
        delta_days_right = now_date.daysTo(calc_date) # осталось дней
        days_total = start_date.daysTo(calc_date) # всего дней
        print(delta_days_left,delta_days_right,days_total,n().f_lineno)
        procent = int(delta_days_left*100/days_total)
        print(procent,n().f_lineno)
        form.progressBar.setProperty("value",procent)
    except:
        print("Не могу прочитать файл конфигурации")


def on_click():
    global calc_date, description, start_date
    start_date =now_date
    calc_date = form.calendarWidget.selectedDate()
    description = form.plainTextEdit.toPlainText()

    # print(form.plainTextEdit.toPlainText(), n().f_lineno)
    # print(form.dateEdit.dateTime().toString('dd-MM-yyyy'), n().f_lineno)
    print("Clicked!!!", n().f_lineno)

    save_to_file()
    # Установка даты на календаре
    # print(form.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
    # date = QDate(2022,9,17)
    # form.calendarWidget.setSelectedDate(date)


def on_click_calendar():
    global start_date, calc_date
    # print(form.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
    form.dateEdit.setDate(form.calendarWidget.selectedDate())
    calc_date = form.calendarWidget.selectedDate()
    delta_days = start_date.daysTo(calc_date)
    print(delta_days, n().f_lineno)


def on_dateedit_change():
    global start_date, calc_date
    # print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))
    form.calendarWidget.setSelectedDate(form.dateEdit.date())
    calc_date = form.dateEdit.date()
    delta_days = start_date.daysTo(calc_date)
    print(delta_days, n().f_lineno)
    form.label_3.setText(f"До наступления события осталось: {delta_days} дней")


form.pushButton.clicked.connect(on_click)
form.calendarWidget.clicked.connect(on_click_calendar)
form.dateEdit.dateChanged.connect(on_dateedit_change)

start_date = form.calendarWidget.selectedDate()
print(start_date.toString('dd-MM-yyyy'),n().f_lineno)
now_date = form.calendarWidget.selectedDate()
calc_date = form.calendarWidget.selectedDate()
description = form.plainTextEdit.toPlainText()
read_from_file()
form.label.setText(f"Трекер события от {start_date.toString('dd-MM-yyyy')}")
on_click_calendar()

app.exec_()
