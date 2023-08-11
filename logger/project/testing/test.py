import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

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

from multiprocessing import Process

def print_func(continent='Asia'):
    print('The name of continent is : ', continent)

if __name__ == "__main__":  # confirms that the code is under main function
    names = ['America', 'Europe', 'Africa']
    print('Main')
    procs = []
    proc = Process(target=print_func)  # instantiating without any argument
    procs.append(proc)
    proc.start()

    # instantiating process with arguments
    for name in names:
        print('Start')
        proc = Process(target=print_func, args=(name,))
        procs.append(proc)
        proc.start()
        print('Start1')

    # complete the processes
    for proc in procs:
        print('Join')
        proc.join()



