# -*- coding: utf-8 -*-
# len =5
lst = []
lst1 = [1,2]
lst.extend(lst1)
print(lst)
# print(len(lst))
# for i,val in enumerate(lst):
#     print(i,val,'1')

import subprocess
addr = '0xbfd80000'
read_command = f'mcprog\\mcprog.exe -r read_mh.bin {addr} 262080'
write_command = f'mcprog\\mcprog.exe -e0 write_mh.bin {addr}'
erase_command = f'mcprog\\mcprog.exe -e2 erase_mh.bin {addr}'
# exe_path = 'D:\repo\motohours\mcprog\mcprog.exe'
exe_path = 'mcprog\\mcprog.exe'
# result = subprocess.Popen(
#     # r'D:\repo\motohours\mcprog\mcprog.exe -r read_mh.bin 0xbfd8000 262080',
#     # r'mcprog\\mcprog.exe -r read_mh.bin 0xbfd80000 262080',
#     erase_command,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.STDOUT,
#     text=True,
#     errors='ignore'
# )
# # stdout, stderr = result.communicate(timeout=5)
# # returncode = result.returncode
#
# from tqdm import tqdm
# with tqdm(unit='line', desc='Выполнение') as pbar:
#
#     for line in result.stdout:
#         print('AAAAAAAAAAAAAAAAAAAAA')
#         print(line)
#         pbar.update(1)
#
# result.wait()
#
#
# import subprocess
# import sys
#
#
# def parse_mcproga_output():
#     # Запускаем команду.
#     # Замените ["mcproga", "--arg1"] на реальную команду запуска вашей программы.
#     command = f'mcprog\\mcprog.exe -e2 erase_mh.bin {addr}'
#
#     try:
#         process = subprocess.Popen(
#             command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.STDOUT,  # Объединяем вывод ошибок с обычным выводом
#             text=True,  # Автоматически декодирует байты в строки (utf-8)
#             bufsize=1,  # Включает строчную буферизацию
#         )
#
#         print("Процесс mcproga запущен. Начинаем чтение вывода...\n")
#
#         # Читаем вывод построчно в реальном времени
#         for line in process.stdout:
#             cleaned_line = line.strip()
#
#             # --- ЗДЕСЬ ВАША ЛОГИКА ПАРСИНГА ---
#             # Пример: ищем строку с процентами загрузки
#             if "Загрузка" in cleaned_line or "%" in cleaned_line:
#                 print(f"[ПАРСЕР]: Найдена строка загрузки -> {cleaned_line}")
#
#             # Для примера просто дублируем весь вывод в консоль Python
#             else:
#                 print(f"[ВЫВОД PROGA]: {cleaned_line}")
#
#         # Ждем завершения процесса и получаем код возврата
#         return_code = process.wait()
#         print(f"\nПроцесс завершился с кодом: {return_code}")
#
#     except FileNotFoundError:
#         print(
#             "Ошибка: Утилита mcproga не найдена. Проверьте путь или PATH.",
#             file=sys.stderr,
#         )
#     except Exception as e:
#         print(f"Произошла ошибка при запуске: {e}", file=sys.stderr)
#
#
# if __name__ == "__main__":
#     parse_mcproga_output()

# import sys
# import subprocess
#
# # Замените ['mcprog', 'аргументы'] на вашу реальную команду
# # cmd = ["mcprog", "--some-arguments"]
# cmd = f'mcprog\\mcprog.exe -e2 erase_mh.bin {addr}'
#
# process = subprocess.Popen(
#     cmd,
#     shell=True,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.STDOUT,
#     bufsize=0  # бинарный режим
# )
#
# buffer = b''
# while True:
#     ch = process.stdout.read(1)
#     if not ch and process.poll() is not None:
#         break
#     if ch == b'\r' or ch == b'\n':
#         if buffer.strip():
#             line = buffer.decode('utf-8', errors='ignore')
#             print(f"[LINE] {line}")
#         buffer = b''
#     else:
#         buffer += ch
# import sys
# import re
# import subprocess
# from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
#                              QProgressBar, QTextEdit, QPushButton)
# from PyQt5.QtCore import QThread, pyqtSignal
#
#
# class MCProgThread(QThread):
#     progress_updated = pyqtSignal(int)
#     output_updated = pyqtSignal(str)
#     finished_signal = pyqtSignal(int)
#
#     def __init__(self, command):
#         super().__init__()
#         self.command = command
#         self.process = None
#
#     def run(self):
#         self.process = subprocess.Popen(
#             self.command,
#             shell=True,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.STDOUT,
#             bufsize=0,
#         )
#
#         buffer = b''
#         last_line = ''
#         last_percent = -1
#
#         while True:
#             ch = self.process.stdout.read(1)
#             if not ch and self.process.poll() is not None:
#                 break
#             if not ch:
#                 continue
#
#             if ch in (b'\r', b'\n'):
#                 if buffer:
#                     line = buffer.decode('utf-8', errors='ignore').rstrip()
#                     if line and line != last_line:  # не дублируем
#                         last_line = line
#                         self.output_updated.emit(line)
#
#                         # Парсим проценты
#                         m = re.search(r'(\d+)\s*%', line)
#                         if m:
#                             pct = int(m.group(1))
#                             if pct != last_percent:
#                                 last_percent = pct
#                                 self.progress_updated.emit(pct)
#                 buffer = b''
#             else:
#                 buffer += ch
#
#         if buffer:
#             line = buffer.decode('utf-8', errors='ignore').rstrip()
#             if line:
#                 self.output_updated.emit(line)
#
#         self.process.wait()
#         self.finished_signal.emit(self.process.returncode)
#
#     def stop(self):
#         if self.process and self.process.poll() is None:
#             self.process.terminate()
#
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('mcprog progress')
#         self.resize(600, 400)
#
#         layout = QVBoxLayout(self)
#
#         self.progress = QProgressBar()
#         self.progress.setRange(0, 100)
#         layout.addWidget(self.progress)
#
#         self.output = QTextEdit()
#         self.output.setReadOnly(True)
#         layout.addWidget(self.output)
#
#         self.btn = QPushButton('Start')
#         self.btn.clicked.connect(self.start)
#         layout.addWidget(self.btn)
#
#         self.worker = None
#
#     def start(self):
#         self.progress.setValue(0)
#         self.output.clear()
#         self.btn.setEnabled(False)
#
#         self.worker = MCProgThread(
#             'mcprog\\mcprog.exe -e2 erase_mh.bin 0xbfd80000'
#         )
#         self.worker.progress_updated.connect(self.progress.setValue)
#         self.worker.output_updated.connect(self.output.append)
#         self.worker.finished_signal.connect(self.on_done)
#         self.worker.start()
#
#     def on_done(self, code):
#         self.btn.setEnabled(True)
#         self.progress.setValue(100)
#         self.output.append(f"\n=== Done (code={code}) ===")
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = MainWindow()
#     w.show()
#     sys.exit(app.exec_())

import win32gui
import win32con

def find_console_window(title_substr):
    result = []
    def cb(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            t = win32gui.GetWindowText(hwnd)
            if title_substr in t:
                result.append(hwnd)
        return True
    win32gui.EnumWindows(cb, None)
    return result[0] if result else None

# Периодически читаем текст из консоли
hwnd = find_console_window('mcprog')