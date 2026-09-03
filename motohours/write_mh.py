from PyQt5.QtCore import pyqtSignal, QObject
import subprocess, struct

# from debug_mh import *

class WriteDataMh(QObject):
    cal_signal = pyqtSignal(int)
    flag_abort = 0

    def __init__(self, station, cnt_params, list_read_params):
        super().__init__()
        self.station = station
        self.cnt_params = cnt_params
        self.list_read_params = list_read_params
        if self.station == 'SES150' or self.station == 'TOR_ARCTICA':
            self.addr = '0xbfdc0000'
        else:
            self.addr = '0xbfd80000'

    def write(self):
        print(self.list_read_params,'3')
        # ќткрываем файл в бинарном режиме
        with open('write_mh.bin', 'wb') as f:
            for value in self.list_read_params:
                # ”паковываем число в 4 байта (формат '<i' Ч Little-Endian, 4 байта)
                binary_data = struct.pack('<i', value)
                f.write(binary_data)
        # subprocess.run(f'D:\\repo\\motohours\\mcprog\\mcprog.exe -e0 write_mh.bin {self.addr}',
        #                  shell=True, capture_output=True, text=True, errors='ignore')
