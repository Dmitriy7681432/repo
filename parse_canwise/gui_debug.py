# -*- coding: utf-8 -*-
# import PySimpleGUI as sg
#
# def new_data(index=0,):
#     headings = [f"{index} Column {col}" for col in range(cols)]
#     data = [[f"{index} Data {row}/{col}" for col in range(cols)] for row in range(rows)]
#     return headings, data
#
# rows, cols, index = 10, 5, 0
# headings, data = new_data(index)
#
# col_layout = [
#     [sg.Table(data, headings=headings, num_rows=10, justification='c', key='-TABLE-')],
# ]
# layout = [
#     [sg.Column(col_layout, key='-COLUMN-')],
#     [sg.Push(), sg.Button("Update"), sg.Push()],
# ]
# window = sg.Window('Demo', layout)
#
# while True:
#
#     event, values = window.read()
#
#     if event == sg.WIN_CLOSED:
#         break
#     elif event == "Update":
#         index += 1
#         headings, data = new_data(index)
#         window['-TABLE-'].table_frame.master.destroy()
#         del window.AllKeysDict['-TABLE-']
#         window.extend_layout(window['-COLUMN-'], [[sg.Table(data, headings=headings, num_rows=10, justification='c', key='-TABLE-')]])
#
# window.close()

#------------------Sub window----------------------------#
# import PySimpleGUI as sg
#
#
# def main_window():
#     # Create main window
#     layout = [
#         [sg.T('This is a quasi-modal design pattern for multiple windows')],
#         [sg.T('Text input:'), sg.In('', key='text_in')],
#         [sg.T('DropDown input:'), sg.DropDown(values=['val1', 'val2', 'val3'])],
#         [sg.T('Some text:'), sg.T('Nothing yet', key='lbl')],
#         [sg.Button('Change text', key='launch_sub'), sg.Button('Exit', key='Exit')]
#     ]
#
#     window = sg.Window('Main window', size=(400, 400)).Layout(layout)
#     window.Finalize()
#     window.BringToFront()
#     while True:
#         event, values = window.Read()
#         if event in [None, 'Exit']:  # always,  always give a way out!
#             window.Close()
#             break
#         elif event is 'launch_sub':
#             # call sub_window
#             sub_window(window)
#
#
# def sub_window(parent_window):
#     # Disable parent elements
#     parent_keys = list(parent_window.AllKeysDict.keys())
#
#     print('parent_window.AllKeysDict:', parent_keys)
#     print('parent_window.ReturnValuesDictionary:', list(parent_window.ReturnValuesDictionary.keys()))
#     for k in parent_keys:
#         try:
#             parent_window.FindElement(k).Update(disabled=True)
#         except:
#             pass
#     parent_window.FindElement(0).Update(disabled=True)  # <---The element 0 can't be found
#
#     # Create new window
#     layout = [
#         [sg.T('This is a Sub-Window')],
#         [sg.T('Input something new:'), sg.In('', key='text_in')],
#         [sg.Ok(key='Ok'), sg.Cancel(key='Cancel')]
#     ]
#     window = sg.Window('Sub window', keep_on_top=True).Layout(layout)
#     window.Finalize()
#     window.BringToFront()
#     while True:
#         event, values = window.Read()
#         if event in [None, 'Cancel']:
#             break
#         elif event is 'Ok':
#             parent_window.FindElement('lbl').Update(values['text_in'])
#             break
#
#     # Close this window and enable parent elements
#     window.Close()
#     for k in parent_keys:
#         try:
#             parent_window.FindElement(k).Update(disabled=False, )
#         except:
#             pass
#     try:
#         parent_window.BringToFront()
#     except:
#         pass
#
#
# main_window()


# import PySimpleGUI as sg
#
# """
#     Demo - "Pinning" an element into a location in a layout
#
#
#     Copyright 2020, 2022, 2023 PySimpleGUI
# """
#
# layout = [[sg.Text('Hide Button or Multiline. Buttons 1 & 2 hide Button 2')],
#           [sg.pin(sg.Multiline(size=(60, 10)))],
#           [sg.pin(sg.Button('Button1')), sg.pin(sg.Button('Button2'), shrink=False), sg.B('Toggle Multiline')],
#           ]
#
# window = sg.Window('Visible / Invisible Element Demo', layout)
#
# toggle = toggle_in = False
# while True:  # Event Loop
#     event, values = window.read()
#     print(event, values)
#     if event == sg.WIN_CLOSED or event == 'Exit':
#         break
#
#     if event in ('Button1', 'Button2'):
#         window['Button2'].update(visible=toggle)
#         toggle = not toggle
#     elif event == 'Toggle Multiline':
#         window['-MLINE-'].update(visible=not window['-MLINE-'].visible)
# window.close()


import psutil
import PySimpleGUI as sg
from debug import printf

def configure_canvas(event, canvas, frame_id):
    canvas.itemconfig(frame_id, width=canvas.winfo_width())

def configure_frame(event, canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def delete_widget(widget):
    children = list(widget.children.values())
    for child in children:
        delete_widget(child)
    widget.pack_forget()
    widget.destroy()

def delete_element(element, window):
    if element.Key in window.AllKeysDict:
        del window.AllKeysDict[element.Key]
    rows = getattr(element, 'Rows', None)
    if rows is not None:
        for row in rows:
            for row_element in row:
                delete_element(row_element, window)

def new_rows():
    global index
    index += 1
    layout_frame = [[sg.Text("Hello World"), sg.Push(), sg.Button('Delete', key=('Delete', index))]]
    return [[sg.Frame(f"Frame {index:0>2d}", layout_frame, expand_x=True, key=('Frame', index))]]

index = 0

layout = [
    [sg.Button("Add")],
    [sg.Column(new_rows(), scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, key='Scrollable Column')]
]

window = sg.Window("Title", layout, resizable=True, margins=(0, 0), finalize=True)

frame_id = window['Scrollable Column'].Widget.frame_id
frame = window['Scrollable Column'].Widget.TKFrame
canvas = window['Scrollable Column'].Widget.canvas
canvas.bind("<Configure>", lambda event, canvas=canvas, frame_id=frame_id:configure_canvas(event, canvas, frame_id))
frame.bind("<Configure>", lambda event, canvas=canvas:configure_frame(event, canvas))

window.maximize()
rss, vms, total = 0, 0, 0
while True:

    event, values = window.read(timeout=500)
    printf(event,values)

    if event in ('Close', sg.WIN_CLOSED):
        break
    elif event == 'Add':
        e = 'ADD'
        window.extend_layout(window['Scrollable Column'], rows=new_rows())
    elif event[0] == 'Delete':
        e = 'DEL'
        i = event[1]
        element = window[('Frame', i)]
        widget = element.Widget
        delete_element(element, window)
        delete_widget(widget.master)
        printf(element)
        printf(widget)
        del widget
        del element
        printf(values)
    elif event == sg.TIMEOUT_KEY:
        e = 'TMT'

    p = psutil.Process().memory_info()
    if (rss, vms, total) != (p.rss, p.vms, p.rss+p.vms):
        rss, vms, total = p.rss, p.vms, p.rss+p.vms
        print(f'{e}> Mem Usage:{rss}, VM Size:{vms}, Total:{rss+p.vms}')

window.close()
