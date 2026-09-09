# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal,QObject
import subprocess,struct
# from debug_mh import *
from PyQt5.QtCore import QThread, pyqtSignal


# 1. Создаем поток для выполнения подпроцесса
class SubprocessMh(QThread):
    # Сигналы для передачи результатов в главный поток
    finished_success = pyqtSignal(str)
    finished_with_error = pyqtSignal(str)

    def __init__(self,station,mode):
        super().__init__()
        self.station = station
        self.mode = mode
        if self.station == 'SES150' or self.station == 'TOR_ARCTICA':
            self.addr = '0xbfdc0000'
        else:
            self.addr = '0xbfd80000'
        self.read_command = f'mcprog\\mcprog.exe -r read_mh.bin {self.addr} 262080'
        self.write_command =f'mcprog\\mcprog.exe -e0 write_mh.bin {self.addr}'
        self.erase_command = f'mcprog\\mcprog.exe -e2 erase_mh.bin {self.addr}'

    def run(self):
        try:
            # Запускаем команду (например, ping, который будет длиться долго)
            # timeout=5 означает, что через 5 секунд выбросится TimeoutExpired
            # result = subprocess.run(f'D:\\repo\\motohours\\mcprog\\mcprog.exe -r read_mh.bin {self.addr} 262080',
            if self.mode == 'read':
                print('sub_read')
                result=subprocess.run(self.read_command,capture_output=True,text=True,
                                      errors='ignore',
                                      timeout=5)
            elif self.mode == 'write':
                print('sub_write')
                result=subprocess.run(self.write_command,capture_output=True,text=True,
                                      errors='ignore',
                                      timeout=5)
            else:
                print('sub_erase')
                result=subprocess.run(self.erase_command,capture_output=True,text=True,
                                      errors='ignore',
                                      timeout=5)
                result=subprocess.run(self.write_command,capture_output=True,text=True,
                                      errors='ignore',
                                      timeout=5)

            self.finished_success.emit(result.stdout)

        except subprocess.TimeoutExpired:
            self.finished_with_error.emit("Превышено время ожидания! Процесс был принудительно прерван.")
            print('sub2')
        except Exception as e:
            self.finished_with_error.emit(f"Произошла ошибка: {str(e)}")
            print('sub3')
