#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 8 - Перетаскивание (drag & drop)
# 8.1 - Простое перетаскивание ______________________________________________
"""
import sys
from PyQt5.QtWidgets import (QPushButton, QWidget,
    QLineEdit, QApplication)

n = sys._getframe

class Button(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.setAcceptDrops(True)


    def dragEnterEvent(self, e):
        print(n().f_lineno)
        print(e.mimeData().text())

        if e.mimeData().hasFormat('text/plain'):
            print(n().f_lineno)
            e.accept()
        else:
            print(n().f_lineno)
            e.ignore()

    def dropEvent(self, e):
        print(n().f_lineno)

        self.setText(e.mimeData().text())


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        edit = QLineEdit('', self)
        edit.setDragEnabled(True)
        edit.move(30, 65)
        print(n().f_lineno)
        button = Button("Button", self)
        button.move(190, 65)

        self.setWindowTitle('Simple drag & drop')
        self.setGeometry(300, 300, 300, 150)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()
"""
# 8.2 - Перетаскивание виджета кнопки ______________________________________________
import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

n = sys._getframe

class Button(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)


    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.RightButton:
            print(n().f_lineno)
            return

        mimeData = QMimeData()
        # print(mimeData.data('text/plain'), n().f_lineno)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):

        QPushButton.mousePressEvent(self, e)

        if e.button() == Qt.LeftButton:
            print('press')


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setAcceptDrops(True)

        self.button = Button('Button', self)
        self.button.move(100, 65)

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 280, 150)


    def dragEnterEvent(self, e):

        e.accept()


    def dropEvent(self, e):

        position = e.pos()
        self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()
