import asyncio,time,serial
from PyQt5 import QtCore, QtWidgets
from debug import printf

class Connect(object):
    # ser = serial.Serial(port='COM16', baudrate=3000000, timeout=0.1)
    ser = serial.Serial()

    # def __init__(self):
    # Поиск устройства
    # ports = serial.tools.list_ports.comports()
    # for port in ports:
    #     print(port.device)
    #     port = port.device
    # self.ser = serial.Serial(port =port,baudrate=3000000,timeout=0.1)
    # self.ser = serial.Serial(port='COM88', baudrate=3000000, timeout=0.1)

    # Выбор режима com_port
    def can_open_O(self, arg):
        printf('can_open')
        arg.timeot = 0.1
        msg = b"C\r"
        arg.write(msg)
        msg = b"S5\rZ1\r"
        arg.write(msg)
        msg = b"O\r"
        arg.write(msg)

    # Закрытие com_port
    def can_close(self, arg):
        printf('can_close')
        msg = b"C\r"
        arg.write(msg)
        # После закрытия необходимо заново инициалировать serial
        # arg.close()

class Testing(Connect):

    def __init__(self, ser, product, control_block):
        self.ser = ser
        self.product = product
        self.control_block = control_block

    async def wh_func(self):
        while True:
            print('While start')

    def while2_func(self):
        # while True:
        #     time.sleep(1)
        print('while2 func')

    def while_func(self,mode):
        print('while_func',mode)
        self.while2_func()
        # while True:
        # time.sleep(1)
        print('Wh st')
        #     self.while2_func()
        #     while True:
        #         time.sleep(1)
        #         print('Wh2 st2')
