# -*- coding: utf-8 -*-

# Модуль плохой
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import LinearLocator,FormatStrFormatter,MultipleLocator
from scipy.interpolate import make_interp_spline
# МДМ холодный
# 12 В на входе
u_in_12_c = np.array([12]*20)
i_in_12_c = np.array([0.85, 1.29, 1.75, 2.2, 2.65, 3.1, 3.56, 4.03, 4.5, 4.97, 5.46, 5.95, 6.44, 6.95, 7.45, 7.98, 8.5, 9.03, 9.57, 10.13])
u_out_12_c = np.array([4.99, 4.9817, 4.9736, 4.9670, 4.9581, 4.9503, 4.9426, 4.9344, 4.9263, 4.9180, 4.9093, 4.9010, 4.8924, 4.8837, 4.8761, 4.8685, 4.8607, 4.8525, 4.8441, 4.8361])
i_out_12_c = np.array([x+1 for x in range(0,20)])
print(i_out_12_c)

# x_smooth = np.linspace(u_out_12_c.min(), u_out_12_c.max(), 300)
# spl = make_interp_spline(u_out_12_c, i_out_12_c, k=3)  # k=3 — кубический сплайн
# y_smooth = spl(x_smooth)
# y_smooth = np.interp(x_smooth, u_out_12_c, i_out_12_c)

# 27 В на входе
u_in_27_c = [27]*20
# i_in_27_c = [0.35, 0.53, 0.75, 0.94, 1.14, 1.33, 1.53, 1.73, 1.93, 2.14, 2.35, 2.56, 2.77, 2.98, 3.2, 3.42, 3.64, 3.86, 4.09, 4.32, 4.55]
i_in_27_c = [0.53, 0.75, 0.94, 1.14, 1.33, 1.53, 1.73, 1.93, 2.14, 2.35, 2.56, 2.77, 2.98, 3.2, 3.42, 3.64, 3.86, 4.09, 4.32, 4.55]
# u_out_27_c = [4.9957, 4.9876, 4.9672, 4.9458, 4.9324, 4.9229, 4.9180, 4.9142, 4.9108, 4.9070, 4.9035, 4.8994, 4.8942, 4.8876, 4.8804, 4.8729, 4.8655, 4.8582, 4.8503, 4.8418, 4.8334]
u_out_27_c = [4.9876, 4.9672, 4.9458, 4.9324, 4.9229, 4.9180, 4.9142, 4.9108, 4.9070, 4.9035, 4.8994, 4.8942, 4.8876, 4.8804, 4.8729, 4.8655, 4.8582, 4.8503, 4.8418, 4.8334]
i_out_27_c = [x+1 for x in range(0,20)]
print(len(i_in_27_c),len(u_out_27_c))

# МДМ теплый, нагрели 10 минут при нагрузке 3 А
# 12 В на входе
u_in_12_h = [12]*20
i_in_12_h = [0.94, 1.38, 1.82, 2.27, 2.73, 3.18, 3.65, 4.11, 4.59, 5.09, 5.58, 6.08, 6.59, 7.1, 7.63, 8.16, 8.71, 9.24, 9.79, 10.36]
u_out_12_h = [4.9895, 4.9817, 4.9755, 4.9665, 4.9588, 4.9508, 4.9425, 4.9340, 4.9255, 4.9177, 4.9095, 4.9010, 4.8927, 4.8845, 4.8761, 4.8679, 4.8597, 4.8514, 4.8430, 4.8345]
i_out_12_h = [x+1 for x in range(0,20)]

# 27 В на входе
u_in_27_h = [27]*20
i_in_27_h = [0.55, 0.75, 0.95, 1.15, 1.35, 1.54, 1.75, 1.96, 2.17, 2.38, 2.59, 2.8, 3.02, 3.23, 3.45, 3.67, 3.9, 4.13, 4.36, 4.6]
u_out_27_h = [4.9846, 4.9769, 4.9640, 4.9498, 4.9450, 4.9425, 4.9366, 4.9293, 4.9213, 4.9134, 4.9054, 4.8965, 4.8880, 4.8795, 4.8714, 4.8632, 4.8550, 4.8468, 4.8384, 4.8301]
i_out_27_h = [x+1 for x in range(0,20)]

# 24 В на входе
u_in_24_h = [24]*20
i_in_24_h = [0.59, 0.81, 1.04, 1.26, 1.47, 1.71, 1.93, 2.16, 2.4, 2.64, 2.88, 3.12, 3.37, 3.62, 3.87, 4.13, 4.39, 4.65, 4.92, 5.19]
u_out_24_h = [4.9827, 4.9751, 4.9700, 4.9564, 4.9513, 4.9450, 4.9355, 4.9274, 4.9192, 4.9111, 4.9031, 4.8945, 4.8868, 4.8785, 4.8704, 4.8621, 4.8539, 4.8457, 4.8374, 4.8292]
i_out_24_h = [x+1 for x in range(0,20)]
#
# def make_plot(x, y, color, title):
#     fig, ax = plt.subplots(figsize=(8, 6))
#     ax.plot(x, y, color=color, linewidth=2, marker='o')
#     ax.set_title(title)
#     ax.set_xlabel('U, напряжение')
#     ax.set_ylabel('I, ток', rotation=0)
#     ax.yaxis.set_major_locator(LinearLocator(16))
#     ax.xaxis.set_major_locator(LinearLocator(12))
#     ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#     ax.grid(True, axis='both')
#     plt.tight_layout()
#     return fig
#
# make_plot(u_in_12_c,  i_in_12_c,  'green',  'Модуль не нагретый. Входная ВАХ, 12 В')
# make_plot(u_out_12_c, i_out_12_c, 'orange', 'Модуль не нагретый. Выходная ВАХ, 12 В')
# make_plot(u_in_27_c,  i_in_27_c,  'blue',   'Модуль не нагретый. Входная ВАХ, 27 В')
# make_plot(u_out_27_c, i_out_27_c, 'red',    'Модуль не нагретый. Выходная ВАХ, 27 В')
# make_plot(u_in_12_h,  i_in_12_h,  'green',  'Модуль нагретый. Входная ВАХ, 12 В')
# make_plot(u_out_12_h, i_out_12_h, 'orange', 'Модуль нагретый. Выходная ВАХ, 12 В')
# make_plot(u_in_27_h,  i_in_27_h,  'blue',   'Модуль нагретый. Входная ВАХ, 27 В')
# make_plot(u_out_27_h, i_out_27_h, 'red',    'Модуль нагретый. Выходная ВАХ, 27 В')
# make_plot(u_in_24_h,  i_in_24_h,  'blue',   'Модуль нагретый. Входная ВАХ, 24 В')
# make_plot(u_out_24_h, i_out_24_h, 'red',    'Модуль нагретый. Выходная ВАХ, 24 В')
# plt.show()

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
#
# # Входные ВАХ — все напряжения на одном графике
# for x, y, color, marker, label in [
#     (u_in_12_c, i_in_12_c, 'green',  'o', '12 В'),
#     (u_in_27_c, i_in_27_c, 'blue',   's', '27 В'),
#     # (u_in_48_c, i_in_48_c, 'purple', '^', '48 В'),
# ]:
#     ax1.plot(x, y, color=color, linewidth=2, marker=marker, label=label, markersize=3)
#
# # Выходные ВАХ
# for x, y, color, marker, label in [
#     (u_out_12_c, i_out_12_c, 'orange', 'o', '12 В'),
#     (u_out_27_c, i_out_27_c, 'red',    's', '27 В'),
#     # (u_out_48_c, i_out_48_c, 'brown',  '^', '48 В'),
# ]:
#     ax2.plot(x, y, color=color, linewidth=2, marker=marker, label=label,markersize=3)
#
# ax1.set_title('Входная ВАХ')
# ax1.set_xlabel('U, напряжение')
# ax1.set_ylabel('I, ток', rotation=0)
# ax1.legend()
#
# ax2.set_title('Выходная ВАХ')
# ax2.set_xlabel('U, напряжение')
# ax2.set_ylabel('I, ток', rotation=0)
# ax2.legend()
#
# for ax in (ax1, ax2):
#     ax.yaxis.set_major_locator(LinearLocator(16))
#     ax.xaxis.set_major_locator(LinearLocator(12))
#     # ax.xaxis.set_major_formatter(fmt)
#     ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#     ax.grid(True, axis='both')
#
# plt.tight_layout()
# plt.show()

# import matplotlib.pyplot as plt
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
#
# fig, axes = plt.subplots(2, 2, figsize=(10, 7))
# axes = axes.flatten()
#
# N_Y = 16
# N_X = 12
# fmt = FormatStrFormatter('%.2f')
#
# # Каждый элемент: (заголовок, [(x, y, color, marker, label), ...])
# plots = [
#     (
#         'Входная ВАХ',
#         [
#             (u_in_12_c, i_in_12_c, 'green', 'o', '12 В'),
#             (u_in_27_c, i_in_27_c, 'blue', 's', '27 В'),
#         ]
#     ),
#     (
#         'Выходная ВАХ',
#         [
#             (u_out_12_c, i_out_12_c, 'orange', 'o', '12 В'),
#             (u_out_27_c, i_out_27_c, 'red', 's', '27 В'),
#         ]
#     ),
#     (
#         'Входная ВАХ (вариант 2)',  # замените на свои данные
#         [
#             (u_in_12_h, i_in_12_h, 'green', '^', '12 В'),
#             (u_in_24_h ,i_in_24_h, 'red', 'D', '24 В'),
#             (u_in_27_h ,i_in_27_h, 'blue', 'D', '27 В'),
#         ]
#     ),
#     (
#         'Выходная ВАХ (вариант 2)',  # замените на свои данные
#         [
#             (u_out_12_h, i_out_12_h, 'orange', '^', '12 В'),
#             (u_out_24_h, i_out_24_h, 'brown', 'D', '24 В'),
#             (u_out_27_h, i_out_27_h, 'red', 'D', '27 В'),
#         ]
#     ),
# ]
#
# for ax, (title, lines) in zip(axes, plots):
#     for x, y, color, marker, label in lines:
#         ax.plot(x, y, color=color, linewidth=2, marker=marker, label=label,markersize=3)
#
#     ax.set_title(title)
#     ax.set_xlabel('U, напряжение')
#     ax.set_ylabel('I, ток', rotation=0)
#     ax.legend()
#     ax.yaxis.set_major_locator(LinearLocator(N_Y))
#     ax.xaxis.set_major_locator(LinearLocator(N_X))
#     ax.xaxis.set_major_formatter(fmt)
#     ax.grid(True, axis='both')
#
# plt.tight_layout()
# plt.show()


# import matplotlib.pyplot as plt
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
#
# N_Y = 16
# N_X = 12
# fmt = FormatStrFormatter('%.2f')
#
# # ==========================================
# # ФИГУРА 1: Входные ВАХ (12 В и 27 В)
# # ==========================================
# fig1, ax1 = plt.subplots(figsize=(10, 6))
# fig1.canvas.manager.set_window_title('Входная ВАХ')
#
# ax1.plot(u_in_12_c, i_in_12_c, color='green', linewidth=1.5, marker='o', markersize=3, label='12 В')
# ax1.plot(u_in_27_c, i_in_27_c, color='blue',  linewidth=1.5, marker='s', markersize=3, label='27 В')
#
# ax1.set_title('Плохой модуль. Холодный старт. Входная ВАХ')
# ax1.set_xlabel('U, напряжение')
# ax1.set_ylabel('I, ток', rotation=0)
# ax1.legend()
# ax1.yaxis.set_major_locator(LinearLocator(N_Y))
# ax1.xaxis.set_major_locator(LinearLocator(N_X))
# ax1.xaxis.set_major_formatter(fmt)
# ax1.grid(True, axis='both')
# fig1.tight_layout()
#
# # ==========================================
# # ФИГУРА 2: Выходные ВАХ (12 В и 27 В)
# # ==========================================
# fig2, ax2 = plt.subplots(figsize=(10, 6))
# fig2.canvas.manager.set_window_title('Выходная ВАХ')
#
# ax2.plot(u_out_12_c, i_out_12_c, color='orange', linewidth=1.5, marker='o', markersize=3, label='12 В')
# ax2.plot(u_out_27_c, i_out_27_c, color='red',    linewidth=1.5, marker='s', markersize=3, label='27 В')
#
# ax2.set_title('Плохой модуль. Холодный старт. Выходная ВАХ')
# ax2.set_xlabel('U, напряжение')
# ax2.set_ylabel('I, ток', rotation=0)
# ax2.legend()
# ax2.yaxis.set_major_locator(LinearLocator(N_Y))
# ax2.xaxis.set_major_locator(LinearLocator(N_X))
# ax2.xaxis.set_major_formatter(fmt)
# ax2.grid(True, axis='both')
# fig2.tight_layout()
#
# # Показываем оба окна одновременно
# plt.show()


import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter


def plot_many_figures(figures_config, step_X = None, step_Y =None,
                      N_Y=16, N_X=12, nmb_divis=2,
                      markersize=3, linewidth=1.5,
                      xlabel='U, напряжение, В', ylabel='I, ток, А',
                      show=True):
    fmt = FormatStrFormatter(f'%.{nmb_divis}f')
    created_figs = []

    for cfg in figures_config:
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.canvas.manager.set_window_title(cfg['title'])

        for x, y, color, marker, label in cfg['lines']:
            ax.plot(x, y, color=color, linewidth=linewidth,
                    marker=marker, markersize=markersize, label=label)

        ax.set_title(cfg['title'])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel, rotation=90)
        ax.legend()
        if step_X is not None:
            ax.xaxis.set_major_locator(MultipleLocator(step_X))
        else:
            ax.xaxis.set_major_locator(LinearLocator(N_X))
        if step_Y is not None:
            ax.yaxis.set_major_locator(MultipleLocator(step_Y))
        else:
            ax.yaxis.set_major_locator(LinearLocator(N_Y))
        ax.xaxis.set_major_formatter(fmt)
        ax.grid(True, axis='both')
        fig.tight_layout()

        created_figs.append(fig)

    if show:
        plt.show()

    return created_figs



figures = [
    {
        'title': 'Модуль холодный. Входная ВАХ, 12 В / 27 В',
        'lines': [
            (u_in_12_c,  i_in_12_c,  'green',  'o', '12 В'),
            (u_in_27_c,  i_in_27_c,  'blue',   's', '27 В'),
        ]
    },
    {
        'title': 'Модуль холодный. Выходная ВАХ, 12 В / 27 В',
        'lines': [
            (u_out_12_c, i_out_12_c, 'orange', 'o', '12 В'),
            (u_out_27_c, i_out_27_c, 'red',    's', '27 В'),
        ]
    },
    {
        'title': 'Модуль разогретый. Входная ВАХ, 12 В / 24 В / 27 В',
        'lines': [
            (u_in_12_h,  i_in_12_h,  'green',  'o', '12 В'),
            (u_in_24_h,  i_in_24_h,  'red',   's', '27 В'),
            (u_in_27_h, i_in_27_h, 'blue', 's', '27 В'),
        ]
    },
    {
        'title': 'Модуль разогретый. Выходная ВАХ, 12 В / 24 В / 27 В',
        'lines': [
            (u_out_12_h, i_out_12_h, 'orange', 'o', '12 В'),
            (u_out_24_h, i_out_24_h, 'brown',  's', '24 В'),
            (u_out_27_h, i_out_27_h, 'red', 's', '27 В'),

        ]
    },
]

figs = plot_many_figures(figures,step_Y=1)

# Подсчет КПД
n_12_c = []
n_27_c = []
n_12_h = []
n_24_h = []
n_27_h = []
for i in range(0,20):
    n_12_c.append((i_out_12_c[i] * u_out_12_c[i] / (i_in_12_c[i] * u_in_12_c[i]))*100)
    n_27_c.append((i_out_27_c[i] * u_out_27_c[i] / (i_in_27_c[i] * u_in_27_c[i]))*100)
    n_12_h.append((i_out_12_h[i] * u_out_12_h[i] / (i_in_12_h[i] * u_in_12_h[i])) * 100)
    n_24_h.append((i_out_24_h[i] * u_out_24_h[i] / (i_in_24_h[i] * u_in_24_h[i])) * 100)
    n_27_h.append((i_out_27_h[i] * u_out_27_h[i] / (i_in_27_h[i] * u_in_27_h[i])) * 100)

figures = [

    {
        'title': 'Модуль не нагретый. КПД, входное 12 В / 27 В',
        'lines': [
            (i_out_12_c, n_12_c, 'orange', 'o', '12 В'),
            (i_out_27_c, n_27_c, 'red', 'o', '27 В'),

        ]
    },
    {
        'title': 'Модуль разогретый. КПД, входное 12 В / 24 В / 27 В',
        'lines': [
            (i_out_12_h, n_12_h, 'orange', 'o', '12 В'),
            (i_out_24_h, n_24_h, 'red', 'o', '24 В'),
            (i_out_27_h, n_27_h, 'brown', 'o', '27 В'),

        ]
    },

]

figs = plot_many_figures(figures, step_X= 1, step_Y=5,ylabel= "n, КПД, %",xlabel= 'I, ток, А', nmb_divis=0)
