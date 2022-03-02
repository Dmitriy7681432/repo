import time
import random
import sys
#Задача 1
# def show(f):
#     def func(*args,**kwargs):
#         start_time = time.time()
#         print(start_time)
#         f(*args,**kwargs)
#         time.sleep(3.245)
#         stop_time = time.time()
#         print(stop_time)
#         print(f'Время выполнения функции:{stop_time-start_time}')
#     return func
#
# @show
# def func1():
#     a = ['Volvo','BMW','Audio','Lada','Lexus']
#     b =[]
#     c =[]
#     for i in a:
#         b.append(i)
#     for i in b:
#         c.append(i)
#     print(b)
#     for i in range(60):
#         c.append(i)
#     print(c)
#     for i in c:
#         if not isinstance(i,str):
#             i=i+2
#             b.append(i)
#     print(b)
#
# func1()

#Задача 2  и 4
def list_ls(n):
    list_n = [i for i in range(n)]
    return list_n

start = time.time()
func_ls = list_ls(1000001)
stop = time.time()
time_list = stop-start
memory_list = sys.getsizeof(func_ls)
print(f'Время создания списка с элементами от 1 до 1000000: {time_list}.\nОбъем оперативной памяти: {memory_list}')

#Задание 3
def show(f):
    def func(*args,**kwargs):
        print(f(*args,**kwargs))
        print('Объем ОЗУ:',sys.getsizeof(f))
    return func

@show
def func1(a,b):
    x = random.randint(a,b)
    return x

func1(1,1000000)
func1(1,10000000000)
func1(1,100000000000000)



