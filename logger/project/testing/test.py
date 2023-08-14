# -*- coding: utf-8 -*-
#Мультипроцессинг_________________________________________
# from multiprocessing import Pool
#
# def f(x):
#     return x+x
#
# if __name__ == '__main__':
#     with Pool(5) as p:
#         print(p)
#         print(p.map(f, [1, 2, 3]))

# from multiprocessing import Process
# import os
#
# def info(title):
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())
#     print(title)
#
# def f(name):
#     info('function f')
#     print('hello', name)
#
# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()

# import multiprocessing
# print("Number of cpu : ", multiprocessing.cpu_count())

# from multiprocessing import Process
#
# def print_func(continent='Asia'):
#     print('The name of continent is : ', continent)
#
# if __name__ == "__main__":  # confirms that the code is under main function
#     names = ['America', 'Europe', 'Africa']
#     print('Main')
#     procs = []
#     proc = Process(target=print_func)  # instantiating without any argument
#     procs.append(proc)
#     proc.start()
#
#     # instantiating process with arguments
#     for name in names:
#         print('Start')
#         proc = Process(target=print_func, args=(name,))
#         procs.append(proc)
#         print(name)
#         proc.start()
#         print('Start1')
#
#     # complete the processes
#     for proc in procs:
#         print('Join')
#         proc.join()


# from multiprocessing import Queue
#
# colors = ['red', 'green', 'blue', 'black']
# cnt = 1
# # instantiating a queue object
# queue = Queue()
# print('pushing items to queue:')
# for color in colors:
#     print('item no: ', cnt, ' ', color)
#     queue.put(color)
#     cnt += 1
#
# print('\npopping items from queue:')
# cnt = 0
# while not queue.empty():
#     print('item no: ', cnt, ' ', queue.get())
#     cnt += 1
#
# from multiprocessing import Lock, Process, Queue, current_process
# import time
# import queue # imported for using queue.Empty exception
#
#
# def do_job(tasks_to_accomplish, tasks_that_are_done):
#     while True:
#         try:
#             '''
#                 try to get task from the queue. get_nowait() function will
#                 raise queue.Empty exception if the queue is empty.
#                 queue(False) function would do the same task also.
#             '''
#             task = tasks_to_accomplish.get_nowait()
#             print("try")
#         except queue.Empty:
#             print("except")
#
#             break
#         else:
#             '''
#                 if no exception has been raised, add the task completion
#                 message to task_that_are_done queue
#             '''
#             print("else")
#             print(task, "task")
#             tasks_that_are_done.put(task + ' is done by ' + current_process().name)
#             time.sleep(.5)
#     return True
#
#
# def main():
#     number_of_task = 10
#     number_of_processes = 4
#     tasks_to_accomplish = Queue()
#     tasks_that_are_done = Queue()
#     processes = []
#
#     for i in range(number_of_task):
#         print("iii")
#         tasks_to_accomplish.put("Task no " + str(i))
#
#     # creating processes
#     for w in range(number_of_processes):
#         print("wwww")
#         p = Process(target=do_job, args=(tasks_to_accomplish, tasks_that_are_done))
#         processes.append(p)
#         p.start()
#
#     # completing process
#     for p in processes:
#         print("pppp")
#         p.join()
#
#     # print the output
#     while not tasks_that_are_done.empty():
#         print("while")
#         print(tasks_that_are_done.get())
#
#     return True
#
#
# if __name__ == '__main__':
#     main()
#
# from multiprocessing import Pool
#
# import time
#
# work = (["A", 5], ["B", 2], ["C", 1], ["D", 3])
#
#
# def work_log(work_data):
#     print(" Process %s waiting %s seconds" % (work_data[0], work_data[1]))
#     time.sleep(int(work_data[1]))
#     print(" Process %s Finished." % work_data[0])
#
#
# def pool_handler():
#     p = Pool(5)
#     p.map(work_log, work)
#
#
# if __name__ == '__main__':
#     pool_handler()
#____________________________________________________________
#Потоки _____________________________________________________
# import logging
# import threading
# import time

# def thread_function(name):
#     logging.info("Thread %s: starting", name)
#     time.sleep(2)
#     logging.info("Thread %s: finishing", name)

# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     threads = list()
#     for index in range(3):
#         logging.info("Main    : create and start thread %d.", index)
#         x = threading.Thread(target=thread_function, args=(index,))
#         threads.append(x)
#         x.start()
#
#     for index, thread in enumerate(threads):
#         logging.info("Main    : before joining thread %d.", index)
#         thread.join()
#         logging.info("Main    : thread %d done", index)

# import concurrent.futures
#
# # [rest of code]
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         executor.map(thread_function, range(3))

import logging
import threading
import time
import concurrent.futures

# class FakeDatabase:
#     def __init__(self):
#         self.value = 0
#
#     def update(self, name):
#         logging.info("Thread %s: starting update", name)
#         local_copy = self.value
#         local_copy += 2
#         time.sleep(.1)
#         self.value = local_copy
#         logging.info("Thread %s: finishing update", name)
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     database = FakeDatabase()
#     logging.info("Testing update. Starting value is %d.", database.value)
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         for index in range(1):
#             executor.submit(database.update, index)
#             print("For")
#     logging.info("Testing update. Ending value is %d.", database.value)
#
# # https://realpython.com/intro-to-python-threading/
# class FakeDatabase:
#     def __init__(self):
#         self.value = 0
#         self._lock = threading.Lock()
#
#     def locked_update(self, name):
#         logging.info("Thread %s: starting update", name)
#         logging.debug("Thread %s about to lock", name)
#         with self._lock:
#             logging.debug("Thread %s has lock", name)
#             local_copy = self.value
#             local_copy += 1
#             time.sleep(0.1)
#             self.value = local_copy
#             logging.debug("Thread %s about to release lock", name)
#         logging.debug("Thread %s after release", name)
#         logging.info("Thread %s: finishing update", name)

# from time import perf_counter
#
#
# def replace(filename, substr, new_substr):
#     print(f'Обрабатываем файл {filename}')
#     # получаем содержимое файла
#     with open(filename, 'r') as f:
#         content = f.read()
#
#     # заменяем substr на new_substr
#     content = content.replace(substr, new_substr)
#
#     # записываем данные в файл
#     with open(filename, 'w') as f:
#         f.write(content)
#
#
# def main():
#     filenames = [
#         'd:/temp/test1.txt',
#         'd:/temp/test2.txt',
#         'd:/temp/test3.txt',
#         'd:/temp/test4.txt',
#         'd:/temp/test5.txt',
#         'd:/temp/test6.txt',
#         'd:/temp/test7.txt',
#         'd:/temp/test8.txt',
#         'd:/temp/test9.txt',
#         'd:/temp/test10.txt',
#     ]
#
#     for filename in filenames:
#         replace(filename, 'ids', 'id')
#
#
# if __name__ == "__main__":
#     start_time = perf_counter()
#
#     main()
#
#     end_time = perf_counter()
#     print(f'Выполнение заняло {end_time- start_time :0.2f} секунд.')
#
# from threading import Thread
# from time import perf_counter
#
#
# def replace(filename, substr, new_substr):
#     print(f'Обрабатываем файл {filename}')
#     # получаем содержимое файла
#     with open(filename, 'r') as f:
#         content = f.read()
#
#     # заменяем substr на new_substr
#     content = content.replace(substr, new_substr)
#
#     # записываем данные в файл
#     with open(filename, 'w') as f:
#         f.write(content)
#
#
# def main():
#     filenames = [
#         'd:/temp/test1.txt',
#         'd:/temp/test2.txt',
#         'd:/temp/test3.txt',
#         'd:/temp/test4.txt',
#         'd:/temp/test5.txt',
#         'd:/temp/test6.txt',
#         'd:/temp/test7.txt',
#         'd:/temp/test8.txt',
#         'd:/temp/test9.txt',
#         'd:/temp/test10.txt',
#     ]
#
#     # создаем потоки
#     threads = [Thread(target=replace, args=(filename, 'id', 'ids'))
#             for filename in filenames]
#
#     # запускаем потоки
#     for thread in threads:
#         thread.start()
#
#     # ждем завершения потоков
#     for thread in threads:
#         thread.join()
#
#
# if __name__ == "__main__":
#     start_time = perf_counter()
#
#     main()
#
#     end_time = perf_counter()
#     print(f'Выполнение заняло {end_time- start_time :0.2f} секунд.')

from threading import Thread
from time import sleep
# def func():
#     for i in range(5):
#         print(f"from child thread: {i}")
#         sleep(0.5)

# th = Thread(target=func)
# th.start()
# for i in range(5):
#     print(f"from main thread: {i}")
#     sleep(1)

# th1 = Thread(target=func)
# th2 = Thread(target=func)
# th1.start()
# th2.start()
# th1.join()
# th2.join()
# print("--> stop")

# th = Thread(target=func)
# print(f"thread status: {th.is_alive()}")
# th.start()
# print(f"thread status: {th.is_alive()}")
# sleep(5)
# print(f"thread status: {th.is_alive()}")

# from threading import Condition, Thread
# from queue import Queue
# from time import sleep
# cv = Condition()
# q = Queue()
# # Consumer function for order processing
# def order_processor(name):
#    while True:
#        with cv:
#            # print("with cv")
#            # Wait while queue is empty
#            while q.empty():
#                print("while")
#                cv.wait()
#            try:
#                # Get data (order) from queue
#                order = q.get_nowait()
#                print(f"{name}: {order}")
#                # If get "stop" message then stop thread
#                if order == "stop":
#                    print("stop")
#                    break
#            except:
#                print("except")
#                pass
#            sleep(0.1)
# # Run order processors
# Thread(target=order_processor, args=("thread 1",)).start()
# Thread(target=order_processor, args=("thread 2",)).start()
# Thread(target=order_processor, args=("thread 3",)).start()
# # Put data into queue
# for i in range(10):
#    # print("for i")
#    q.put(f"order {i}")
# # Put stop-commands for consumers
# for _ in range(3):
#    # print("for _")
#    q.put("stop")
# # Notify all consumers
# with cv:
#    cv.notify_all()
#    print("with")


#Семафоры
# from threading import Thread, BoundedSemaphore
# from time import sleep, time
# ticket_office = BoundedSemaphore(value=3)
# def ticket_buyer(number):
#    start_service = time()
#    print("def")
#    with ticket_office:
#        print("with")
#        sleep(1)
#        print(f"client {number}, service time: {time() - start_service}")
# buyer = [Thread(target=ticket_buyer, args=(i,)) for i in range(5)]
# for b in buyer:
#    print("for b")
#    b.start()

#События
# from threading import Thread, Event
# from time import sleep, time
# event = Event()
# def worker(name: str):
#    event.wait()
#    print(f"Worker: {name}")
# # Clear event
# event.clear()
# # Create and start workers
# workers = [Thread(target=worker, args=(f"wrk {i}",)) for i in range(5)]
# for w in workers:
#    w.start()
# print("Main thread")
# event.set()

#Таймеры
# from threading import Timer
# from time import sleep, time
# timer = Timer(interval=3,function=lambda: print("Message from Timer!"))
# timer.start()


# -*- coding: utf-8 -*-
# from PyQt5 import QtCore, QtWidgets
#
#
# class MyThread(QtCore.QThread):
#     mysignal = QtCore.pyqtSignal(str)
#
#     def __init__(self, parent=None):
#         QtCore.QThread.__init__(self, parent)
#
#     def run(self):
#         for i in range(1, 21):
#             self.sleep(3)  # "Засыпаем" на 3 секунды
#             # Передача данных из потока через сигнал
#             self.mysignal.emit("i = %s" % i)
#
#
# class MyWindow(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.label = QtWidgets.QLabel("Нажмите кнопку для запуска потока")
#         self.label.setAlignment(QtCore.Qt.AlignHCenter)
#         self.button = QtWidgets.QPushButton("Запустить процесс")
#         self.vbox = QtWidgets.QVBoxLayout()
#         self.vbox.addWidget(self.label)
#         self.vbox.addWidget(self.button)
#         self.setLayout(self.vbox)
#         self.mythread = MyThread()  # Создаем экземпляр класса
#         self.button.clicked.connect(self.on_clicked)
#         self.mythread.started.connect(self.on_started)
#         self.mythread.finished.connect(self.on_finished)
#         self.mythread.mysignal.connect(self.on_change, QtCore.Qt.QueuedConnection)
#
#     def on_clicked(self):
#         self.button.setDisabled(True)  # Делаем кнопку неактивной
#         self.mythread.start()  # Запускаем поток
#
#     def on_started(self):  # Вызывается при запуске потока
#         self.label.setText("Вызван метод on_started ()")
#
#     def on_finished(self):  # Вызывается при завершении потока
#         self.label.setText("Вызван метод on_finished()")
#         self.button.setDisabled(False)  # Делаем кнопку активной
#
#     def on_change(self, s):
#         self.label.setText(s)
#
#
# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWindow()
#     window.setWindowTitle("Использование класса QThread")
#     window.resize(300, 70)
#     window.show()
#     sys.exit(app.exec_())


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *


class Ui_Win1(object):
    def setupUi(self, Win1):
        Win1.setObjectName("Win1")
        Win1.resize(450, 800)
        self.widgetWin1 = QtWidgets.QWidget(Win1)
        self.widgetWin1.setObjectName("widgetWin1")

        self.text1 = QtWidgets.QLabel(self.widgetWin1)
        self.text1.setGeometry(QtCore.QRect(197, 378, 56, 16))
        self.text1.setObjectName("text1")

        Win1.setCentralWidget(self.widgetWin1)
        self.retranslateUi(Win1)
        QtCore.QMetaObject.connectSlotsByName(Win1)

    def retranslateUi(self, Win1):
        _translate = QtCore.QCoreApplication.translate
        Win1.setWindowTitle(_translate("Win1", "MainWindow"))
        self.text1.setText(_translate("Win1", "Win1"))


class Ui_Win2(object):
    def setupUi(self, Win2):
        Win2.setObjectName("Win2")
        Win2.resize(450, 800)
        self.widgetWin2 = QtWidgets.QWidget(Win2)
        self.widgetWin2.setObjectName("widgetWin2")
        self.text2 = QtWidgets.QLabel(self.widgetWin2)
        self.text2.setGeometry(QtCore.QRect(197, 378, 56, 16))
        self.text2.setObjectName("text2")

        Win2.setCentralWidget(self.widgetWin2)
        self.retranslateUi(Win2)
        QtCore.QMetaObject.connectSlotsByName(Win2)

    def retranslateUi(self, Win2):
        _translate = QtCore.QCoreApplication.translate
        Win2.setWindowTitle(_translate("Win2", "MainWindow"))
        self.text2.setText(_translate("Win2", "Win2"))


class Ui_Win3(object):
    def setupUi(self, Win3):
        Win3.setObjectName("Win3")
        Win3.resize(450, 800)
        self.widgetWin3 = QtWidgets.QWidget(Win3)
        self.widgetWin3.setObjectName("widgetWin3")
        self.text3 = QtWidgets.QLabel(self.widgetWin3)
        self.text3.setGeometry(QtCore.QRect(197, 378, 56, 16))
        self.text3.setObjectName("text3")

        Win3.setCentralWidget(self.widgetWin3)

        self.retranslateUi(Win3)
        QtCore.QMetaObject.connectSlotsByName(Win3)

    def retranslateUi(self, Win3):
        _translate = QtCore.QCoreApplication.translate
        Win3.setWindowTitle(_translate("Win3", "MainWindow"))
        self.text3.setText(_translate("Win3", "Win3"))


class Win1(QtWidgets.QMainWindow, Ui_Win1):
    def __init__(self, parent=None):
        super(Win1, self).__init__(parent)
        self.setupUi(self)


class Win2(QtWidgets.QMainWindow, Ui_Win2):
    def __init__(self, parent=None):
        super(Win2, self).__init__(parent)
        self.setupUi(self)


class Win3(QtWidgets.QMainWindow, Ui_Win3):
    def __init__(self, parent=None):
        super(Win3, self).__init__(parent)
        self.setupUi(self)


class VLine(QFrame):
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine | self.Sunken)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.stacked = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked)

        self.window_Win1 = Win1(self)
        self.window_Win2 = Win2(self)
        self.window_Win3 = Win3(self)

        self.stacked.addWidget(self.window_Win1)
        self.stacked.addWidget(self.window_Win2)
        self.stacked.addWidget(self.window_Win3)

        # +++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        self.statusBar().showMessage("bla-bla bla")

        self.bnt = QtWidgets.QPushButton('bnt')
        self.bnt_2 = QtWidgets.QPushButton('bnt_2')
        self.bnt_3 = QtWidgets.QPushButton('bnt_3')

        self.bnt.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        self.bnt_2.clicked.connect(lambda: self.stacked.setCurrentIndex(1))
        self.bnt_3.clicked.connect(lambda: self.stacked.setCurrentIndex(2))

        self.statusBar().reformat()
        self.statusBar().setStyleSheet('border: 0; background-color: #FFF8DC;')
        self.statusBar().setStyleSheet("QStatusBar::item {border: none;}")

        self.statusBar().addPermanentWidget(VLine())
        self.statusBar().addPermanentWidget(self.bnt)
        self.statusBar().addPermanentWidget(VLine())
        self.statusBar().addPermanentWidget(self.bnt_2)
        self.statusBar().addPermanentWidget(VLine())
        self.statusBar().addPermanentWidget(self.bnt_3)
        self.statusBar().addPermanentWidget(VLine())
    # +++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(450, 600)  # <---- (450, 800)
    window.show()
    sys.exit(app.exec_())