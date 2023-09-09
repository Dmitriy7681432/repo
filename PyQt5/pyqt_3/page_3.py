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
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui, QtPrintSupport
import sys

app = QtWidgets.QApplication(sys.argv)
writer = QtGui.QPdfWriter("output.pdf")
writer.setCreator("ФИО")
writer.setTitle("Тест")
# Заодно поэкспериментируем с указанием параметров бумаги с помощью
# класса QPageLayout
layout = QtGui.QPageLayout()
layout.setPageSize(QtGui.QPageSize(QtGui.QPageSize.A5))
layout.setOrientation(QtGui.QPageLayout.Portrait)
writer.setPageLayout(layout)
painter = QtGui.QPainter()
painter.begin(writer)
color = QtGui.QColor(QtCore.Qt.black)
painter.setPen(QtGui.QPen(color))
painter.setBrush(QtGui.QBrush(color))
font = QtGui.QFont("Verdana", pointSize=42)
painter.setFont(font)
painter.drawText(10, writer.height() // 2 - 50, writer.width() - 20,
                 50, QtCore.Qt.AlignCenter | QtCore.Qt.TextDontClip,
                 "QPdfWriter")
layout.setOrientation(QtGui.QPageLayout.Landscape)
writer.setPageLayout(layout)
writer.newPage()
pixmap = QtGui.QPixmap("img3.jpg")
pixmap = pixmap.scaled(writer.width(),
                       writer.height(),
                       aspectRatioMode=QtCore.Qt.KeepAspectRatio)
painter.drawPixmap(0, 0, pixmap)
painter.end()
