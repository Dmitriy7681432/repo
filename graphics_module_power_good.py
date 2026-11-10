# -*- coding: utf-8 -*-

# Модуль плохой
import numpy as np
from matplotlib.ticker import MultipleLocator
# МДМ холодный
# 12 В на входе
u_in_12_c = np.array([12]*20)
i_in_12_c = np.array([0.69,     1.12,   1.55,   1.99,   2.43,   2.88,   3.33,   3.78,   4.24,   4.71,   5.18,   5.66,   6.14,   6.63,   7.12,   7.62,   8.13,    8.65,   9.17,   9.7])
u_out_12_c = np.array([5.0040, 4.9940, 4.9841, 4.9755, 4.9673, 4.9533, 4.9507, 4.9418, 4.9329, 4.9240, 4.9152, 4.9064, 4.8975, 4.8885, 4.8799, 4.8704, 4.8609, 4.8514, 4.8421, 4.8331])
i_out_12_c = np.array([x+1 for x in range(0,20)])
print(i_out_12_c)

# 27 В на входе
u_in_27_c = [27]*20
# i_in_27_c = [0.35, 0.53, 0.75, 0.94, 1.14, 1.33, 1.53, 1.73, 1.93, 2.14, 2.35, 2.56, 2.77, 2.98, 3.2, 3.42, 3.64, 3.86, 4.09, 4.32, 4.55]
# u_out_27_c = [4.9957, 4.9876, 4.9672, 4.9458, 4.9324, 4.9229, 4.9180, 4.9142, 4.9108, 4.9070, 4.9035, 4.8994, 4.8942, 4.8876, 4.8804, 4.8729, 4.8655, 4.8582, 4.8503, 4.8418, 4.8334]
i_in_27_c = [0.37,     0.56,   0.75,   0.95,   1.15,   1.35,    1.55, 1.75,     1.95, 2.16,     2.36, 2.57,     2.78, 2.99,    3.20,   3.42,   3.63,   3.85,   4.07,   4.30]
u_out_27_c = [5.0005, 4.9919, 4.9833, 4.9747, 4.9661, 4.9574, 4.9488, 4.9401, 4.9315, 4.9227, 4.9141, 4.9054, 4.8968, 4.8880, 4.8794, 4.8706, 4.8619, 4.8532, 4.8443, 4.8355]
i_out_27_c = [x+1 for x in range(0,20)]
print(len(i_in_27_c),len(u_out_27_c))

# МДМ теплый, нагрели 10 минут при нагрузке 3 А
# 12 В на входе
u_in_12_h = [12]*20
i_in_12_h = [0.68,     1.11,   1.54,   1.98,   2.43,   2.88,   3.34,   3.80,   4.27,   4.74,   5.22,   5.70,   6.19,   6.68,    7.18,  7.70,   8.22,   8.74,   9.28,   9.82]
u_out_12_h = [5.0038, 4.9931, 4.9822, 4.9735, 4.9660, 4.9585, 4.9500, 4.9411, 4.9321, 4.9232, 4.9142, 4.9052, 4.8962, 4.8871, 4.8776, 4.8679, 4.8585, 4.8493, 4.8402, 4.8314]
i_out_12_h = [x+1 for x in range(0,20)]

# 27 В на входе
u_in_27_h = [27]*20
i_in_27_h = [0.36,     0.55,   0.75,   0.95,   1.15,   1.35,   1.55,   1.75,   1.95,   2.16,   2.37,   2.57,   2.78,   3.00,   3.21,   3.43,   3.65,   3.87,   4.10,   4.32]
u_out_27_h = [4.9997, 4.9910, 4.9823, 4.9736, 4.9650, 4.9563, 4.9476, 4.9390, 4.9302, 4.9215, 4.9128, 4.9041, 4.8954, 4.8866, 4.8779, 4.8692, 4.8603, 4.8515, 4.8425, 4.8335]
i_out_27_h = [x+1 for x in range(0,20)]

# 24 В на входе
u_in_24_h = [24]*20
i_in_24_h = [0.39,     0.60,   0.82,   1.04,   1.26,   1.49,   1.72,   1.94,   2.17,   2.41,   2.64,   2.88,   3.12,   3.36,   3.60,   3.85,   4.10,   4.35,   4.60,   4.86]
u_out_24_h = [4.9997, 4.9910, 4.9822, 4.9735, 4.9648, 4.9561, 4.9474, 4.9387, 4.9300, 4.9213, 4.9125, 4.9036, 4.8949, 4.8860, 4.8773, 4.8684, 4.8596, 4.8508, 4.8418, 4.8327]
i_out_24_h = [x+1 for x in range(0,20)]


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
        'title': 'Модуль не нагретый. Входная ВАХ, 12 В / 27 В',
        'lines': [
            (u_in_12_c,  i_in_12_c,  'green',  'o', '12 В'),
            (u_in_27_c,  i_in_27_c,  'blue',   's', '27 В'),
        ]
    },
    {
        'title': 'Модуль не нагретый. Выходная ВАХ, 12 В / 27 В',
        'lines': [
            (u_out_12_c, i_out_12_c, 'orange', 'o', '12 В'),
            (u_out_27_c, i_out_27_c, 'red',    's', '27 В'),
        ]
    },
    {
        'title': 'Модуль нагретый. Входная ВАХ, 12 В / 24 В / 27 В',
        'lines': [
            (u_in_12_h,  i_in_12_h,  'green',  'o', '12 В'),
            (u_in_24_h,  i_in_24_h,  'red',   's', '27 В'),
            (u_in_27_h, i_in_27_h, 'blue', 's', '27 В'),
        ]
    },
    {
        'title': 'Модуль нагретый. Выходная ВАХ, 12 В / 24 В / 27 В',
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
        'title': 'Модуль нагретый. КПД, входное 12 В / 24 В / 27 В',
        'lines': [
            (i_out_12_h, n_12_h, 'orange', 'o', '12 В'),
            (i_out_24_h, n_24_h, 'red', 'o', '24 В'),
            (i_out_27_h, n_27_h, 'brown', 'o', '27 В'),

        ]
    },

]

figs = plot_many_figures(figures, step_X= 1, step_Y=5,ylabel= "n, КПД, %",xlabel= 'I, ток, А', nmb_divis=0)
