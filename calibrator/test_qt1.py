# -*- coding: utf-8 -*-
# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets
#
#
# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.resize(506, 312)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#
#         self.hbox = QtWidgets.QHBoxLayout(self.centralwidget)
#
#         self.toolButton = QtWidgets.QToolButton(self.centralwidget)
#         # self.toolButton.setGeometry(QtCore.QRect(220, 120, 41, 41))
#         self.toolButton1 = QtWidgets.QToolButton(self.centralwidget)
#         # self.toolButton1.setGeometry(QtCore.QRect(120, 20, 141, 41))
#
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
#         self.toolButton.setSizePolicy(sizePolicy)
#         self.toolButton.setMaximumSize(QtCore.QSize(300, 100))
#         self.hbox.addWidget(self.toolButton)
#         self.hbox.addWidget(self.toolButton1)
#
#         # icon = QtGui.QIcon()
#         # icon.addPixmap(QtGui.QPixmap("exiticon.png [exact location of image]"),
#         #                QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         #
#         # # adding icon to the toolbutton
#         # self.toolButton.setIcon(icon)
#         MainWindow.setCentralWidget(self.centralwidget)
#
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#         # adding signal and slot
#         self.toolButton.clicked.connect(self.exitapp)
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#
#         # For closing the application
#     #
#     def exitapp(self):
#         sys.exit()
#
#
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
import sys

# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit
#
#
# class Window(QMainWindow):  # Создаем класс Window, который наследует все от класса QMainWindow
#     def __init__(self):  # Создаем конструктор
#         super().__init__()  # С помощью функции super вызывем конструктор из родительского класса
#
#         self.setGeometry(700, 200, 450, 650)  # Выбираем отступы, ширу и высоту окна
#         self.setWindowTitle('КБЖУ')  # Указываем название приложения
#
#         self.heading = QLabel()  # Создаем заголовок приложения
#         self.heading.setText('Заголовок')  # Текст в этом заголовке
#         self.heading.setStyleSheet('background-color: rgb(68, 207, 203);')  # Фон заголовка
#
#         self.text_edit = QTextEdit()
#
#         self.button_close = QPushButton('Закрыть')
#         self.button_close.clicked.connect(self.close)
#
#         self.button_save = QPushButton('Сохранить')
#
#         layout_buttons = QHBoxLayout()
#         layout_buttons.addWidget(self.button_save)
#         layout_buttons.addWidget(self.button_close)
#
#         main_layout = QVBoxLayout()
#         main_layout.addWidget(self.heading)
#         main_layout.addWidget(self.text_edit)
#         main_layout.addLayout(layout_buttons)
#
#         central_widget = QWidget()
#         central_widget.setLayout(main_layout)
#
#         self.setCentralWidget(central_widget)
#
#
# # Функция которая создает приложение
# def main():
#     app = QApplication(sys.argv)  # создаем объект в качестве параметра предаём информацию о системе
#
#     window = Window()  # Создаем объект(Окно  приложения) на основе нашего класса Window
#     window.show()  # Метод show показывает созданное окно
#
#     sys.exit(app.exec_())  # Корректное закрытие приложения
#
#
# if __name__ == '__main__':
#     main()

# from PyQt5 import QtCore, QtWidgets, QtGui
# import sys
# from PyQt5.QtWidgets import QSpinBox
# # Создаем класс делегата
# class pinBoxDelegate(QtWidgets.QStyledItemDelegate):
#     def createEditor(self, parent, options, index):
#         # Создаем компонент-редактор, используемый для правки значений
#         # количества позиций
#         editor = QtWidgets.QSpinBox(parent)
#         editor.setFrame(False)
#         editor.setMinimum(0)
#         editor.setSingleStep(1)
#         return editor
#     def setEditorData(self, editor, index):
#         # Заносим в компонент-редактор значение количества
#         value = int(index.model().data(index, QtCore.Qt.EditRole))
#         editor.setValue(value)
#     def updateEditorGeometry(self, editor, options, index):
#         # Указьзаем размеры компонента-редактора
#         editor.setGeometry(options.rect)
#     def setModelData(self, editor, model, index):
#         # Заносим исправленное значение количества в модель
#         value = str(editor.value())
#         model.setData(index, value, QtCore.Qt.EditRole)
#
# app = QtWidgets.QApplication(sys.argv)
# window = QtWidgets.QTableView()
# window.setWindowTitle("Использование делегата")
# sti = QtGui.QStandardItemModel(parent=window)
# lst1 = ['Дискета', 'Бумага для принтера', 'Барабан для принтера']
# lst2 = ["10", "3", "8"]
# for row in range(0, 3):
#     item1 = QtGui.QStandardItem(lst1[row])
#     item2 = QtGui.QStandardItem(lst2[row])
#     sti.appendRow([item1, item2])
# sti.setHorizontalHeaderLabels(['Товар', 'Кол-во'])
# window.setModel(sti)
# # Назначаем делегат второму столбцу таблицы
# # window.setItemDelegateForColumn(1, SpinBoxDelegate())
# window.setColumnWidth(0, 150)
# window.resize(300, 150)
# window.show()
# sys.exit(app.exec_())

# import sys
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5       import QtWidgets, QtGui, QtCore
# from PyQt5.QtGui import QBrush, QColor
#
# class Widget(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         lay = QtWidgets.QVBoxLayout(self)
#
#         self.listView = QtWidgets.QListView()
#         self.label    = QtWidgets.QLabel("Please Select item in the QListView")
#         lay.addWidget(self.listView)
#         lay.addWidget(self.label)
#
#         model = QStringListModel()
#         textList = list()
#         textList = ["Itemname1", "Itemname2", "Itemname3", "Itemname4", "Itemname5", "Itemname6", "Itemname7", "Itemname8"]
#         model.setStringList(textList)
#         self.listView.setModel(model)
#
#         self.listView.clicked[QtCore.QModelIndex].connect(self.on_clicked)
#
#     def on_clicked(self, index):
#         item = self.listView.selectedIndexes()
#         print(item)
#
# if __name__ == '__main__':
#
#     app = QtWidgets.QApplication(sys.argv)
#     w = Widget()
#     w.show()
#     sys.exit(app.exec_())


# from PyQt5 import Qt
#
#
# class W(Qt.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.table = Qt.QTableWidget(3, 1)
#         self.table.itemChanged.connect(self.on_item)
#         self.setCentralWidget(self.table)
#
#     def on_item(self):
#         item = self.table.currentItem()
#         try:
#             n = float(item.text())
#             self.statusBar().showMessage('OK')
#         except:
#             item.setText('')
#             self.statusBar().showMessage('ERROR')
#
#
# if __name__ == "__main__":
#     app = Qt.QApplication([])
#     w = W()
#     w.show()
#     app.exec_()
#
# import sys
# from PyQt5.QtWidgets import *
#
#
# class MainInterface(QMainWindow):
#
#     def __init__(self, tuple_of_dict: tuple = None):
#         super().__init__()
#
#         self.__tuple_of_dict = tuple_of_dict
#
#         self.centralWidget = QWidget()
#         self.setCentralWidget(self.centralWidget)
#
#         self.setMinimumHeight(400)
#         self.setMinimumWidth(650)
#
#         table = QTableWidget()
#
#         if self.__tuple_of_dict:
#             table_headers = tuple(self.__tuple_of_dict[0].keys())
#
#             table.setColumnCount(len(table_headers))
#             table.setRowCount(len(self.__tuple_of_dict))
#             table.setHorizontalHeaderLabels(table_headers)
#             for num, row in enumerate(self.__tuple_of_dict):
#                 for column in table_headers:
#                     if isinstance(row[column], bool):
#                         row[column] = "True" if row[column] else "False"
#                     elif isinstance(row[column], type(None)):
#                         row[column] = "None"
#                     row_item = QTableWidgetItem(row[column])
#                     table.setItem(num, table_headers.index(column), row_item)
#                     row_item.setToolTip(row[column])
#         table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch) # вот так
#         box = QGroupBox("Table")
#         h_layout = QHBoxLayout(box)
#         h_layout.addWidget(table)
#
#         g_layout = QGridLayout(self.centralWidget)
#         g_layout.addWidget(box, 1, 1)
#
#
# if __name__ == '__main__':
#     result = ({"id": "673543", "devicename": "bla_bla_bla", "description": "My Fancy Device", "another": "value"}, )
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
#     ex = MainInterface(tuple_of_dict=result)
#     ex.show()
#     sys.exit(app.exec_())

# import sys
#
# from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QTextEdit, QListWidgetItem, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy
# from PyQt5.QtGui import QTextOption, QFont
# from PyQt5.QtCore import Qt
#
# # Кастомный виджет для вставки в строку QListWidget
# class ListRowWidget(QWidget):
#     def __init__(self):
#         super(ListRowWidget, self).__init__()
#
#         lay = QHBoxLayout()
#         lay.setMargin(0)
#         self.dummy = QWidget()
#         self.dummy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.edit = QTextEdit()
#         self.edit.setFrameShape(QFrame.NoFrame)
#         self.edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         font = QFont()
#         font.setPointSize(16)
#         self.edit.setFont(font)
#         self.edit.setReadOnly(True);
#
#         # Перенос строки, если не хватило места
#         self.edit.setWordWrapMode(QTextOption.WrapAnywhere)
#
#         # Выключаем вертикальный скролбар
#         self.edit.verticalScrollBar().hide()
#
#         self.setLayout(lay)
#
#     # Сообщение
#     def setText(self, text):
#         self.edit.setText(text)
#
#     # Выравнивание
#     def setAlignment(self, alignment):
#         if self.layout().count() > 0:
#             self.layout().removeWidget(self.dummy)
#             self.layout().removeWidget(self.edit)
#
#         if alignment == Qt.AlignLeft:
#             self.layout().addWidget(self.dummy)
#             self.layout().addWidget(self.edit)
#         else:
#             self.layout().addWidget(self.edit)
#             self.layout().addWidget(self.dummy)
#
#     def size(self):
#         return self.edit.document().size().toSize()
#
# class Widget(QWidget):
#     def __init__(self):
#         super(Widget, self).__init__()
#
#         self.load_ui()
#
#         self.sendButton.clicked.connect(self.send)
#         # Флажок для "выравнивания" сообщения (вправо-влево, поочередно)
#         self._side = False
#
#     def load_ui(self):
#         self.listWidget = QListWidget()
#         self.sendButton = QPushButton("Отправить")
#         self.textEdit = QTextEdit()
#         font = QFont()
#         font.setPointSize(16)
#         self.textEdit.setFont(font)
#         self.textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
#
#         hLay = QHBoxLayout()
#         hLay.addWidget(self.textEdit)
#         hLay.addWidget(self.sendButton)
#
#         vLay = QVBoxLayout()
#         vLay.addWidget(self.listWidget)
#         vLay.addItem(hLay)
#         self.setLayout(vLay)
#
#     def send(self):
#         # Получаем текст из поля ввода
#         text = self.textEdit.toPlainText()
#
#         # Итем для вставки в список
#         listItem = QListWidgetItem()
#         self.listWidget.addItem(listItem)
#
#         # Наш кастомный виджет отображения сообщений чата
#         listRowWidget = ListRowWidget()
#         # Передаем в него текст
#         listRowWidget.setText(text)
#
#         # Выравнивание в соответствии с "какой стороны пришло" сообщение
#         listRowWidget.setAlignment(Qt.AlignLeft if self._side else Qt.AlignRight)
#         self._side = not self._side
#
#         # Помещаем наш виджет вместо итема
#         self.listWidget.setItemWidget(listItem, listRowWidget)
#
#         # Устанавливаем размер строки списка
#         listItem.setSizeHint(listRowWidget.size())
#
# if __name__ == "__main__":
#     app = QApplication([])
#     widget = Widget()
#     widget.show()
#     sys.exit(app.exec_())

# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets
#
# class ListView(QtWidgets.QTreeView):
#     def __init__(self, *args, **kwargs):
#         super(ListView, self).__init__(*args, **kwargs)
#         self.setModel(QtGui.QStandardItemModel(self))
#         self.model().setColumnCount(2)
#         self.setRootIsDecorated(False)
#         self.setAllColumnsShowFocus(True)
#         self.setSelectionBehavior(
#             QtWidgets.QAbstractItemView.SelectRows)
#         self.setHeaderHidden(True)
#         self.header().setStretchLastSection(False)
#         self.header().setSectionResizeMode(
#             0, QtWidgets.QHeaderView.Stretch)
#         self.header().setSectionResizeMode(
#             1, QtWidgets.QHeaderView.ResizeToContents)
#
#     def addItem(self, key, value):
#         first = QtGui.QStandardItem(key)
#         second = QtGui.QStandardItem(value)
#         second.setTextAlignment(QtCore.Qt.AlignRight)
#         self.model().appendRow([first, second])
#
# class Window(QtWidgets.QWidget):
#     def __init__(self):
#         super(Window, self).__init__()
#         self.view = ListView(self)
#         for text in 'Aquamarine Red Green Purple Blue Yellow '.split():
#             self.view.addItem(text, str(16 ** len(text)))
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.addWidget(self.view)
#
# if __name__ == '__main__':
#
#     app = QtWidgets.QApplication(sys.argv)
#     window = Window()
#     window.setGeometry(600, 100, 300, 200)
#     window.show()
#     sys.exit(app.exec_())

# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5.Qt

# class Id:
#     id_lst = []
#     # def __init__(self):
#     #     pass
#     # def id_func(self):
#     #     self.id_lst = []
#     # def id_ap(self):
#     #
#     #     return self.id_lst
#
# class MyLineEdit(QtWidgets.QLineEdit,Id):
#     def __init__(self):
#         super().__init__()
#         self.id = None
#         self.id_lst = Id.id_lst
#
#     def event(self, e):
#         if e.type() == QtCore.QEvent.Shortcut:
#             print(self.id)
#             if self.id == e.shortcutId():
#                 self.id_lst.append(self.id)
#                 self.setFocus(QtCore.Qt.ShortcutFocusReason)
#                 return True
#         return QtWidgets.QLineEdit.event(self, e)
#
# class MyWindow(QtWidgets.QWidget,Id):
#     def __init__ (self):
#         super().__init__()
#         self.tmp1 =0;self.tmp2=0;
#         self.resize(300, 100)
#         self.label = QtWidgets.QLabel("Устано&вить фокус на поле 1")
#         self.lineEdit1 = QtWidgets.QLineEdit()
#         # self.label.setBuddy(self.lineEdit1)
#         self.lineEdit2 = MyLineEdit()
#         # self.lineEdit2 = QtWidgets.QLineEdit()
#         self.lineEdit2.id = self.lineEdit2.grabShortcut(
#             QtGui.QKeySequence(PyQt5.Qt.Qt.Key_Up))
#         print(self.lineEdit2.id)
#         self.lineEdit3 = MyLineEdit()
#         # self.lineEdit3 = QtWidgets.QLineEdit()
#         self.lineEdit3.id = self.lineEdit3.grabShortcut(
#             QtGui.QKeySequence(PyQt5.Qt.Qt.Key_Up))
#         self.button = QtWidgets.QPushButton("&Убрать фокус с поля 1")
#         self.vbox = QtWidgets.QVBoxLayout()
#         # self.vbox.addWidget(self.label)
#         self.vbox.addWidget(self.lineEdit1)
#         self.vbox.addWidget(self.lineEdit2)
#         self.vbox.addWidget(self.lineEdit3)
#         self.vbox.addWidget(self.button)
#         self.setLayout(self.vbox)
#         self.button.clicked.connect(self.on_clicked)
#     def on_clicked(self):
#         self.lineEdit1.clearFocus()
#         print(self.id_lst)
#         self.id_lst.clear()
#
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec_())

# class MyWidget(QtWidgets.QWidget):
#     keyPressed = QtCore.pyqtSignal(int)
#
#     def __init__(self):
#         super().__init__()
#         self.keyPressed.connect(self.on_key)
#
#     def keyPressEvent(self, event):
#         super(MyWidget, self).keyPressEvent(event)
#         self.keyPressed.emit(event.key())
#
# class My_Class():
#     def __init__(self):
#         super().__init__()
#         self.widget = MyWidget()
#         self.widget.keyPressed.connect(self.on_key)
#
#     def on_key(self,key):
#         # test for a specific key
#         if key == QtCore.Qt.Key_Return:
#             print('return key pressed')
#         else:
#             print('key pressed: %i' % key)
#
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     widget = My_Class()
#     widget.show()
#     sys.exit(app.exec_())
# import sys
# from PyQt5.QtWidgets import (QApplication, QWidget,
#                              QVBoxLayout, QProgressBar, QPushButton)
# from PyQt5.QtCore import QBasicTimer
#
#
# class Example(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.pbar = QProgressBar(self)
#         self.pbar.setGeometry(30, 40, 200, 25)
#
#         self.btn = QPushButton('Начать', self)
#         self.btn.move(30, 80)
#         self.btn.clicked.connect(self.doAction)
#
#         self.timer = QBasicTimer()
#         self.step = 0
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.pbar)
#         layout.addWidget(self.btn)
#         self.setLayout(layout)
#
#
#         self.setGeometry(300, 300, 280, 170)
#         self.setWindowTitle('Прогресс бар')
#         # self.show()
#
#     def timerEvent(self, e):
#         if self.step >= 100:
#             self.timer.stop()
#             self.btn.setText('Закончено')
#             return
#
#         self.step = self.step + 1
#         self.pbar.setValue(self.step)
#
#     def doAction(self):
#         print('doAction', self.timer.isActive())
#         if self.timer.isActive():
#             self.timer.stop()
#             self.btn.setText('Начать')
#         else:
#             self.timer.start(100, self)
#             self.btn.setText('Стоп')
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     ex.show()
#     sys.exit(app.exec_())



# print((bin(~50)))
# print((bin(-50)))
# print(bin(50))
# print(~50)
def func_tran_neg_hex_to_dec(arg):
    arg = '0x'+arg
    arg = int(arg,16)
    print(type(arg))
    t = bin(arg)
    s = str.maketrans('10','10')
    s1 = t[2:].translate(s)
    print(s1)
    s2 = (int(s1,2)+1)*-1
    # print(s2+1)
    return s2
ff = func_tran_neg_hex_to_dec('ffffffe7')
print('ff',ff)

value = '41b80000'
import struct
value = struct.unpack('!I', bytes.fromhex(value))
print('type',type(value[0]))
lst_val =[]
# print(tuple(value[0]))
lst_val.append(round(value[0],2))
value = lst_val.copy()
print(value)

a = '0xffffffe7'
# print(hex(int(a,16)))
print(type(int(a,16)))

# val = b'00000000'
# value = value.decode('utf-8')
# print('val',value)
with open(f'test.bin', 'wb') as f:
    for i in range(0, 7):
        # val_h = struct.pack('I',0xa5a55a5a)
        value = -1515890086
        out_byte_array = [bytearray(value.to_bytes(length=4, byteorder="little",signed=True))]
        print(out_byte_array)
        f.write(out_byte_array[0])

out_byte_array = bytearray(0xA5A55A5A.to_bytes(length=4, byteorder="little"))
print(out_byte_array)
temp = {'preset': [2779077210, 2126990577, 352789792, 1586708, 4077122392, 0, 120], 'calibr': [2779077210, 1140334099, 352789792, 2307604, 4077122392, 0, 50], 'filter': [2779077210, 2381915854, 352789792, 2438676, 4077122392, 0, 48]}


# a = 0xffffffe7
# a = bin(a)[2:]
# print(a)
# print(a.replace('1','0').replace('0','1'))
# tmp = '-25'
# if '-' in tmp:
#     print('YE')
arg1 = 'A5A55A5A'
# arg3 = '07C07598'
arg3 = '11'

# arg2 = int(arg1, 16)
arg2 = func_tran_neg_hex_to_dec(arg3)
arg2=(arg2+1)*-1

print('arg2',hex(arg2),type(arg2))
import binascii
tmp1 = 'A'
# tmp1 = hex(tmp1).encode('utf-8')
tmp1 = tmp1.encode('utf-8').hex()
print('tmp1',tmp1)
tmp2 = binascii.unhexlify(arg1)
tmp2 = int.from_bytes(tmp2,'big',signed=True)
print('tmp2',tmp2,type(tmp2),hex(tmp2))
tmp3 = -1515890086
tmp3 = bytearray(tmp3.to_bytes(length=4, byteorder="big",signed=True))
print('tmp3',tmp3)



per = bytearray(b'ZZ\xa5\xa5')
per = int.from_bytes(per,'little',signed=False)
per = hex(per)[2:].upper()
per = per[6:8] + per[4:6] + per[2:4] + per[0:2]
per = per.encode('utf-8') + b'0000'
print(per)


c = '1'
# per1 = hex(per1)
# per1 = int.from_bytes(per1, 'little', signed=False)
# per1 = int.to_bytes(per1,'little',signed=False)
c = int(c)
c = hex(c)[2:].upper()
if len(c) == 1:
    c = '0' + c + "000000"
elif len(c) == 2:
    c = c + "000000"
elif len(c) == 4:
    c = c[len(c) - 2:] + "  " + \
        c[len(c) - 4:len(c) - 2] + "0000"
elif len(c) == 6:
    c = c[len(c) - 2:] + "  " + \
        c[len(c) - 4:len(c) - 2] + "  " + c[len(c) - 6:len(c) - 4] + "00"
elif len(c) == 8:
    c = c[len(c) - 2:] + "  " + \
        c[len(c) - 4:len(c) - 2] + "  " + c[len(c) - 6:len(c) - 4] + "  " + c[len(c) - 8:len(c) - 6]
print(c)
c = c.encode('utf-8') + b'0000'
print(c)

lst_main = {'preset': {'s_zero': ['Ноль', 'int', '1', '0', '0', '0', '0', 0, 0, 0, 0], 's_one': ['Единица', 'int', '1', '1', '1', '1', '1', 1, 1, 1, 1], 's_zero_time': ['Пауза длительностью 0 мс', 'int', 'с', '0', '0', '0', '0', 0, 0, 0, 0], 's_cont_time': ['Ожидание срабатывания контактора', 'int', 'с', '0.1', '0.8', '0.8', '0.5', 100, 800, 800, 500], 's_cont_time_slow': ['Ожидание срабатывания силового контактора', 'int', 'с', '0.1', '1', '1', '2', 100, 1000, 1000, 2000], 's_14': ['T ОЖ запрета пуска ЭА,[°С]', '-int', '°С', '-25', '-50', '-50', '-10', -25, -50, -50, -10], 's_56': ['t допустимых 200 % I ОШ,[мС]', 'int', 'с', '1', '15', '15', '6', 1000, 15000, 15000, 6000], 's_96': ['t полной закачки бака,[мС]', 'int', 'с', '200', '255', '255', '600', 200000, 255000, 255000, 600000], 's_100': ['Промежуток t вычисления градиента уровня топлива', 'int', 'с', '5', '10', '10', '20', 5000, 10000, 10000, 20000], 's_108': ['t открывания люка забора ЭА, мс', 'int', 'с', '20', '50', '50', '100', 20000, 50000, 50000, 100000], 's_109': ['t закрЫвания люка забора ЭА, мс', 'int', 'с', '20', '45', '45', '100', 20000, 45000, 45000, 100000], 's_110': ['t ожидания донесения от люка забора ЭА, мс', 'int', 'с', '70', '20', '20', '110', 70000, 20000, 20000, 110000], 's_111': ['T открывания люка забора ЭА, °С', 'int', '°С', '20', '95', '95', '80', 20, 95, 95, 80], 's_112': ['T закрывания люка забора ЭА, °С', 'int', '°С', '30', '75', '75', '60', 30, 75, 75, 60], 's_172': ['Порог для фазировки', 'int', '1', '1', '1', '1', '1', 60, 1, 1, 1], 's_213': ['Время задержки максимального значения f,[мС]', 'int', 'с', '3', '5', '5', '10', 3000, 5000, 5000, 10000], 's_222': ['Нижняя граница допустимого диапазона напряжений СИПТ(с УКПТ)', 'float', 'В', '23', '24.3', '24.3', '25', 23.0, 24.299999, 24.299999, 25.0], 's_223': ['Верхняя граница допустимого диапазона напряжений СИПТ(с УКПТ)', 'float', 'В', '26', '29.7', '29.7', '28', 26.0, 29.700001, 29.700001, 28.0], 's_235': ['t ожидания включения_отключения контактора', 'int', 'с', '0.1', '0.8', '0.8', '0.5', 100, 800, 800, 500], 's_236': ['Порог для аварий у который аварийный уровень - 0', 'int', '1', '0', '0', '0', '0', 0, 0, 0, 0], 's_239': ['Низкое U АКБ', 'float', 'В', '17', '18', '18', '19', 17.0, 18.0, 18.0, 19.0], 's_240': ['t задержки низкого U АКБ', 'int', 'с', '1', '2', '2', '1.5', 1000, 2000, 2000, 1500], 's_256': ['t задержки отключения СИПТ,[мС]', 'int', 'с', '1', '6', '6', '10', 1000, 6000, 6000, 10000], 's_277': ['t открытия люка забора 2 ЭА, мс', 'int', 'с', '20', '50', '50', '100', 20000, 50000, 50000, 100000], 's_278': ['t закрытия люка забора 2 ЭА, мс', 'int', 'с', '20', '45', '45', '100', 20000, 45000, 45000, 100000], 's_279': ['t ожидания донесения от люка забора 2 ЭА, мс', 'int', 'с', '70', '20', '20', '110', 70000, 20000, 20000, 110000], 's_280': ['T открытия люка забора 2 ЭА, °С', 'int', '°С', '20', '85', '85', '80', 20, 85, 85, 80], 's_281': ['T закрытия люка забора 2 ЭА, °С', 'int', '°С', '30', '75', '75', '60', 30, 75, 75, 60], 's_285': ['Ток СИПТ 105 %', 'float', 'А', '185', '195', '195', '205', 185.0, 195.0, 195.0, 205.0], 's_286': ['t допустимых 105 % тока СИПТ', 'int', 'с', '4', '5', '5', '6', 4000, 5000, 5000, 6000], 's_287': ['КЗ СИПТ 150 %', 'float', 'А', '250', '278', '278', '300', 250.0, 278.0, 278.0, 300.0], 's_288': ['t допустимых 150 % тока СИПТ', 'int', 'с', '1', '2', '2', '3', 1000, 2000, 2000, 3000], 's_290': ['t допустимых 150 % тока СПЧ', 'int', 'с', '1', '2', '2', '3', 1000, 2000, 2000, 3000], 's_292': ['t команды ПДУ', 'int', 'с', '0.1', '0.2', '0.2', '0.3', 100, 200, 200, 300], 's_353': ['Низкое U АКБ ХД', 'float', 'В', '17', '18', '18', '19', 17.0, 18.0, 18.0, 19.0], 's_354': ['t задержки низкого U АКБ ХД', 'int', 'с', '1', '2', '2', '1.5', 1000, 2000, 2000, 1500], 's_355': ['Низкое U ИВЭП', 'float', 'В', '18', '23', '23', '23.5', 18.0, 23.0, 23.0, 23.5], 's_356': ['Высокое U ИВЭП', 'float', 'В', '27', '29', '29', '30', 27.0, 29.0, 29.0, 30.0], 's_357': ['Ток перегруза ИВЭП', 'float', 'А', '45', '50', '50', '55', 45.0, 50.0, 50.0, 55.0], 's_438': ['t срабатывания КЗ автомата фидера 2', 'int', 'с', '2', '2', '2', '2', 1113325568, 2000, 2000, 2000], 's_439': ['t срабатывания предупреждения автомата фидера 2', 'int', 'с', '2', '3', '3', '2', 2000, 3000, 3000, 2000], 's_440': ['t срабатывания КЗ автомата фидера 17', 'int', 'с', '2', '2', '2', '2', 2000, 2000, 2000, 2000], 's_441': ['t срабатывания предупреждения автомата фидера 17', 'int', 'с', '2', '3', '3', '2', 2000, 3000, 3000, 2000], 's_442': ['t срабатывания КЗ автомата фидера 18', 'int', 'с', '2', '2', '2', '2', 2000, 2000, 2000, 2000], 's_443': ['t срабатывания предупреждения автомата фидера 18', 'int', 'с', '2', '3', '3', '2', 2000, 3000, 3000, 2000], 's_444': ['t срабатывания КЗ автомата фидера 22', 'int', 'с', '2', '2', '2', '2', 2000, 2000, 2000, 2000], 's_445': ['t срабатывания предупреждения автомата фидера 22', 'int', 'с', '2', '3', '3', '2', 2000, 3000, 3000, 2000], 's_446': ['t запуска СИПТ', 'int', 'с', '3', '15', '15', '10', 3000, 15000, 15000, 10000], 's_448': ['Пониженное U АКБ', 'float', 'В', '17', '20.0', '20.0', '19', 17.0, 20.0, 20.0, 19.0], 's_455': ['T ОЖ открытия люка забоа 2 и 3', 'int', '°С', '70', '85', '85', '85', 70, 85, 85, 85], 's_456': ['T ОЖ закрытия люка забоа 2 и 3', 'int', '°С', '70', '75', '75', '85', 70, 75, 75, 85], 's_461': ['Уровень открытия люка забора', 'int', '1', '10', '30', '30', '10', 10, 30, 30, 10], 's_463': ['Уровень закрытия люка забора', 'int', '1', '90', '36', '36', '90', 90, 36, 36, 90], 's_465': ['Уровень окрытия люка забора для ПЧ1', 'int', '1', '30', '30', '30', '30', 30, 30, 30, 30], 's_466': ['Уровень окрытия люка забора для ПЧ2', 'int', '1', '30', '30', '30', '30', 30, 30, 30, 30], 's_467': ['Уровень закрытия люка забора для ПЧ1', 'int', '1', '70', '70', '70', '70', 30, 70, 70, 70], 's_468': ['Уровень закрытия люка забора для ПЧ2', 'int', '1', '70', '70', '70', '70', 70, 70, 70, 70], 's_477': ['Время выдержки запуска и останова ПЧ для АФК', 'int', 'с', '60', '40', '40', '60', 60000, 40000, 40000, 60000], 's_478': ['Время выдержки запуска и останова ПЧ для АФК', 'int', 'с', '60', '70', '70', '60', 60000, 70000, 70000, 60000], 's_480': ['Задержка запуска режима после начала открытия люка для 2 блока', 'int', 'с', '60', '4', '4', '60', 60000, 4000, 4000, 60000], 's_489': ['Разрешение изменения реакции аварий 1', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_490': ['Разрешение изменения реакции аварий 2', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_491': ['Max количество аварий для изменений их реакций', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_492': ['Элемент аварии 1', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_493': ['Элемент аварии 2', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_494': ['Элемент аварии 3', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_495': ['Элемент аварии 4', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_496': ['Элемент аварии 5', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_497': ['Элемент аварии 6', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_498': ['Значение реакции для аварии 1', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_499': ['Значение реакции для аварии 2', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 0], 's_500': ['Значение реакции для аварии 3', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_501': ['Значение реакции для аварии 4', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_502': ['Значение реакции для аварии 5', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_503': ['Значение реакции для аварии 6', 'int', '1', '5', '0', '0', '5', 5, 0, 0, 5], 's_504': ['t выхода обновления изменения реакций аварий', 'int', 'с', '5', '10', '10', '5', 5000, 10000, 10000, 5000], 's_507': ['t работы цикла сброса аварий по команде оператора', 'int', 'с', '2', '2', '2', '2', 2000, 2000, 2000, 2000], 's_508': ['количество повторений в циклe сброса аварий', 'int', '1', '2', '2', '2', '2', 2, 2, 2, 2], 's_514': ['t ожидания включения_отключения реле фидеров', 'int', 'с', '0.1', '0.8', '0.8', '0.5', 100, 800, 800, 500], 's_515': ['T включения охлаждения пульта управления, °С', 'int', '°С', '15', '35', '35', '25', 500, 35, 35, 25], 's_516': ['t срабатывания КЗ автомата фидера 2', 'int', 'с', '2', '2', '2', '2', 2000, 2000, 2000, 2000], 's_517': ['t срабатывания предупреждения автомата фидера 2', 'int', 'с', '2', '3', '3', '2', 2000, 3000, 3000, 2000], 's_518': ['T включения охлаждения пульта управления, °С', 'int', '°С', '15', '30', '30', '25', 15, 30, 30, 25], 's_519': ['Пониженное U АБ ОП', 'float', 'В', '17', '20', '20', '19', 17.0, 20.0, 20.0, 19.0], 's_520': ['t срабатывания предупреждения о пониженном U АБ ОП', 'int', 'с', '2', '5', '5', '2', 2000, 5000, 5000, 2000], 's_521': ['t срабатывания КЗ автомата Q6 экстренного отключения', 'int', 'с', '2', '3', '3', '2', 2000, 3000, 3000, 2000], 's_543': ['Порог превышающий допустимое значение наработки', 'int', '1', '98', '1200', '1200', '100', 98, 1200, 1200, 100], 's_544': ['Недопустимое значение наработки', 'int', '1', '98', '500000', '500000', '100', 98, 500000, 500000, 100], 's_545': ['Вкл/выкл анализа наработки', 'int', '1', '98', '1', '1', '100', 98, 1, 1, 100]}, 'calibr': {'U_AB_STARTER_k': ['U АБ СТ, В', '0.0209', 0.0209], 'U_AB_STARTER_b': ['U АБ СТ, В', '-41.8751', -41.875099], 'U_AB_OP_k': ['U аккумулятора ОП, В', '0.0209', 0.0209], 'U_AB_OP_b': ['U аккумулятора ОП, В', '-41.8751', -41.875099]}, 'filter': {'U_AB_STARTER_FILTER': [2685206528, 4], 'U_AB_OP_FILTER': [2685207552, 4]}}

lst_data_dict_keys = list(lst_main['preset'].keys())
print(lst_data_dict_keys)
dt_dict = lst_main['preset'].get(lst_data_dict_keys[0])
print(dt_dict)

head = {'preset': [bytearray(b'ZZ\xa5\xa5'), bytearray(b'\x13VOa'), bytearray(b' %\x06\x10'), bytearray(b'\x14Q$\x00'), bytearray(b'X\xf3\x03\xf3'), bytearray(b'\x00\x00\x00\x00'), bytearray(b'\x05\x01\x00\x00')], 'calibr': [bytearray(b'ZZ\xa5\xa5'), bytearray(b'\x0c\x18\xbd\xc4'), bytearray(b' %\x06\x10'), bytearray(b'\x14Q)\x00'), bytearray(b'X\xf3\x03\xf3'), bytearray(b'\x00\x00\x00\x00'), bytearray(b'~\x00\x00\x00')], 'filter': [bytearray(b'ZZ\xa5\xa5'), bytearray(b'R\xc2S~'), bytearray(b' %\x06\x10'), bytearray(b'\x14Q1\x00'), bytearray(b'\x14Q1\x00'), bytearray(b'\x00\x00\x00\x00'), bytearray(b'l\x00\x00\x00')]}

print(head['preset'][0:])
bb = b't65487C00D4BF581B00001025'
bb2 = b'7C00D4BF'
if bb2 in bb:
    print(bb[5:13])

val = '01000000'
val = val.encode('utf-8') + b'0000'
print(val)
