# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal,QObject
import subprocess,struct
# from debug_mh import *
from PyQt5.QtCore import QThread, pyqtSignal


# 1. Создаем поток для выполнения подпроцесса
class ReadDataMh(QObject):
    cal_signal = pyqtSignal(int)
    trigger = pyqtSignal()
    flag_abort = 0

    def __init__(self,cnt_params):
        super().__init__()
        self.data_list = []
        self.value_list = []
        self.cnt_params = cnt_params

    def read(self):
        self.data_list = []
        self.value_list = []
        step = 0

        # print('read1')
        # subprocess.run(f'D:\\repo\\motohours\\mcprog\\mcprog.exe -r read_mh.bin {self.addr} 262080',
        #                          shell=True, capture_output=True, text=True, errors='ignore')

        # Открываем файл в бинарном режиме
        with open('read_mh.bin', 'rb') as f:
            # Цикл чтения файла по 4 байта
            while chunk := f.read(4):
                step += 1
                self.cal_signal.emit(step)
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

        for i in range (0,self.cnt_params):
            self.value_list.append(self.data_list[-1*(self.cnt_params-i)])
        # print(data_list)
        # print(value_list)
        return 'OK'
    def clear_data_list(self):
        self.data_list = []


# read_obj = ReadDataMh('SES200M',8).read()