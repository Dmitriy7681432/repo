#!/usr/bin/python3
# -*- coding: utf-8 -*-
#5 - Диалоговые окна
#5.1 - QInputDialog ___________________________________
"""
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QInputDialog, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()


    def showDialog(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Enter your name:')
        if ok:
            self.le.setText(str(text))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
"""
#5.2 - QColorDialog ___________________________________
"""
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame,
    QColorDialog, QApplication,QLabel)
from PyQt5.QtGui import QColor
from PyQt5 import QtGui

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        col = QColor(0, 0, 0)

        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)

        self.btn.clicked.connect(self.showDialog)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }"
            % col.name())
        self.frm.setGeometry(130, 22, 100, 100)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Color dialog')
        self.show()


    def showDialog(self):

        col = QColorDialog.getColor()

        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                % col.name())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
"""
#5.3 - QFontDialog ___________________________________
"""
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,\
    QSizePolicy, QLabel, QFontDialog, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        vbox = QVBoxLayout()

        btn = QPushButton('Dialog', self)
        btn.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)


        btn.move(20, 20)

        vbox.addWidget(btn)

        btn.clicked.connect(self.showDialog)

        self.lbl = QLabel('Knowledge only matters', self)
        self.lbl.move(130, 20)

        vbox.addWidget(self.lbl)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Font dialog')
        self.show()


    def showDialog(self):

        font, ok = QFontDialog.getFont()
        if ok:
            self.lbl.setFont(font)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
"""
#5.4 - QFileDialog ___________________________________
import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()


    def showDialog(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        print(fname)
        if fname !=None:
            f = open(fname, 'r')
            with f:
                data = f.read()
                self.textEdit.setText(data)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

