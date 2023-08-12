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
class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def locked_update(self, name):
        logging.info("Thread %s: starting update", name)
        logging.debug("Thread %s about to lock", name)
        with self._lock:
            logging.debug("Thread %s has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("Thread %s about to release lock", name)
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)