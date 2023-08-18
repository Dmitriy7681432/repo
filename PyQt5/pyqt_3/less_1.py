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
from PyQt5 import QtWidgets
import sys
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("Вывод окна по центру экрана")
window.resize(300, 100)
# window.move(window.width() * -2, 0)
window.show()
desktop = QtWidgets.QApplication.desktop()
x = (desktop.width() - window.frameSize().width()) // 2
y = (desktop.height() - window.frameSize().height()) // 2
window.move(x, y)
sys.exit(app.exec_())