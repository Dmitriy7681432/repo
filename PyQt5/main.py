# -*- coding: utf-8 -*-
#Уроки -  https://www.youtube.com/watch?v=eipstdomHQE&t=894s
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow
#
# import sys
#
# class Window(QMainWindow):
#     def __init__(self):
#         super(Window,self).__init__()
#
#         self.setWindowTitle("Простая программа")
#         self.setGeometry(300,250,350,200)
#
#         self.new_text = QtWidgets.QLabel(self)
#
#         self.main_text = QtWidgets.QLabel(self)
#         self.main_text.setText("Это базовая надпись")
#         self.main_text.move(100, 100)
#         self.main_text.adjustSize()
#
#         self.btn = QtWidgets.QPushButton(self)
#         self.btn.move(70,150)
#         self.btn.setText("Нажми на меня")
#         self.btn.setFixedWidth(200)
#         self.btn.clicked.connect(self.add_label)
#
#     def add_label(self):
#         self.new_text.setText("Вторая надпись")
#         self.new_text.move(100,50)
#         self.new_text.adjustSize()
#
# def application():
#     app =QApplication(sys.argv)
#     window = Window()
#
#     window.show()
#     sys.exit(app.exec_())
#
#
# if __name__ =="__main__":
#     application()

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication,QMainWindow,QMenuBar,QMenu,QFileDialog

import sys

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Редактор кода")
        self.setGeometry(300,250,350,200)

        self.text_edit =QtWidgets.QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.createMenuBar()

    def createMenuBar(self):
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)

        fileMenu = QMenu("&Файл", self)
        self.menuBar.addMenu(fileMenu)

        fileMenu.addAction('Открыть', self.action_clicked)
        fileMenu.addAction('Сохранить', self.action_clicked)

    @QtCore.pyqtSlot()
    def action_clicked(self):
        action = self.sender()
        if action.text() =="Открыть":
            fname = QFileDialog.getOpenFileName(self)[0]
            try:
                f = open(fname, "r", encoding="utf-8")
                with f:
                    data = f.read()
                    self.text_edit.setText(data)
            except FileNotFoundError:
                print("No such file")
        elif action.text() =="Сохранить":
            fname = QFileDialog.getSaveFileName(self)[0]
            try:
                f = open(fname, "w", encoding="utf-8")
                with f:
                    text = self.text_edit.toPlainText()
                    f.write(text)
            except FileNotFoundError:
                print("No such file")


def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())

if __name__ =="__main__":
    application()