# -*- coding: utf-8 -*-
# key =
#ejyUJxMEapWCNIl5blniNjlCVEH5low0ZcSHIa6aIRkXRvlJdNmIVjsEby3qBgl7cPiWIGskI6knx1p0YQ2AVmuFcS25VmJ9RbCxIv6AM4TXc4xjOmT5UC1CN8DlUr3WNIS0wKicTQGIl8jYZXWP5wzVZSUmRhlkc1GjxKv0exWY1ClHbpndRDWLZfXFJ0zPatWp9LuaIZjtozxgLbCmJ4OtYiWh1olRRnmOljyUc23UQGi0OXiwLwQAmyN3Cz7D0EYIzoRRgGdBGnDe0IYKAqiNLrCcJVOwY5WR15lrTRG0FazQdMCHIo6UIHtbCoRY0oLZjMQquBt9CS8M0ILsD4Q6vhdHCO070qY3PSQduZ9QC37J0bLsj3QavsSEIlslIzk3NSvybAX5B0hTbYnlkKiMOQiRIjiyLWCdJWDDdFXIN50LbC2K1blKcDkUlbEmITjWojiGM8j4cY39NlTNIRinLHCnJcE7YqXpRElyS9XnNWzTdpWMVRkrIBjwoTiCMNDZYQvyMmjvgQvnMNj8AhycNuCwIKsCIZkxREhrd7GAVJFCerHtBRpWcDmyVxzmIWj4oKiqMnD5YxvDMtj9g4vKMNjYAuyaNJSBIrscIukdV1tcYjWblcsBQ6WERfkqcom5Vrz0cEy4Ic6FIunuNw2maeXRRTw1bn3Ed0lbcHk7B0nZbMWSFEpcb4Ce5njEbb2a0pi6LdC3J3J5UwEzFkkrZwHgJrlAcC3hM7iOOdiAIU5nNACk4zyZN9Su4gx2NDzeUIuiMyT8YHz2ICn00H=O211cf496cd51bfa7b023ddcd69797e472ac77add1e925ff69d908d2e41bdb5dc9801b7d47bc61dc898b78d115d4bd38f4f2087551c5edfd037341b8a3594e3dffdcf644a0c0032bec12c1d2f2cfd63e5243f8db4dcdb43c98a8cccaf5258b6b2e3fcfaf3819c2498193c780d1c90883b9c061fde3ef03d86e21bc9517ff6660dd0a288ca19580bf17c7a36b9803460d93d178b1bd4e1a8ef5b46391e077fa8e4ab868c9dc14490da163253d4a621676e197bf3aaecc78460ebd912b43c0cf0be6aeee7df1131170dd550c81bcec60e9afe8ec98bb6f4c6dc0bfb7f2e7de4e0386f9d907f120f1ac3f1e197f3353cf09640306de69e5ce3c7511c8bf4ab027af2e69eb96041453ab0b1e3fe52496f680065c0e44b03c04bf049162020452c6c1abd96c2e51a7fef4f91ed589e2a3e327931ec18e815bb1d0d5d0f1f6b4cfe27fd7ce2db847337738748d7ee4926819f8e7c439187a56a05f3eaf8e8e8b9e818169aab3a3e5247c2d71683f5e901e32a3a42fa696e7ff6d0ed5852abb2bc5be0d4273ff6bddff55daeacb16eedd21681496463eebbbd5545cb5b9819a2008aed05f7e0d056e0122ea67f9be922a810c0dbce2d18696f7093724969ef0ad48ca3dcd181e659fdd58dc1c124c538245ba12e6ba36c2cf559edcf116bf0359c55315ac12015c8787d145d6b8c456c4ced78329326733209da9f847093cd048be9062e

#----------------------------------------------------------##
import PySimpleGUI as sg
from debug_1 import main,open_object_p,del_object_p,open_dict_obj
from debug import printf
from tkinter import *
import os
"""
    Demo - Add and "Delete" Rows from a window

    This is cut-down version of the Fed-Ex package tracking demo

    The purpose is to show a technique for making windows that grow by clicking an "Add Row" button
    Each row can be individually "deleted".

    The reason for using the quotes are "deleted" is that the elements are simply hidden.  The effect is the same as deleting them.

    Copyright 2022 PySimpleGUI
"""


def item_row(item_num, grafic_list=[]):
    """
    A "Row" in this case is a Button with an "X", an Input element and a Text element showing the current counter
    :param item_num: The number to use in the tuple for each element
    :type:           int
    :return:         List
    """
    grafic_list.append('График '+ str(item_num+1))
    row =  [sg.pin(sg.Col([[sg.B("X", border_width=1, button_color=(sg.theme_text_color(), sg.theme_background_color()), k=('-DEL-', item_num), tooltip='Delete this item'),
                            sg.In(size=(10,1),k=(str(item_num))),
                            sg.In(size=(20,1)),
                            sg.Combo(grafic_list, default_value=grafic_list[item_num],k=str(item_num)+'graphic')
                            # sg.T( k=('-STATUS-', item_num)),
                            # sg.Checkbox('float', default=True, k=('-FLOAT-',item_num)),
                            # sg.Checkbox('int', default=True, k=('-INT-',item_num)),
                            ]],k=('-ROW-', item_num)))]
    return row



def make_window():
    layout = [  [sg.Text('Необходимы файлы в текущей директории: canmon.log, data_keys.h \n', font='_ 10')],
                [sg.Text('        ID:                 Designation:', font='_ 15', tooltip='Обязательное поле Designation')],
                [sg.pin(sg.Col([item_row(0)], k='-TRACKING SECTION-'))],
                [sg.pin(sg.Text(size=(35,1), font='_ 8', k='-REFRESHED-',))],
                [sg.B("Exit",button_color=(sg.theme_text_color(), sg.theme_background_color()), enable_events=True,
                        k='Exit', tooltip='Выйти из приложения'),
                 sg.B('Ввод',border_width=1,button_color=(sg.theme_text_color(), sg.theme_background_color()),
                         enable_events=True, k='Input',tooltip='Сохранить изменения и ввести аргументы'),
                 sg.B('+',button_color=(sg.theme_text_color(), sg.theme_background_color()), enable_events=True,
                         k='Add Item', tooltip='Добавить элементы'),
                 sg.B('Показать графики', button_color=(sg.theme_text_color(), sg.theme_background_color()), enable_events=True,
                     k='Show', tooltip='Откроет графики параметров')]]

    right_click_menu = [[''], ['Add Item',  'Edit Me', 'Version']]

    window = sg.Window('Parse canwise', layout,  right_click_menu=right_click_menu, use_default_focus=False, font='_ 15', metadata=0)

    return window


def main1():

    window = make_window()
    key_del =[]
    while True:
        event, values = window.read()     # wake every hour
        print(event,'event = ')
        print(values, 'values = ')
        if event == 'Input':
            for i in key_del:
                values.pop(i)
                values.pop(str(i))
            printf(values)
            main(values)
            # printf(values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Add Item':
            window.metadata += 1
            window.extend_layout(window['-TRACKING SECTION-'], rows=[item_row(window.metadata)])
        elif event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Version':
            sg.popup_scrolled(__file__, sg.get_versions(), location=window.current_location(), keep_on_top=True, non_blocking=True)
        elif event[0] == '-DEL-':
            # window.metadata -= 1
            # window[('-ROW-',event[1])].Widget.pack_forget()
            # window.AllKeysDict[('-ROW-',event[1])]
            # window[('-ROW-', event[1])].Widget.master.pack_forget()
            # window[('-ROW-', event[1])].Widget.destroy()
            window[('-ROW-', event[1])].update(visible=False)
            key_del.append(event[1])
            # del_object_p(event[1])
        if event == 'Show':
            # file_path = os.path.realpath(__file__)
            # script_dir = os.path.dirname(file_path)
            # print(file_path, 'file_path1')
            # print(script_dir, 'script_dir1')
            # print(os.path.dirname(os.path.abspath(__file__)),'dirrr')
            # print(os.getcwd(),'getcwd')
            # open_object_p()
            for i in key_del:
                values.pop(i)
                values.pop(str(i))
            open_dict_obj(values)
if __name__ == '__main__':
    main1()
    a = {'0': '51', 0: 'EA_t_COOL','2': '51', 2: 'EA_t_COOL'}
    a = {'0': '51', 0: 'EA_t_COOL','2': '52', 2: 'AIR_TEMP','5': '51', 5: 'EA_P_OIL','6': '51', 6: 'EA_U_A'}
    print(str([*a.keys()][len([*a.keys()])-1]))
    print(len([*a.keys()]))
    # for i in a.values():
    #     print(i)
    print(a)
    b = '111graphic'
    if b.isdigit():
        print(b[:-7])

    graph_list = ['График 1',[31,35,36,32],[41,42,46,48], 'График 2',[51,52,50]]
    # graph_dict = {'График 1':[31,35,36,32],[41,42,46,48]} 'График 2': [51,52,50]}

    for i in graph_list:
        print(i,type(i))

    graph_list.append('График 3',[61,62,63]))
    # graph_list.append([61, 62, 63])
    print(graph_list)
