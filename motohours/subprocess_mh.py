# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal,QObject
import subprocess,sys
# from debug_mh import *
from PyQt5.QtCore import QThread, pyqtSignal


# 1. Создаем поток для выполнения подпроцесса
class SubprocessMh(QThread):
    # Сигналы для передачи результатов в главный поток
    finished_success = pyqtSignal(str)
    finished_with_error = pyqtSignal(str)

    def __init__(self,command,timeout):
        super().__init__()
        self.command = command
        self.timeout=timeout
        print(self.command)
        self.kwargs = {}

        if sys.platform == 'win32':
            # Способ 1: флаг CREATE_NO_WINDOW
            self.kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
            # Способ 2 (дублируем): startupinfo со скрытием
            # si = subprocess.STARTUPINFO()
            # si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # si.wShowWindow = subprocess.SW_HIDE
            # self.kwargs['startupinfo'] = si

    def run(self):
        try:

            result=subprocess.run(self.command,capture_output=True,text=True,
                                  errors='ignore',
                                  timeout=self.timeout,**self.kwargs)
            self.finished_success.emit(result.stdout)
        except subprocess.TimeoutExpired:
            self.finished_with_error.emit("Превышено время ожидания! Процесс был принудительно прерван.")
            # print('sub2')
        except Exception as e:
            # self.finished_with_error.emit(f"Произошла ошибка: {str(e)}")
            self.finished_with_error.emit("Произошла ошибка")

