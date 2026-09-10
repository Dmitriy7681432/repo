# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal,QObject
import struct,os
# from debug_mh import *
from PyQt5.QtCore import QThread, pyqtSignal


# 1. Создаем поток для выполнения подпроцесса
class ReadDataMh(QObject):
    # cal_signal = pyqtSignal(int)
    trigger = pyqtSignal()
    flag_abort = 0
    step = 0

    def __init__(self,cnt_params):
        super().__init__()
        self.file_path = 'read_mh.bin'
        self.data_list = []
        self.value_list = []
        self.cnt_params = cnt_params

    def read(self):
        self.data_list = []
        self.value_list = []

        # if os.path.exists(self.file_path):
        #     os.remove(self.file_path)
        # Открываем файл в бинарном режиме
        with open(self.file_path, 'rb') as f:
            # Цикл чтения файла по 4 байта
            while chunk := f.read(4):
                self.step += 1
                # self.cal_signal.emit(self.step)
                if self.flag_abort == 1:
                    return 'ABORT'
                # Если файл закончился или осталось меньше 4 байт
                if len(chunk) < 4:
                    break
                # Распаковываем 4 байта в число (например, беззнаковое 32-битное целое - 'I')
                # Используйте '<' для little-endian или '>' для big-endian байт-порядка
                value = struct.unpack('<I', chunk)[0]
                if value == 0xffffffff: break
                self.data_list.append(value)

        try:
            for i in range (0,self.cnt_params):
                self.value_list.append(self.data_list[-1*(self.cnt_params-i)])
        except IndexError:
            return 'ERR'
        print('read_data',len(self.data_list)/8,self.data_list)
        print('read_val',self.value_list)
        # print(data_list)
        # print(value_list)
        return 'OK'
    def clear_data_list(self):
        self.data_list = []


# read_obj = ReadDataMh('SES200M',8).read()