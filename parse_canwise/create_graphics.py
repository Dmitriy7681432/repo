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

#
# from debug import printf
# import pandas as pd
# from bokeh.plotting import figure, show, output_notebook,output_file
# from datetime import datetime
# import datetime
# output_notebook()
#
# x = pd.date_range('2022-12-01', '2022-12-24', freq='D')
# y = list(range(1,25))
# y = [58.1, 58.5,57.8,60.2,58.5,58.0]
# # x=(datetime(2022,12, 7),datetime(2022,12, 10))
# x=[datetime.time(11,6,41,127),datetime.time(11,6,41,741),datetime.time(11,6,42,127),
#    datetime.time(11,6,42,447),datetime.time(11,6,42,827),datetime.time(11,6,43,227)]
# # x = [1,2,3,4,5,6]
# printf(x)
# printf(y)
# # printf(x_range)
#
#
# p = figure(
#     plot_width=1700,
#     plot_height=700,
#     # x_range=(datetime.time(11,6,41,127),datetime.time(11,6,48,741)),
#     title='Weather      Evolution',
#     x_axis_label='Date',
#     y_axis_label='Precip',


#РИСОВАНИЕ ДАННЫХ С ПОМОЩЬЮ ГЛИФОВ
#Создание первых данных
# from bokeh.io import output_file
# from bokeh.plotting import figure, show
# # Мои данные о координатах x-y
# x = [1, 2, 1]
# y = [1, 1, 2]
# output_file('Рисование_данных_с_помощью_глифов1.html', title='First Glyphs')
# # Создайте фигуру без панели инструментов и диапазонов осей
# fig = figure(title='My Coordinates',
#              plot_height=300, plot_width=300,
#              x_range=(0, 3), y_range=(0, 3),
#              toolbar_location=None)
# # Нарисуйте координаты в виде кругов
# fig.circle(x=x, y=y,
#            color='green', size=10, alpha=0.5)
# # Показать сюжет
# show(fig)






#     x_axis_type='datetime'
# )
# p.line(x,y, legend_label="Evolution", line_width=2)
# output_file('линейный_график.html')how(p)


# import numpy as np
#
# from bokeh.layouts import gridplot
# from bokeh.plotting import figure, show
#
# x = np.linspace(0, 4*np.pi, 100)
# y = np.sin(x)
#
# TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
#
# p1 = figure(title="Legend Example", tools=TOOLS)
#
# p1.scatter(x,   y, legend_label="sin(x)")
# p1.scatter(x, 2*y, legend_label="2*sin(x)", color="orange")
# p1.scatter(x, 3*y, legend_label="3*sin(x)", color="green")
#
# p1.legend.title = 'Markers'
#
# p2 = figure(title="Another Legend Example", tools=TOOLS)
#
# p2.scatter(x, y, legend_label="sin(x)")
# p2.line(x, y, legend_label="sin(x)")
#
# p2.line(x, 2*y, legend_label="2*sin(x)",
#         line_dash=(4, 4), line_color="orange", line_width=2)
#
# p2.scatter(x, 3*y, legend_label="3*sin(x)",
#            marker="square", fill_color=None, line_color="green")
# p2.line(x, 3*y, legend_label="3*sin(x)", line_color="green")
#
# p2.legend.title = 'Lines'
#
# show(gridplot([p1, p2], ncols=2, width=400, height=400))
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import  HoverTool
from datetime import datetime

dateX_str = ['2016-11-14','2016-11-15','2016-11-16']
#conver the string of datetime to python  datetime object
dateX = [datetime.strptime(i, "%Y-%m-%d") for i in dateX_str]

v1= [10,13,5]
v2 = [8,4,14]
v3= [14,9,6]
v = [v1,v2,v3]

names = ['v1','v2','v3']
colors = ['red','blue','yellow']

output_file('example.html',title = 'example of add tooltips to multi_timeseries')
tools_to_show = 'hover,box_zoom,pan,save,resize,reset,wheel_zoom'
p = figure(x_axis_type="datetime", tools=tools_to_show)

#to show the tooltip for multi_lines,you need use the ColumnDataSource which define the data source of glyph
#the key is to use the same column name for each data source of the glyph
#so you don't have to add tooltip for each glyph,the tooltip is added to the figure

#plot each timeseries line glyph
for i in range(3):
    # bokeh can't show datetime object in tooltip properly,so we use string instead
    source = ColumnDataSource(data={
        'dateX': dateX, # python datetime object as X axis
        'v': v[i],
        'dateX_str': dateX_str, #string of datetime for display in tooltip
        'name': [names[i] for n in range(3)]
    })
    p.line('dateX', 'v',source=source,legend=names[i],color = colors[i])
    circle = p.circle('dateX', 'v',source=source, fill_color="white", size=8, legend=names[i],color = colors[i])

    #to avoid some strange behavior(as shown in the picture at the end), only add the circle glyph to the renders of hover tool
    #so tooltip only takes effect on circle glyph
    p.tools[0].renderers.append(circle)

# show the tooltip
hover = p.select(dict(type=HoverTool))
hover.tooltips = [("value", "@v"), ("name", "@name"), ("date", "@dateX_str")]
hover.mode = 'mouse'
show(p)
