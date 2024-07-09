# -*- coding: utf-8 -*-
import struct,re
# from debug import printf
from bokeh.plotting import figure, output_file, show, save
from bokeh.models import ColumnDataSource
import datetime
import argparse,sys
import webbrowser,os

object_p = []
object_p1 = []

def del_object_p(arg):
    object_p.pop(arg)

def open_object_p():
    # file_path = os.path.realpath(__file__)
    # script_dir = os.path.dirname(file_path)
    script_dir =os.getcwd()
    # print(script_dir, 'script_dir')
    # print(object_p)
    # print(object_p1)
    for i,j in zip(object_p,object_p2):
        webbrowser.open(f'{script_dir}/log/{i}_{j}_graphic.html')
    # webbrowser.open(f'{script_dir}/log/EA_t_COOL_ALL_graphic.html')


def func_id_to_hex(arg):
    c = ''
    # f = open('D://repo/parse_canwise/data_keys.h',encoding='utf-8')
    f = open('data_keys.h',encoding='utf-8')
    for i in f:
        if "KEY_"+arg+" " in i:
            for j in i[::-1]:
                if j ==")": continue
                if j == "(": break
                c = c+j
    c = hex(int(c[::-1])).upper()[2:]

    if len(c) == 2: c = c + "  00  00  00"
    elif len(c) == 4: c = c[len(c) - 2:] + "  " + \
         c[len(c) - 4:len(c) - 2] + "  00  00"
    elif len(c) == 6: c = c[len(c) - 2:] + "  " + \
         c[len(c) - 4:len(c) - 2] + "  " + c[len(c) - 6:len(c) - 4] + "  00"
    elif len(c) == 8: c = c[len(c) - 2:] + "  " + \
         c[len(c) - 4:len(c) - 2] + "  " + c[len(c) - 6:len(c) - 4] + "  " + c[len(c) - 8:len(c) - 6]

    f.close()
    return c



def main (arg):
    #Для командной строки
    parser = argparse.ArgumentParser(description='Приветствую тебя')
    parser.add_argument('name', nargs="*", help='designation')
    args = parser.parse_args()


    # for ii in args.name:
    for ii in arg.values():
        if not ('_' in ii or ii.isalnum()):id = 'ALL';id_dec = 'ALL';continue
        if ii.isdigit(): id_dec = ii; id =str('000000' + hex(int(ii))[2:]); continue

        f = open('canmon.log')
        filename_log =f'log/{ii}_{id_dec}_log.txt'
        dir_name = os.path.dirname(filename_log)
        os.makedirs(dir_name,exist_ok=True)
        f1 = open(filename_log,'w+')

        bbb = '0'
        y= []
        x= []
        date = []

        hex_can = func_id_to_hex(ii)

        for i in f:
            # if 'A5  13' in i:
            # if '4F  2F' in i:
            if hex_can in i and id in i:
                bb = i[60:62] +i[56:58] +i[52:54] +i[48:50] + i[44:46] +i[40:42]
                for j in bb:
                    if len(bbb)<9:
                        bbb =bbb+j
                a =struct.unpack('!f', bytes.fromhex(bbb[1:]))[0]
                y.append(a)
                x.append(datetime.time(int(i[85:87]),int(i[88:90]),int(i[91:93]),int(i[94:98])))
                date.append(i[85:98])
                bbb = '0'
                log_param_file = i[:98] + "  " + str(a) + '\n'
                f1.write(log_param_file)
            elif hex_can in i and id =="ALL":
                bb = i[60:62] + i[56:58] + i[52:54] + i[48:50] + i[44:46] + i[40:42]
                for j in bb:
                    if len(bbb) < 9:
                        bbb = bbb + j
                a = struct.unpack('!f', bytes.fromhex(bbb[1:]))[0]
                y.append(a)
                x.append(datetime.time(int(i[85:87]), int(i[88:90]), int(i[91:93]), int(i[94:98])))
                date.append(i[85:98])
                bbb = '0'
                log_param_file = i[:98] + "  " + str(a) + '\n'
                f1.write(log_param_file)
        f.close()
        f1.close()

        #Перевод из designation в hex_can
        TOOLS = "pan,wheel_zoom,box_zoom,hover,tap,reset,save"

        source = ColumnDataSource(data=dict(
            x=x,
            y=y,
            date =date
        ))
        TOOLTIPS = [
            ("index", "$index"),
            ("(x,y)", "($x, $y)"),
            ("date", "@date"),
        ]
        p = figure(
            plot_width=1700,
            plot_height=700,
            tooltips =TOOLTIPS,
            # x_range=(datetime.time(11,6,41,127),datetime.time(11,6,48,741)),
            title='Weather      Evolution',
            x_axis_label=ii+'  ' + 'ID = '+ id_dec,
            y_axis_label='Precip',
            x_axis_type='datetime',
            tools=TOOLS,
        )
        p.line(x,y, legend_label="Evolution", line_width=2)
        p.circle('x','y',width =3,source=source)
        output_file(f'log/{ii}_{id_dec}_graphic.html')
        # webbrowser.open(f'{ii}_graphic.html')
        object_p.append(ii)
        object_p1.append(id_dec)
        save(p)
        # show(p1)



if __name__ == "__main__":
    main()

# # Создание графической фигуры
# p = figure(title='Пример линейного графика', x_axis_label='X-ось', y_axis_label='Y-ось',width=1600,height=900)
# # Добавление линии на график
# p.line(list_par_x, list_par_y, legend_label='Линия', line_width=2)
#
# # Отображение графика
# output_file('линейный_график.html')
# show(p)

# custom_datetime = datetime.datetime(2020, 1, 1, 11, 6, 41)
# print(custom_datetime)
# # from datetime import datetime
# # x_range=(datetime.time(11,6,41,741),datetime(2022,12, 10,12,8,42))
# x_range = datetime.time(11,6,41,421)
# print(x_range)
# f = open('D://repo/parse_canwise/canmon.log')
# # f1 = open('D://repo/parse_canwise/data_keys.h',encoding='utf-8')
# f2 = open('D://repo/parse_canwise/log.txt', 'w')
#
# for i in f:
#     # printf()
#     if '00000033' in i:
#         # printf()
#         a = i[36:38]+i[32:34]
#         a = "("+str(int(a,16))+")"
#         nmb = i[3:11]
#         f1 = open('D://data_keys.h', encoding='utf-8')
#         for j in f1:
#             # printf()
#             if a in j:
#                 # print(a,' - ',j)
#                 b = nmb + ' - ' +a+ ' - ' +j
#                 f2.writelines(b)
#         # print(a)
#
# f.close()
# f1.close()
# f2.close()


# a = struct.unpack('!x', bytes.fromhex('42'))
# b = struct.unpack('!f', bytes.fromhex('4268B90E'))[0]
# c = int('4268B90E',16)
# d = struct.pack("@3s",b'123')
# print(a)
# print(b)
# print(c)
# print(d)


# b = "RX 0002155 SFF 00000033 8 HEX   A5  13  00  07  0E  B9  68  42 0047915140 18.06.2024 11:06:15.411 0031113583 2307728432"
# if 'A5  13' in b:
#     print("YES")
# print(b[85:87])
# print(b[88:90])
# print(b[91:93])
# print(b[94:98])

# bbb = '0'
# bb = i[60:62] + i[56:58] + i[52:54] + i[48:50] + i[44:46] + i[40:42]
# for i in bb:
#     if len(bbb)<9:
#         bbb =bbb+i
# print(bbb[1:])