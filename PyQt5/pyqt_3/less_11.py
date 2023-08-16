# http://it.kgsu.ru/Python_Qt/oglav.html
# Запуск второго потока из первого и главного потока из второго
# #  -*- coding:   utf-8  -*-
# from PyQt5 import QtCore, QtWidgets
# class Thread1(QtCore.QThread):
#     s1 = QtCore.pyqtSignal(int)
#     def __init__(self, parent=None):
#         QtCore.QThread.__init__(self, parent)
#         self.count = 0
#     def run(self):
#         self.exec_()       # Запускаем цикл обработки сигналов
#     def on_start(self):
#         self.count += 1
#         self.s1.emit(self.count)
#
# class Thread2(QtCore.QThread):
#     s2 = QtCore.pyqtSignal(str)
#     def __init__ (self, parent=None):
#         QtCore.QThread.__init__(self, parent)
#     def run(self):
#         self.exec_()       # Запускаем цикл обработки сигналов
#     def on_change(self, i):
#         i += 10
#         self.s2.emit("%d" % i)
#
# class MyWindow(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.label = QtWidgets.QLabel("Нажмите кнопку")
#         self.label.setAlignment(QtCore.Qt.AlignHCenter)
#         self.button = QtWidgets.QPushButton("Сгенерировать сигнал")
#         self.vbox = QtWidgets.QVBoxLayout()
#         self.vbox.addWidget(self.label)
#         self.vbox.addWidget(self.button)
#         self.setLayout(self.vbox)
#         self.thread1 = Thread1()
#         self.thread2 = Thread2()
#         self.thread1.start()
#         self.thread2.start()
#         self.button.clicked.connect(self.thread1.on_start)
#         self.thread1.s1.connect(self.thread2.on_change)
#         self.thread2.s2.connect(self.on_thread2_s2)
#     def on_thread2_s2(self, s):
#         self.label.setText(s)
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWindow()
#     window.setWindowTitle("Обмен сигналами между потоками")
#     window.resize(300, 70)
#     window.show()
#     sys.exit(app.exec_())
#  -*- coding:   utf-8  -*-

# from PyQt5 import QtCore, QtWidgets
# import queue
#
# class MyThread(QtCore.QThread):
#     task_done = QtCore.pyqtSignal(int, int, name = 'taskDone')
#     def __init__(self, id, queue, parent=None):
#         QtCore.QThread.__init__(self, parent)
#         self.id = id
#         self.queue = queue
#     def run(self):
#         while True:
#             print("runs1")
#             task = self.queue.get()            # Получаем задание
#             print("runs2")
#             self.sleep(5)                      # Имитируем обработку
#             print("runs3")
#             self.task_done.emit(task, self.id) # Передаем данные обратно
#             print("runs4")
#             self.queue.task_done()
#             print("runs5")
#
# class MyWindow(QtWidgets.QPushButton):
#     def __init__(self):
#         QtWidgets.QPushButton.__init__(self)
#         self.setText("Раздать задания")
#         self.queue = queue.Queue()       # Создаем очередь
#         self.threads = []
#         for i in range(1, 3):	# Создаем потоки и запускаем
#             print("for i")
#             thread = MyThread(i, self.queue)
#             self.threads.append(thread)
#             thread.task_done.connect(self.on_task_done, QtCore.Qt.QueuedConnection)
#             thread.start()
#         self.clicked.connect(self.on_add_task)
#     def on_add_task(self):
#         for i in range(0, 11):
#             print("on_add")
#             self.queue.put(i)	  # Добавляем задания в очередь
#     def on_task_done(self, data, id):
#         print(data, "- id =", id) # Выводим обработанные данные
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWindow()
#     window.setWindowTitle("Использование модуля queue")
#     window.resize(300, 30)
#     window.show()
#     sys.exit(app.exec_())


#  -*- coding:   utf-8  -*-
from PyQt5 import QtCore, QtWidgets


class MyThread(QtCore.QThread):
    x = 10  # Атрибут класса
    mutex = QtCore.QMutex()  # Мьютекс

    def __init__(self, id, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.id = id

    def run(self):
        self.change_x()

    def change_x(self):
        MyThread.mutex.lock()  # Блокируем
        print("x =", MyThread.x, "id =", self.id)
        MyThread.x += 5
        self.sleep(2)
        print("x =", MyThread.x, "id =", self.id)
        MyThread.x += 34
        print("x =", MyThread.x, "id =", self.id)
        MyThread.mutex.unlock()  # Снимаем блокировку


class MyWindow(QtWidgets.QPushButton):
    def __init__(self):
        QtWidgets.QPushButton.__init__(self)
        self.setText("Запустить")
        self.thread1 = MyThread(1)
        self.thread2 = MyThread(2)
        self.clicked.connect(self.on_start)

    def on_start(self):
        if not self.thread1.isRunning():
            self.thread1.start()
        if not self.thread2.isRunning():
            self.thread2.start()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("Использование класса QMutex")
    window.resize(300, 30)
    window.show()
    sys.exit(app.exec_())