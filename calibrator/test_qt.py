# -*- coding: utf-8 -*-
# import sys
# from PyQt5.QtWidgets import (QWidget, QPushButton, QStackedWidget, QToolBar, QToolButton,
#                              QHBoxLayout, QVBoxLayout, QApplication, QAction, QMainWindow)
#
# from PyQt5 import QtCore, QtGui, QtWidgets
#
# class Main(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         #Шрифт
#         font = QtGui.QFont()
#         font.setFamily("Times New Roman")
#         font.setPointSize(14)
#         font.setBold(True)
#         font.setWeight(75)
#
#         desktop = QtWidgets.QApplication.desktop()
#         x = desktop.width();
#         y = desktop.height()
#         print(x, y)
#         x_size_desktop = int(x / 2.4);
#         y_size_desktop = int(y / 1.3)
#
#         # Вычисляем размер экрана
#         self.resize(x_size_desktop, y_size_desktop)
#         # Вывод окна по центру
#         x_ = (desktop.width() - self.frameSize().width()) // 2
#         y_ = (desktop.height() - self.frameSize().height()) // 2
#         self.move(x_, y_)
#
#         self.centralwidget = QtWidgets.QWidget(self)
#         self.centralwidget.setObjectName("centralWidget")
#         self.centralwidget.setGeometry(0,0,800,50)
#
#         # self.mainWidget = QWidget(self.centralwidget)
#         self.mainLayout = QHBoxLayout(self.centralwidget)
#
#         # Кнопки вкладки
#         buttonUnit1 = QToolButton(self.centralwidget)
#         buttonUnit1.setText('Б400')
#         buttonUnit2 = QToolButton(self.centralwidget)
#         buttonUnit2.setText('БУ50')
#         buttonUnit1.setFont(font)
#         buttonUnit2.setFont(font)
#         buttonUnit1.setGeometry(QtCore.QRect(100,100,100,100))
#         buttonUnit2.setGeometry(QtCore.QRect(100,100,100,100))
#
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         # sizePolicy.setHeightForWidth(buttonUnit1.sizePolicy().hasHeightForWidth())
#         buttonUnit1.setSizePolicy(sizePolicy)
#         buttonUnit2.setSizePolicy(sizePolicy)
#         buttonUnit1.setMaximumSize(QtCore.QSize(750, 300))
#         buttonUnit2.setMaximumSize(QtCore.QSize(750, 300))
#
#         self.mainLayout.addWidget(buttonUnit1)
#         self.mainLayout.addWidget(buttonUnit2)
#         # self.mainWidget.setGeometry(0,-30,150,100)
#         # self.mainLayout.setGeometry(QtCore.QRect(100,300,300,300))
#
#         self.setObjectName("MainWindow")
#         self.setWindowTitle('Calibrator')
#         self.show()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     app.setStyle('Fusion')
#     ex = Main()
#     sys.exit(app.exec_())


# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog
#
# class SecondWindow(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Второе окно")
#         self.button = QPushButton("Закрыть")
#         self.button.clicked.connect(self.close)
#         layout = QVBoxLayout()
#         layout.addWidget(self.button)
#         self.setLayout(layout)
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Главное окно")
#         self.button = QPushButton("Открыть второе окно")
#         self.button.clicked.connect(self.open_second_window)
#         central_widget = QWidget()
#         layout = QVBoxLayout()
#         layout.addWidget(self.button)
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)
#
#     def open_second_window(self):
#         second_window = SecondWindow()
#         second_window.exec_() # Или second_window.show() для немодального окна
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()
#     sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import test_qt1
from PyQt5.QtCore import QBasicTimer

class Worker(QThread):
    finished = pyqtSignal()
    window_created = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = None

    def run(self):
        # Здесь создается второе окно
        # self.window = QWidget()
        # layout = QVBoxLayout()
        # label = QLabel("Второе окно")
        # layout.addWidget(label)
        # self.window.setLayout(layout)
        # self.window.setWindowTitle("Второе окно")
        # self.window = test_qt1.Example()

        self.window = QWidget()
        self.pbar = QProgressBar(self.window)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.btn = QPushButton('Начать', self.window)
        self.btn.move(30, 80)
        self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0

        layout = QVBoxLayout()
        layout.addWidget(self.pbar)
        layout.addWidget(self.btn)
        self.window.setLayout(layout)

        self.window.setGeometry(300, 300, 280, 170)
        self.window.setWindowTitle('Прогресс бар')

        self.window_created.emit(self.window)  # Отправляем сигнал о создании окна
        self.finished.emit()  # Отправляем сигнал об окончании работы
        print('3')

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Закончено')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        print('doAction', self.timer.isActive())
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Начать')
        else:
            self.timer.start(100, self)
            self.btn.setText('Стоп')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное окно")
        self.button = QPushButton("Открыть второе окно")
        self.button.clicked.connect(self.open_second_window)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.show()
        # self.open_second_window()
        # self.second_window = None
        # self.worker = None

    # @pyqtSlot()
    def open_second_window(self):
        # self.button.setEnabled(False)  # Отключаем кнопку, пока второе окно загружается
        self.worker = Worker()
        self.worker.window_created.connect(self.show_second_window)
        self.worker.finished.connect(self.thread_finished)
        self.worker.start()
        print('1')

    # @pyqtSlot(QWidget)
    def show_second_window(self, window):
        self.second_window = window
        self.second_window.show()
        print('2')

    # @pyqtSlot()
    def thread_finished(self):
        self.button.setEnabled(True) # Включаем кнопку, когда второе окно отображено
        # pass
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    # main_window.show()
    # main_window.open_second_window()
    sys.exit(app.exec_())
