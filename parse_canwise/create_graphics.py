# -*- coding: utf-8 -*-
# from bokeh.plotting import figure, output_file, show
# from bokeh.models import ColumnDataSource
#
# # Создание графической фигуры
# p = figure(title='Пример линейного графика', x_axis_label='X-ось', y_axis_label='Y-ось')
#
# # Данные для графика
# x = [1, 2, 3, 4, 15]
# y = [6, 7, 2, 4, 5]
#
# y = [58.1, 58.5,57.8,60.2,58.5,58.0]
# x = [711,715,743,855,877,914]
# # Добавление линии на график
# p.line(x, y, legend_label='Линия', line_width=2)
#
# # Отображение графика
# output_file('линейный_график.html')
# show(p)

from debug import printf
import pandas as pd
from bokeh.plotting import figure, show, output_notebook,output_file
from datetime import datetime
import datetime
output_notebook()

x = pd.date_range('2022-12-01', '2022-12-24', freq='D')
y = list(range(1,25))
y = [58.1, 58.5,57.8,60.2,58.5,58.0]
# x=(datetime(2022,12, 7),datetime(2022,12, 10))
x=[datetime.time(11,6,41,127),datetime.time(11,6,41,741),datetime.time(11,6,42,127),
   datetime.time(11,6,42,447),datetime.time(11,6,42,827),datetime.time(11,6,43,227)]
# x = [1,2,3,4,5,6]
printf(x)
printf(y)
# printf(x_range)


p = figure(
    plot_width=1700,
    plot_height=700,
    # x_range=(datetime.time(11,6,41,127),datetime.time(11,6,48,741)),
    title='Weather      Evolution',
    x_axis_label='Date',
    y_axis_label='Precip',
    x_axis_type='datetime'
)
p.line(x,y, legend_label="Evolution", line_width=2)
output_file('линейный_график.html')
show(p)