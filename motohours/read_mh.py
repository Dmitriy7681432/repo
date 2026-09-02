# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal,QObject
import subprocess,struct
class ReadDataMh(QObject):
    cal_signal = pyqtSignal(int)
    flag_abort = 0

    def __init__(self,station,cnt_params):
        super().__init__()
        self.data_list = []
        self.value_list = []
        self.station = station
        self.cnt_params = cnt_params
        if self.station == 'SES150' or self.station == 'TOR_ARCTICA':
            self.addr = '0xbfdc0000'
        else:
            self.addr = '0xbfd80000'

    def read(self):
        self.data_list = []
        self.value_list = []
        step = 0
        # process = subprocess.run(f'D:\\repo\\motohours\\mcprog\\mcprog.exe -r mh.bin {self.addr} 262080',
        #                          shell=True, capture_output=True, text=True, errors='ignore')
        # Открываем файл в бинарном режиме
        with open('mh.bin', 'rb') as f:
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

# read_obj = ReadDataMh('SES200M',8).read()