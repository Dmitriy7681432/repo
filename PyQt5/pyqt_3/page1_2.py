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


# -*- coding:  utf-8 -*-
# from PyQt5 import QtCore, QtWidgets
# class MyWindow(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.setWindowTitle("Блокировка и удаление обработчика")
#         self.resize(300, 150)
#         self.button1 = QtWidgets.QPushButton("Нажми меня")
#         self.button2 = QtWidgets.QPushButton("Блокировать")
#         self.button3 = QtWidgets.QPushButton("Разблокировать")
#         self.button4 = QtWidgets.QPushButton("Удалить обработчик")
#         self.button5 = QtWidgets.QPushButton("Вернуть обработчик")
#         self.button3.setEnabled(False)
#         self.button5.setEnabled(False)
#         vbox = QtWidgets.QVBoxLayout()
#         vbox.addWidget(self.button1)
#         vbox.addWidget(self.button2)
#         vbox.addWidget(self.button3)
#         vbox.addWidget(self.button4)
#         vbox.addWidget(self.button5)
#         self.setLayout(vbox)
#         self.button1.clicked.connect(self.on_clicked_button1)
#         self.button2.clicked.connect(self.on_clicked_button2)
#         self.button3.clicked.connect(self.on_clicked_button3)
#         self.button4.clicked.connect(self.on_clicked_button4)
#         self.button5.clicked.connect(self.on_clicked_button5)
#
#     @QtCore.pyqtSlot()
#     def on_clicked_button1(self):
#         print("Нажата кнопка buttonl")
#     @QtCore.pyqtSlot()
#     def on_clicked_button2(self):
#         self.button1.blockSignals(True)
#         self.button2.setEnabled(False)
#         self.button3.setEnabled(True)
#     @QtCore.pyqtSlot()
#     def on_clicked_button3(self):
#         self.button1.blockSignals(False)
#         self.button2.setEnabled(True)
#         self.button3.setEnabled(False)
#     @QtCore.pyqtSlot()
#     def on_clicked_button4(self):
#         self.button1.clicked.disconnect(self.on_clicked_button1)
#         self.button2.setEnabled(False)
#         self.button3.setEnabled(False)
#         self.button4.setEnabled(False)
#         self.button5.setEnabled(True)
#
#     @QtCore.pyqtSlot()
#     def on_clicked_button5(self):
#         self.button1.clicked.connect(self.on_clicked_button1)
#         self.button2.setEnabled(True)
#         self.button3.setEnabled(False)
#         self.button4.setEnabled(True)
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec_())

# -*- coding: utf-8 -*-
# from PyQt5 import QtCore, QtWidgets
# class MyWindow(QtWidgets.QWidget):
#     mysignal = QtCore.pyqtSignal(int, int)
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.setWindowTitle("Генерация сигнала из программы")
#         self.resize(300, 100)
#         self.button1 = QtWidgets.QPushButton("Нажми меня")
#         self.button2 = QtWidgets.QPushButton("Кнопка 2")
#         vbox = QtWidgets.QVBoxLayout()
#         vbox.addWidget(self.button1)
#         vbox.addWidget(self.button2)
#         self.setLayout(vbox)
#         self.button1.clicked.connect(self.on_clicked_button1)
#         self.button2.clicked.connect(self.on_clicked_button2)
#         self.mysignal.connect(self.on_mysignal)
#     def on_clicked_button1(self):
#         print("Нажата кнопка button1")
#         # Генерируем сигналы
#         self.button2.clicked[bool].emit(True)
#         self.mysignal.emit(10, 20)
#     def on_clicked_button2(self):
#         print("Нажата кнопка button2")
#     def on_mysignal(self, x, y):
#         print("Обработан пользовательский сигнал mysignal()")
#         print("x =", x, "y =", y)
#
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec_())

# -*- coding:  utf-8 -*-
# from PyQt5 import QtCore, QtWidgets
# import time
# class MyWindow(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.setWindowTitle("Часы в окне")
#         self.resize(200, 100)
#         self.timer_id = 0
#         self.label = QtWidgets.QLabel("")
#         self.label.setAlignment (QtCore.Qt.AlignHCenter)
#         self.button1 = QtWidgets.QPushButton("Запустить")
#         self.button2 = QtWidgets.QPushButton("Остановить")
#         self.button2.setEnabled(False)
#         vbox = QtWidgets.QVBoxLayout()
#         vbox.addWidget(self.label)
#         vbox.addWidget(self.button1)
#         vbox.addWidget(self.button2)
#         self.setLayout(vbox)
#         self.button1.clicked.connect(self.on_clicked_button1)
#         self.button2.clicked.connect(self.on_clicked_button2)
#     def on_clicked_button1(self):
#         # Задаем интервал в 1 секунду и "приближенный" таймер
#         self.timer_id = self.startTimer(1000, timerType = QtCore.Qt.VeryCoarseTimer)
#         self.button1.setEnabled(False)
#         self.button2.setEnabled(True)
#     def on_clicked_button2(self):
#         if self.timer_id:
#             self.killTimer(self.timer_id)
#             self.timer_id = 0
#         self.button1.setEnabled(True)
#         self.button2.setEnabled(False)
#     def timerEvent(self, event):
#         self.label.setText(time.strftime("%H:%M:%S"))
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec_())

# -*- coding:  utf-8 -*-
from PyQt5 import QtCore, QtWidgets
import time
class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.resize(300, 100)
    def event(self, e):
        if e.type() == QtCore.QEvent.KeyPress:
            print("Нажата клавиша на клавиатуре")
            print("Код:", e.key(), ", текст:", e.text())
        elif e.type() == QtCore.QEvent.Close:
            print("Окно закрыто")
        elif e.type() == QtCore.QEvent.MouseButtonPress:
            print ("Щелчок мышью. Координаты:", e.x(), e.y())
        return QtWidgets.QWidget.event(self, e) # Отправляем дальше

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())