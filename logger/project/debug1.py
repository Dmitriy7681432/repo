# -*- coding: utf-8 -*-
import sys,threading
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QApplication,QAction,
                            QWidget)

from PyQt5 import QtWidgets,QtCore
from PyQt5 import Qt


class WorkThread(Qt.QThread):
    threadSignal = Qt.pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self, *args, **kwargs):
        c = 0
        while True:
            Qt.QThread.msleep(1000)
            c += 1
            self.threadSignal.emit(c)
        return Qt.QThread.run(self, *args, **kwargs)


class MsgBox(Qt.QDialog):

    def __init__(self):
        super().__init__()
        layout = Qt.QVBoxLayout(self)
        self.label = Qt.QLabel("")
        layout.addWidget(self.label)
        close_btn = Qt.QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        self.resize(50, 50)


class MainWindow(Qt.QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.btn = Qt.QPushButton("Run thread!")
        self.btn.clicked.connect(self.on_btn)
        self.msg = MsgBox()
        self.setCentralWidget(self.btn)
        self.thread = None

    def on_btn(self):
        if self.thread is None:
            self.thread = WorkThread()
            self.thread.threadSignal.connect(self.on_threadSignal)
            self.thread.start()
            self.btn.setText("Stop thread")
        else:
            self.thread.terminate()
            self.thread = None
            self.btn.setText("Start thread")

    def on_threadSignal(self, value):
        self.msg.label.setText(str(value))
        if not self.msg.isVisible():
            self.msg.show()


if __name__ == '__main__':
    app = Qt.QApplication([])
    mw = MainWindow()
    mw.show()
    app.exec()
