'''
import sys
simple_list = [x**3 for x in range(100)]
print(type(simple_list))
#for i in simple_list:
#    print(i)
print('Memory: ',sys.getsizeof(simple_list))
# Неявные генераторы
simple_generator = (x**3 for x in range(100))
#for i in simple_generator:
#    print(i)
print('Memory: ',sys.getsizeof(simple_generator))
# Явные генераторы
# Простой пример
def generator_example_1(num):
    for i in range(num):
        yield(i**3)
gen = generator_example_1(10)
print(next(gen))
print(next(gen))
print(next(gen))
'''
# Сложный пример

import time
import os
import random
import psutil
#
# colors = ['White', 'Black', 'Green']
# brands = ['Volvo', 'Lada', 'Audi']
# '''
# def cars(num):
#     cars_list = []
#     for i in range(num):
#         car = {'colocr': random.choice(colors),
#                'brand': random.choice(brands),
#                'id':i}
#         cars_list.append(car)
#     return cars_list
# proc = psutil.Process(os.getpid())
# print('Исп. память до вып. функции:' + str(proc.memory_info().rss/1000000))
# start=time.clock()
# cars_list = cars(1000000)
# stop=time.clock()
# proc=psutil.Process(os.getpid())
# print('Исп. память после вып. функции:'+str(proc.memory_info().rss/1000000))
# print("Заняло {} секунд".format(stop-start))
# '''
# Применим генератор!

def cars_gen(num):
    for i in range(num):
        car = {'colocr': random.choice(colors),
               'brand': random.choice(brands),
               'id':i}
        yield car


proc = psutil.Process(os.getpid())

print('Исп. память до вып. функции:' + str(proc.memory_info().rss/1000000))
start=time.perf_counter()
print('start:',start)
cars_generator = cars_gen(1000000)
stop=time.perf_counter()
print('stop:',stop)

proc=psutil.Process(os.getpid())
print('Исп. память после вып. функции:'+str(proc.memory_info().rss/1000000))
print("Заняло {} секунд".format(stop-start))
