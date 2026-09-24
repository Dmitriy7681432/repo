from PyQt5.QtCore import pyqtSignal, QObject
import struct,os

# from debug_mh import *

class WriteDataMh(QObject):
    cal_signal = pyqtSignal(int)
    flag_abort = 0

    def __init__(self, list_read_params):
        super().__init__()
        self.file_path = 'write_mh.bin'
        self.list_read_params = list_read_params

    def write(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        # Открываем файл в бинарном режиме
        with open(self.file_path, 'wb') as f:
            for value in self.list_read_params:
                print(value)
                # Упаковываем число в 4 байта (формат '<i' — Little-Endian, 4 байта)
                binary_data = struct.pack('<I', value)
                # print('binary',binary_data)
                f.write(binary_data)
            # total_size = 262080 - len(self.list_read_params) *4
            # chunk_size = 4
            # # Вычисляем количество повторений значения
            # count = total_size // chunk_size
            # data = struct.pack('<I', 0xFFFFFFFF) * count
            # f.write(data)
        print('write_mh',len(self.list_read_params)/8, self.list_read_params)

    def update_data_list(self,list_data):
        self.list_read_params =list_data
