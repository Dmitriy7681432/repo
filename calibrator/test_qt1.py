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



import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit


class Window(QMainWindow):  # Создаем класс Window, который наследует все от класса QMainWindow
    def __init__(self):  # Создаем конструктор
        super().__init__()  # С помощью функции super вызывем конструктор из родительского класса

        self.setGeometry(700, 200, 450, 650)  # Выбираем отступы, ширу и высоту окна
        self.setWindowTitle('КБЖУ')  # Указываем название приложения

        self.heading = QLabel()  # Создаем заголовок приложения
        self.heading.setText('Заголовок')  # Текст в этом заголовке
        self.heading.setStyleSheet('background-color: rgb(68, 207, 203);')  # Фон заголовка

        self.text_edit = QTextEdit()

        self.button_close = QPushButton('Закрыть')
        self.button_close.clicked.connect(self.close)

        self.button_save = QPushButton('Сохранить')

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.button_save)
        layout_buttons.addWidget(self.button_close)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.heading)
        main_layout.addWidget(self.text_edit)
        main_layout.addLayout(layout_buttons)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)


# Функция которая создает приложение
def main():
    app = QApplication(sys.argv)  # создаем объект в качестве параметра предаём информацию о системе

    window = Window()  # Создаем объект(Окно  приложения) на основе нашего класса Window
    window.show()  # Метод show показывает созданное окно

    sys.exit(app.exec_())  # Корректное закрытие приложения


if __name__ == '__main__':
    main()