# # -*- coding: utf-8 -*-
# from PyQt5 import QtCore, QtWidgets
# class MyWindow(QtWidgets.QWidget):
#     def __init__ (self, parent = None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.resize(300, 100)
#     def changeEvent(self, e):
#         if e.type() == QtCore.QEvent.WindowStateChange:
#             if self.isMinimized():
#                 print("Окно свернуто")
#             elif self.isMaximized():
#                 print("Окно раскрыто до максимальных размеров")
#             elif self.isFullScreen():
#                 print("Полноэкранный режим")
#             elif self.isActiveWindow():
#                 print("Окно находится в фокусе ввода")
#         # QtWidgets.QWidget.changeEvent(self, e) # Отправляем дальше
#     def showEvent(self, e):
#         print("Окно отображено")
#         # QtWidgets.QWidget.showEvent(self, e)   # Отправляем дальше
#     def hideEvent(self, e):
#         print("Окно скрыто")
#         # QtWidgets.QWidget.hideEvent(self, e)   # Отправляем дальше
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec_())

# -*- coding: utf-8 -*-
# from PyQt5 import QtWidgets
#
# class MyLineEdit(QtWidgets.QLineEdit):
#     def __init__(self, id, parent = None):
#         QtWidgets.QLineEdit.__init__(self, parent)
#         self.id = id
#     def focusInEvent(self, e):
#         print("Получен фокус полем", self.id)
#         QtWidgets.QLineEdit.focusInEvent(self, e)
#     def focusOutEvent(self, e):
#         print("Потерян фокус полем", self.id)
#         QtWidgets.QLineEdit.focusOutEvent(self, e)
#
# class MyWindow(QtWidgets.QWidget):
#     def __init__ (self, parent = None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.resize(300, 100)
#         self.button = QtWidgets.QPushButton("Установить фокус на поле 2")
#         self.line1 = MyLineEdit (1)
#         self.line2 = MyLineEdit (2)
#         self.vbox = QtWidgets.QVBoxLayout()
#         self.vbox.addWidget(self.button)
#         self.vbox.addWidget(self.line1)
#         self.vbox.addWidget(self.line2)
#         self.setLayout(self.vbox)
#         self.button.clicked.connect(self.on_clicked)
#         # Задаем порядок обхода с помощью клавиши <Tab>
#         QtWidgets.QWidget.setTabOrder(self.line1, self.line2)
#         QtWidgets.QWidget.setTabOrder(self.line2, self.button)
#     def on_clicked(self):
#         self.line2.setFocus()
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec_())

# -*- coding:   utf-8  -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
# window.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
window.setWindowTitle("Создание окна произвольной формы")
window.resize(600, 600)
pixmap = QtGui.QPixmap("fon1.png")
pal = window.palette()
pal.setBrush(QtGui.QPalette.Normal, QtGui.QPalette.Window, QtGui.QBrush(pixmap))
pal.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, QtGui.QBrush(pixmap))
window.setPalette(pal)
window.setMask(pixmap.mask())
button = QtWidgets.QPushButton ("Закрыть окно", window)
button.setFixedSize(150, 30)
button.move(220, 279)
button.clicked.connect(QtWidgets.qApp.quit)
window.show()
sys.exit(app.exec_())