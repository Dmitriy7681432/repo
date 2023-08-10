# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication,QAction

class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        btn1 = QPushButton("Вперед", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Назад", self)
        btn2.move(500, 50)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        btn1.setShortcut("F1")
        btn2.setShortcut("F2")

        self.statusBar()

        self.setGeometry(300, 300, 600, 450)
        self.setWindowTitle('Event sender')
        self.show()

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text())
        print("Click")
        main =Main1()

class Main1(Main):

    def __init__(self):
        super().__init__()
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




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
