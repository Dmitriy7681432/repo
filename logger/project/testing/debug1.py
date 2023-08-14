# -*- coding: utf-8 -*-
import sys,threading
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QApplication,QAction,
                            QWidget,QLabel,QFrame)

from PyQt5 import QtWidgets,QtCore
from PyQt5 import Qt

#
# class WorkThread(Qt.QThread):
#     threadSignal = Qt.pyqtSignal(int)
#
#     def __init__(self):
#         super().__init__()
#
#     def run(self, *args, **kwargs):
#         c = 0
#         while True:
#             print("Thread")
#             Qt.QThread.msleep(1000)
#             c += 1
#             self.threadSignal.emit(c)
#         return Qt.QThread.run(self, *args, **kwargs)
#
#
# class MsgBox(Qt.QDialog):
#
#     def __init__(self):
#         super().__init__()
#         layout = Qt.QVBoxLayout(self)
#         self.label = Qt.QLabel("")
#         layout.addWidget(self.label)
#         close_btn = Qt.QPushButton("Close")
#         close_btn.clicked.connect(self.close)
#         layout.addWidget(close_btn)
#         self.resize(50, 50)
#
#
# class MainWindow(Qt.QMainWindow):
#
#     def __init__(self):
#         super().__init__()
#         self.resize(300, 200)
#         self.btn = Qt.QPushButton("Run thread!")
#         self.btn.clicked.connect(self.on_btn)
#         self.msg = MsgBox()
#         self.setCentralWidget(self.btn)
#         self.thread = None
#
#     def on_btn(self):
#         if self.thread is None:
#             self.thread = WorkThread()
#             self.thread.threadSignal.connect(self.on_threadSignal)
#             self.thread.start()
#             self.btn.setText("Stop thread")
#         else:
#             self.thread.terminate()
#             self.thread = None
#             self.btn.setText("Start thread")
#
#     def on_threadSignal(self, value):
#         self.msg.label.setText(str(value))
#         if not self.msg.isVisible():
#             self.msg.show()
#
#
# if __name__ == '__main__':
#     app = Qt.QApplication([])
#     mw = MainWindow()
#     mw.show()
#     app.exec()

class W_page1(object):
   def setup(self,page1):
       page1.setObjectName("page1")
       page1.resize(450, 800)
       self.widget_page1 = QWidget(page1)
       self.widget_page1.setObjectName("widget_page1")

       self.label_1 = QLabel(self.widget_page1)
       self.label_1.setGeometry(QtCore.QRect(197, 378, 56, 16))
       self.label_1.setObjectName("label_1")

       self.bnt = QtWidgets.QPushButton(self.widget_page1)

       page1.setCentralWidget(self.widget_page1)
       self.retranslate(page1)
       QtCore.QMetaObject.connectSlotsByName(page1)

   def retranslate(self,page1):
       _translate = QtCore.QCoreApplication.translate
       page1.setWindowTitle(_translate("page1", "MainWindow"))
       self.label_1.setText(_translate("page1", "page1"))
       self.bnt.setText(_translate("Main", "btn"))


class W_page2(object):
    def setup(self, page2):
        page2.setObjectName("page2")
        page2.resize(450, 800)
        self.widget_page2 = QWidget(page2)
        self.widget_page2.setObjectName("widget_page2")

        self.label_2 = QLabel(self.widget_page2)
        self.label_2.setGeometry(QtCore.QRect(197, 378, 56, 16))
        self.label_2.setObjectName("label_2")

        self.bnt2 = QtWidgets.QPushButton(self.widget_page2)

        page2.setCentralWidget(self.widget_page2)
        self.retranslate(page2)
        QtCore.QMetaObject.connectSlotsByName(page2)

    def retranslate(self, page2):
        _translate = QtCore.QCoreApplication.translate
        page2.setWindowTitle(_translate("page2", "MainWindow"))
        self.label_2.setText(_translate("page2", "page2"))
        self.bnt2.setText(_translate("Main", "btn2"))

class Page1(QtWidgets.QMainWindow, W_page1):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup(self)

class Page2(QtWidgets.QMainWindow, W_page2):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup(self)

class VLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(self.VLine | self.Sunken)


class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        self.stacked = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked)

        self.window_page1 = Page1(self)
        self.window_page2 = Page2(self)
        self.w_p1 = W_page1()
        self.w_p2 = W_page2()

        self.stacked.addWidget(self.window_page1)
        self.stacked.addWidget(self.window_page2)

        self.w_p1.bnt.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        self.w_p2.bnt_2.clicked.connect(lambda: self.stacked.setCurrentIndex(1))
#         self.statusBar().addPermanentWidget(VLine())
#         self.statusBar().addPermanentWidget(self.bnt)
#         self.statusBar().addPermanentWidget(VLine())
#         self.statusBar().addPermanentWidget(self.bnt_2)
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.resize(450, 600)  # <---- (450, 800)
    window.show()
    sys.exit(app.exec_())
