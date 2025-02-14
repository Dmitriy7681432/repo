# -*- coding: utf-8 -*-
# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets
#
#
# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.resize(506, 312)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#
#         self.hbox = QtWidgets.QHBoxLayout(self.centralwidget)
#
#         self.toolButton = QtWidgets.QToolButton(self.centralwidget)
#         # self.toolButton.setGeometry(QtCore.QRect(220, 120, 41, 41))
#         self.toolButton1 = QtWidgets.QToolButton(self.centralwidget)
#         # self.toolButton1.setGeometry(QtCore.QRect(120, 20, 141, 41))
#
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
#         self.toolButton.setSizePolicy(sizePolicy)
#         self.toolButton.setMaximumSize(QtCore.QSize(300, 100))
#         self.hbox.addWidget(self.toolButton)
#         self.hbox.addWidget(self.toolButton1)
#
#         # icon = QtGui.QIcon()
#         # icon.addPixmap(QtGui.QPixmap("exiticon.png [exact location of image]"),
#         #                QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         #
#         # # adding icon to the toolbutton
#         # self.toolButton.setIcon(icon)
#         MainWindow.setCentralWidget(self.centralwidget)
#
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#         # adding signal and slot
#         self.toolButton.clicked.connect(self.exitapp)
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#
#         # For closing the application
#     #
#     def exitapp(self):
#         sys.exit()
#
#
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())



# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit
#
#
# class Window(QMainWindow):  # Создаем класс Window, который наследует все от класса QMainWindow
#     def __init__(self):  # Создаем конструктор
#         super().__init__()  # С помощью функции super вызывем конструктор из родительского класса
#
#         self.setGeometry(700, 200, 450, 650)  # Выбираем отступы, ширу и высоту окна
#         self.setWindowTitle('КБЖУ')  # Указываем название приложения
#
#         self.heading = QLabel()  # Создаем заголовок приложения
#         self.heading.setText('Заголовок')  # Текст в этом заголовке
#         self.heading.setStyleSheet('background-color: rgb(68, 207, 203);')  # Фон заголовка
#
#         self.text_edit = QTextEdit()
#
#         self.button_close = QPushButton('Закрыть')
#         self.button_close.clicked.connect(self.close)
#
#         self.button_save = QPushButton('Сохранить')
#
#         layout_buttons = QHBoxLayout()
#         layout_buttons.addWidget(self.button_save)
#         layout_buttons.addWidget(self.button_close)
#
#         main_layout = QVBoxLayout()
#         main_layout.addWidget(self.heading)
#         main_layout.addWidget(self.text_edit)
#         main_layout.addLayout(layout_buttons)
#
#         central_widget = QWidget()
#         central_widget.setLayout(main_layout)
#
#         self.setCentralWidget(central_widget)
#
#
# # Функция которая создает приложение
# def main():
#     app = QApplication(sys.argv)  # создаем объект в качестве параметра предаём информацию о системе
#
#     window = Window()  # Создаем объект(Окно  приложения) на основе нашего класса Window
#     window.show()  # Метод show показывает созданное окно
#
#     sys.exit(app.exec_())  # Корректное закрытие приложения
#
#
# if __name__ == '__main__':
#     main()

import sys
from PyQt5 import QtWidgets, uic  # Импортируем PyQt5

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('your_ui_file.ui', self) # Замените 'your_ui_file.ui' на имя вашего файла .ui

        self.centralwidget = QtWidgets.QWidget(self)
        # Создаем QStackedWidget
        self.stacked_widget = QtWidgets.QStackedWidget(self.centralwidget) # self.centralwidget - это центральный виджет вашего главного окна. Если структура другая, поправьте.
        self.stacked_widget.setGeometry(10, 10, 800, 600) # Установите геометрию по вашему ui файлу.
        self.setCentralWidget(self.stacked_widget)

        # Создаем страницы (виджеты)
        self.page1 = QtWidgets.QWidget()
        self.page2 = QtWidgets.QWidget()
        self.page3 = QtWidgets.QWidget()

        # Загружаем UI для каждой страницы (если используется)
        # uic.loadUi('page1.ui', self.page1)
        # uic.loadUi('page2.ui', self.page2)
        # uic.loadUi('page3.ui', self.page3)

        # Добавляем страницы в QStackedWidget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)

        # Добавляем кнопки навигации (пример)
        self.button1 = QtWidgets.QPushButton("Page 1", self)
        self.button1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.button2 = QtWidgets.QPushButton("Page 2", self)
        self.button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.button3 = QtWidgets.QPushButton("Page 3", self)
        self.button3.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        # Расположите кнопки на вашем главном окне (в ui файле или программно).

        # self.button1.move(10, 10) #Пример
        # self.button2.move(10, 40)
        # self.button3.move(10, 70)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())