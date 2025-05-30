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
from PyQt5 import QtCore, QtGui, QtWidgets,
import PyQt5.Qt
import PyQt5.QtWidgets.

class Id:
    id_lst = []
    # def __init__(self):
    #     pass
    # def id_func(self):
    #     self.id_lst = []
    # def id_ap(self):
    #
    #     return self.id_lst

class MyLineEdit(QtWidgets.QLineEdit,Id):
    def __init__(self):
        super().__init__()
        self.id = None
        self.id_lst = Id.id_lst

    def event(self, e):
        if e.type() == QtCore.QEvent.Shortcut:
            print(self.id)
            if self.id == e.shortcutId():
                self.id_lst.append(self.id)
                self.setFocus(QtCore.Qt.ShortcutFocusReason)
                return True
        return QtWidgets.QLineEdit.event(self, e)

class MyWindow(QtWidgets.QWidget,Id):
    def __init__ (self):
        super().__init__()
        self.tmp1 =0;self.tmp2=0;
        self.resize(300, 100)
        self.label = QtWidgets.QLabel("Устано&вить фокус на поле 1")
        self.lineEdit1 = QtWidgets.QLineEdit()
        self.label.setBuddy(self.lineEdit1)
        self.lineEdit2 = MyLineEdit()
        # self.lineEdit2 = QtWidgets.QLineEdit()
        self.lineEdit2.id = self.lineEdit2.grabShortcut(
            QtGui.QKeySequence(PyQt5.Qt.Qt.Key_Up))
        print(self.lineEdit2.id)
        self.lineEdit3 = MyLineEdit()
        # self.lineEdit3 = QtWidgets.QLineEdit()
        self.lineEdit3.id = self.lineEdit3.grabShortcut(
            QtGui.QKeySequence(PyQt5.Qt.Qt.Key_Up))
        self.button = QtWidgets.QPushButton("&Убрать фокус с поля 1")
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.lineEdit1)
        self.vbox.addWidget(self.lineEdit2)
        self.vbox.addWidget(self.lineEdit3)
        self.vbox.addWidget(self.button)
        self.setLayout(self.vbox)
        self.button.clicked.connect(self.on_clicked)
    def on_clicked(self):
        self.lineEdit1.clearFocus()
        print(self.id_lst)
        self.id_lst.clear()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
