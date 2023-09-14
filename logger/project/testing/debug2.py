#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)

from PyQt5 import QtCore, QtGui, QtWidgets

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addWidget(okButton,alignment=QtCore.Qt.AlignLeft)
        hbox.addWidget(cancelButton,alignment=QtCore.Qt.AlignLeft)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.setDirection(2)
        # hbox.setContentsMargins(100, 100, 120, 100)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.setContentsMargins(100, 100, 120, 100)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())