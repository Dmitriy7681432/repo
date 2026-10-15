# -*- coding: utf-8 -*-
# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np
#
# x = np.linspace(0, 10, 100)
#
# # Создаем сетку 2 строки и 1 столбец
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))
#
# # Первый график
# ax1.plot(x, np.sin(x), color='green')
# ax1.set_title('График Синуса')
# ax1.set_ylabel('sin(x)')
# ax1.grid(True)
#
# # Второй график
# ax2.plot(x, np.cos(x), color='orange')
# ax2.set_title('График Косинуса')
# ax2.set_xlabel('Ось X')
# ax2.set_ylabel('cos(x)')
# ax2.grid(True)
#
# # Автоматическая регулировка отступов, чтобы надписи не наезжали друг на друга
# plt.tight_layout()
# plt.show()

# import matplotlib.pyplot as plt
#
# x = [1, 2, 3, 4, 5]
# y1 = [1, 4, 9, 16, 25]
# y2 = [2, 4, 6, 8, 10]
#
# # Создаем фигуру и сетку из 1 строки и 2 столбцов (axes)
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
#
# # Первый график
# ax1.plot(x, y1, color='green')
# ax1.set_title('График квадратов')
# ax1.set_xlabel('X')
# ax1.set_ylabel('Y1')
# ax1.grid(True)
#
# # Второй график
# ax2.plot(x, y2, color='orange')
# ax2.set_title('Столбчатая диаграмма')
# ax2.set_xlabel('X')
# ax2.set_ylabel('Y2')
# ax2.grid(True)
#
# # Автоматическая компоновка без наложений
# plt.tight_layout()
# plt.show()


# Модуль плохой
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
# МДМ холодный
# 12 В на входе
u_in_12_c = np.array([12]*20)
i_in_12_c = np.array([0.85, 1.29, 1.75, 2.2, 2.65, 3.1, 3.56, 4.03, 4.5, 4.97, 5.46, 5.95, 6.44, 6.95, 7.45, 7.98, 8.5, 9.03, 9.57, 10.13])
# u_out_12_c = np.array([4.99, 4.98, 4.98, 4.97, 4.96, 4.95, 4.94, 4.93, 4.92, 4.91, 4.90, 4.90, 4.89, 4.88, 4.87, 4.86, 4.86, 4.85, 4.84, 4.83])
u_out_12_c = np.array([4.99, 4.9817, 4.9736, 4.9670, 4.9581, 4.9503, 4.9426, 4.9344, 4.9263, 4.9180, 4.9093, 4.9010, 4.8924, 4.8837, 4.8761, 4.8685, 4.8607, 4.8525, 4.8441, 4.8361])
i_out_12_c = np.array([x+1 for x in range(0,20)])

# x_smooth = np.linspace(u_out_12_c.min(), u_out_12_c.max(), 300)
# spl = make_interp_spline(u_out_12_c, i_out_12_c, k=3)  # k=3 — кубический сплайн
# y_smooth = spl(x_smooth)
# y_smooth = np.interp(x_smooth, u_out_12_c, i_out_12_c)

# 27 В на входе
u_in_27_c = [27]*21
i_in_27_c = [0.35, 0.5, 0.75, 0.94, 1.14, 1.33, 1.53, 1.73, 1.93, 2.14, 2.35, 2.56, 2.77, 2.98, 3.2, 3.42, 3.64, 3.86, 4.09, 4.32, 4.55]
u_out_27_c = [4.99, 4.98, 4.97, 4.95, 4.93, 4.92, 4.92, 4.91, 4.91, 4.91, 4,9, 4.9, 4.89, 4.89, 4.88, 4.87, 4.87, 4.86, 4.85, 4.84, 4.83]
i_out_27_c = [x+1 for x in range(-1,20)]

# МДМ теплый, нагрели 10 минут при нагрузке 3 А
# 12 В на входе
u_in_12_h = [12]*20
i_in_12_h = [0.94, 1.38, 1.82, 2.27, 2.73, 3.18, 3.65, 4.11, 4.59, 5.09, 5.58, 6.08, 6.59, 7.1, 7.63, 8.16, 8.71, 9.24, 9.79, 10.36]
u_out_12_h = [4.99, 4.98, 4.98, 4.97, 4.96, 4.95, 4.94, 4.93, 4.92, 4.92, 4.91, 4.9, 4.89, 4.88, 4.88, 4.87, 4.86, 4.85, 4.84, 4,84]
i_out_12_h = [x+1 for x in range(0,20)]

# 27 В на входе
u_in_27_h = [12]*20
i_in_27_h = [0.55, 0.75, 0.95, 1.15, 1.35, 1.54, 1.75, 1.96, 2.17, 2.38, 2.59, 2.8, 3.02, 3.23, 3.45, 3.67, 3.9, 4.13, 4.36, 4.6]
u_out_27_h = [4.99, 4.98, 4.97, 4.95, 4.95, 4.94, 4.94, 4.93, 4.92, 4.91, 4.9, 4.9, 4.9, 4.88, 4.87, 4.86, 4.86, 4.85, 4.84, 4.83]
i_out_27_h = [x+1 for x in range(0,20)]

# 24 В на входе
u_in_24_h = [12]*20
i_in_24_h = [0.59, 0.81, 1.04, 1.26, 1.47, 1.71, 1.93, 2.16, 2.4, 2.64, 2.88, 3.12, 3.37, 3.62, 3.87, 4.13, 4.39, 4.65, 4.92, 5.19]
u_out_24_h = [4.98, 4.98, 4.97, 4.96, 4.95, 4.95, 4.94, 4.93, 4.92, 4.91, 4.90, 4.9, 4.89, 4.88, 4.87, 4.87, 4.86, 4.85, 4.84, 4.83]
i_out_24_h = [x+1 for x in range(0,20)]


# Создаем фигуру и сетку из 1 строки и 2 столбцов (axes)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Первый график
# ax1.plot(u_in_12_c, i_in_12_c, color='green', marker='o', label='Обычная')
ax1.plot(u_in_12_c, i_in_12_c, color='green', label='Обычная')
ax1.set_title('Плохой модуль. Холодный старт. Входная ВАХ, на входе 12 В')
ax1.set_xlabel('U, напряжение')
ax1.set_ylabel('I, ток',rotation=0)
ax1.grid(True)

# Второй график
# ax2.plot(x_smooth, y_smooth, color='orange', label='Плавнaя',linewidth=2)
ax2.plot(u_out_12_c, i_out_12_c, color='orange', label='Плавнaя',linewidth=2)
# ax2.scatter(u_out_12_c,i_out_12_c,color='darkblue', zorder=5, label='Исходные точки')
ax2.set_title('Плохой модуль. Холодный старт. Выходная ВАХ, на входе 12 В')
ax2.set_xlabel('U, напряжение')
ax2.set_ylabel('I, ток', rotation=0)
ax2.grid(True)

# Автоматическая компоновка без наложений
plt.tight_layout()
plt.show()
