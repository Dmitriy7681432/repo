#  -*- coding:   utf-8  -*-
# from PyQt5 import QtCore, QtGui, QtWidgets
# import time
#
#
# class MyWindow(QtWidgets.QPushButton):
#     def __init__(self):
#         QtWidgets.QPushButton.__init__(self)
#         self.setText("Закрыть окно")
#         self.clicked.connect(QtWidgets.qApp.quit)
#
#     def load_data(self, sp):
#         for i in range(1, 11):  # Имитируем процесс
#             time.sleep(2)  # Что-то загружаем
#             sp.showMessage("Загрузка данных... {0}%".format(i * 10),
#                            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
#             QtWidgets.qApp.processEvents()  # Запускаем оборот цикла
#
#
# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     splash = QtWidgets.QSplashScreen(QtGui.QPixmap("img1.jpeg"))
#     splash.showMessage("Загрузка данных... 0%",
#                        QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
#     splash.show()  # Отображаем заставку
#     QtWidgets.qApp.processEvents()  # Запускаем оборот цикла
#     window = MyWindow()
#     window.setWindowTitle("Использование класса QSplashScreen")
#     window.resize(300, 30)
#     window.load_data(splash)  # Загружаем данные
#     window.show()
#     splash.finish(window)  # Скрываем заставку
# from PyQt5 import QtGui, QtCore, QtWidgets
#
# desktop = QtWidgets.QApplication.desktop()
# print(desktop.width(),desktop.height())
# -*- coding: utf-8 -*-
# from PyQt5 import QtWidgets
# import sys
# app = QtWidgets.QApplication(sys.argv)
# window = QtWidgets.QWidget()
# window.setWindowTitle("Вывод окна по центру экрана")
# window.resize(300, 100)
# desktop = QtWidgets.QApplication.desktop()
# x = (desktop.width() - window.width()) // 2
# y = (desktop.height() - window.height()) // 2
# window.move(x, y)
# window.show()
# sys.exit(app.exec_())

# Вывод окна точно по центру экрана
# -*- coding: utf-8 -*-
# from PyQt5 import QtWidgets
# import sys
# app = QtWidgets.QApplication(sys.argv)
# window = QtWidgets.QWidget()
# window.setWindowTitle("Вывод окна по центру экрана")
# window.resize(300, 100)
# # window.move(window.width() * -2, 0)
# window.show()
# desktop = QtWidgets.QApplication.desktop()
# x = (desktop.width() - window.frameSize().width()) // 2
# y = (desktop.height() - window.frameSize().height()) // 2
# window.move(x, y)
# sys.exit(app.exec_())

#  -*- coding:   utf-8  -*-
# from PyQt5 import QtCore, QtWidgets
# import sys
#
#
# def show_modal_window():
#     # global modalWindow
#     modalWindow = QtWidgets.QWidget(window1, QtCore.Qt.Window)
#     modalWindow.setWindowTitle("Модальное окно")
#     modalWindow.resize(200, 50)
#     modalWindow.setWindowModality(QtCore.Qt.WindowModal)
#     modalWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
#     modalWindow.move(window1.geometry().center() - modalWindow.rect().center() -
#                      QtCore.QPoint(4, 30))
#     modalWindow.show()
#
#
# app = QtWidgets.QApplication(sys.argv)
# window1 = QtWidgets.QWidget()
# window1.setWindowTitle("Обычное окно")
# window1.resize(300, 100)
# button = QtWidgets.QPushButton("Открыть модальное окно")
# button.clicked.connect(show_modal_window)
# vbox = QtWidgets.QVBoxLayout()
# vbox.addWidget(button)
# window1.setLayout(vbox)
# window1.show()
# window2 = QtWidgets.QWidget()
# window2.setWindowTitle("Это окно не будет блокировано при WindowModal")
# window2.resize(500, 100)
# window2.show()
# sys.exit(app.exec_())


# -*- coding:   utf-8  -*-
from PyQt5 import QtCore, QtWidgets
import sys
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget(flags=QtCore.Qt.Dialog)
window.setWindowTitle("Закрытие окна из программы")
window.resize(300, 70)
button = QtWidgets.QPushButton("Закрыть окно", window)
button.setFixedSize(150, 30)
button.move(75, 20)
button.clicked.connect(window.close)
window.show()
sys.exit(app.exec_())
