# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal,QObject
import subprocess,time
# from debug_mh import *
from PyQt5.QtCore import QThread, pyqtSignal


# 1. Создаем поток для выполнения подпроцесса
class SubprocessMh(QThread):
    # Сигналы для передачи результатов в главный поток
    finished_success = pyqtSignal(str)
    finished_with_error = pyqtSignal(str)

    def __init__(self,command):
        super().__init__()
        self.command = command
        print(self.command)

    def run(self):
        try:

            result=subprocess.run(self.command,capture_output=True,text=True,
                                  errors='ignore',
                                  timeout=20)
            self.finished_success.emit(result.stdout)
        except subprocess.TimeoutExpired:
            self.finished_with_error.emit("Превышено время ожидания! Процесс был принудительно прерван.")
            print('sub2')
        except Exception as e:
            # self.finished_with_error.emit(f"Произошла ошибка: {str(e)}")
            self.finished_with_error.emit("Произошла ошибка")

