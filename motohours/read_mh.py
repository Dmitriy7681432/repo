# -*- coding: utf-8 -*-
import subprocess,struct
class ReadDataMh():

    def __init__(self):
        pass

    def read(self):
        process = subprocess.run('D:\\repo\\motohours\\mcprog\\mcprog.exe -r mh.bin 0xbfd80000 262080',
                                 shell=True, capture_output=True, text=True, errors='ignore')
        data_list = []
        # Открываем файл в бинарном режиме
        with open('mh.bin', 'rb') as f:
            # Цикл чтения файла по 4 байта
            while chunk := f.read(4):
                # Если файл закончился или осталось меньше 4 байт
                if len(chunk) < 4:
                    break
                # Распаковываем 4 байта в число (например, беззнаковое 32-битное целое - 'I')
                # Используйте '<' для little-endian или '>' для big-endian байт-порядка
                value = struct.unpack('<I', chunk)[0]
                if value == 0xffffffff: break
                data_list.append(value)

                # print(value)
        return 

        print(data_list)