# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QApplication,
                             QAction, QWidget)
from PyQt5 import Qt


class WorkThread(Qt.QThread):
    threadSignal = Qt.pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self, *args, **kwargs):
        c = 0
        while True:
            print("Thread")
            Qt.QThread.msleep(1)
            c += 1
            self.threadSignal.emit(c)
        return Qt.QThread.run(self, *args, **kwargs)


class Main1(QWidget):

    def __init__(self):
        print("Main1")
        self.initUI()

    def initUI1(self):
        btn1 = QPushButton("Вперед1", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Назад1", self)
        btn2.move(500, 50)

        btn1.clicked.connect(self.buttonClicked1)
        btn2.clicked.connect(self.buttonClicked1)

        btn1.setShortcut("F1")
        btn2.setShortcut("F2")

        self.statusBar()

        self.setGeometry(300, 300, 600, 450)
        self.setWindowTitle('Event sender')
        self.show()

    def buttonClicked1(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text())
        print("Click1")


class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.btn1 = QPushButton("Вперед", self)
        self.btn1.move(30, 50)

        self.btn2 = QPushButton("Назад", self)
        self.btn2.move(500, 50)

        self.btn1.clicked.connect(self.buttonClicked)
        self.btn2.clicked.connect(self.buttonClicked)

        self.btn1.setShortcut("F1")
        self.btn2.setShortcut("F2")

        self.statusBar()

        self.setGeometry(300, 300, 600, 450)
        self.setWindowTitle('Event sender')
        self.show()

        self.thread = None

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text())
        print("Click")
        if self.thread is None:
            print("is None")
            self.thread = WorkThread()
            self.thread.threadSignal.connect(self.main1)
            self.thread.start()
        else:
            self.thread.terminate()
            self.thread = None

    def main1(self):
        # self.btn1.setText("Вперед1")
        self.btn2.setText("Назад1")
        self.btn1.hide()
        self.btn3 = QPushButton("Вперед1", self)
        self.btn3.move(30, 50)
        self.btn3.show()
        # btn1 = QPushButton("Вперед1", self)
        # btn1.move(90, 50)
        # btn1.show()
        #
        # btn2 = QPushButton("Назад1", self)
        # btn2.move(200, 50)
        # btn2.show()
        #
        # self.show()

        # main = Main1()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
