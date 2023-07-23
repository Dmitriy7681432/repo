# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

import sys

n = sys._getframe

class Main(object):

    def setup(self, MainWindow):
        # Главное окно
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(683, 540)

        # Виджет
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Метка
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 0, 211, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # Календарь
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(301, 130, 311, 181))
        self.calendarWidget.setObjectName("calendarWidget")

        # Прогресс бар
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 390, 651, 51))
        self.progressBar.setProperty("value", 35)
        self.progressBar.setObjectName("progressBar")

        # Работ с текстом
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(40, 170, 241, 141))
        self.plainTextEdit.setObjectName("plainTextEdit")

        # Метка 2
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 130, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        # Кнопка
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(170, 330, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        # Дата
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(40, 330, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateEdit.setFont(font)
        self.dateEdit.setObjectName("dateEdit")

        # Метка 3
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 450, 541, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        # Меню бар
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 683, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # Статус бар
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setCentralWidget(self.centralwidget)

        # Вызов функции translate
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Тест"))
        self.label.setText(_translate("MainWindow", "Трекер события"))
        self.label_2.setText(_translate("MainWindow", "Описание события "))
        self.pushButton.setText(_translate("MainWindow", "Отследить"))
        self.label_3.setText(
            _translate("MainWindow", "<html><head/><body><p>До наступления события осталось xx дней</p></body></html>"))

    def on_click(self):
        print(self.plainTextEdit.toPlainText(), n().f_lineno)
        print(self.dateEdit.dateTime().toString('dd-MM-yyyy'), n().f_lineno)
        print("Clicked!!!", n().f_lineno)

    def on_click_calendar(self):
        ui.dateEdit.setDate(ui.calendarWidget.selectedDate())
        # print(self.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
        calc_date = self.calendarWidget.selectedDate()
        delta_days = start_date.daysTo(calc_date)
        print(delta_days,n().f_lineno)

    def on_dateedit_change(self):
        # print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))
        self.calendarWidget.setSelectedDate(self.dateEdit.date())
        print(self.dateEdit.date(),n().f_lineno)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Main()
    ui.setup(MainWindow)
    MainWindow.show()

    ui.pushButton.clicked.connect(ui.on_click)
    ui.calendarWidget.clicked.connect(ui.on_click_calendar)
    ui.dateEdit.dateChanged.connect(ui.on_dateedit_change)
    start_date = ui.calendarWidget.selectedDate()
    ui.on_click_calendar()

    sys.exit(app.exec_())

"""
        self.button1 = QtWidgets.QPushButton("One")
        self.button2 = QtWidgets.QPushButton("Two")
        self.button3 = QtWidgets.QPushButton("Three")
        self.button4 = QtWidgets.QPushButton("Four")
        self.button5 = QtWidgets.QPushButton("Five")
        # self.button5.setGeometry(650,495,239,239)

        self.left_container = QtWidgets.QWidget(self.centralwidget)
        self.left_container.setFixedWidth(130)

        self.layout = QtWidgets.QHBoxLayout(self.left_container)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button4)
        self.layout.addWidget(self.button5)
"""
