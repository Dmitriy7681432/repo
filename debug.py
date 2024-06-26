# -*- coding: utf-8 -*-
# a = [[1,2,3,'a'],[4,5,6,'b'],[7,8,9,'c'],[10,11,12,'d']]
# b = [1,2,3]
# print(' '.join(map(str,b)))
# c = [['1', 'Programm','Java'],['2','Programm','Python']]
# d = []
# for i in c:
#    d.append('      '.join(i))
# print(d)
# for i in d:
#     print(i)
# print([b])

# import sys
# import PyQt5.QtCore as __PyQt5_QtCore
#Вывод номера строки
# s = sys._getframe
# a ="Hello"
# print(a,s().f_lineno)
# print(a,s().f_lineno)

def printf(*args):
    print(f'номер строки={traceback.extract_stack()[-2].lineno},', *args)

import traceback
# вывод номера строки
def nmb():
   print(traceback.extract_stack()[-2].lineno)

#Функия для отображения имя функции
def func():
    stack = traceback.extract_stack()
    print('Print from {}'.format(stack[-2][2]))

if __name__ == "__main__":
    # Бегущая синусоида
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib.animation import FuncAnimation
    plt.style.use('seaborn-pastel')


    fig = plt.figure()
    ax = plt.axes(xlim=(0, 4), ylim=(-2, 2))
    line, = ax.plot([], [], lw=3)

    def init():
        line.set_data([], [])
        return line,
    def animate(i):
        x = np.linspace(0, 4, 1000)
        y = np.sin(2 * np.pi * (x - 0.01 * i))
        line.set_data(x, y)
        return line,


    anim = FuncAnimation(fig, animate, init_func=init,
                         frames=200, interval=20, blit=True)
    plt.show()
