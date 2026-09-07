# # -*- coding: utf-8 -*-
# import struct
#
# # Размер файла в байтах: 2097152
# # Количество 4-байтовых элементов: 2097152 / 4 = 524288
# num_elements = 524288
#
# # Пример: создаем массив чисел (например, счетчик от 0 до num_elements - 1)
# # Использовать формат 'I' (беззнаковое 4 байта) или 'i' (знаковое 4 байта)
# data_format = "I"
# file_path = "output.bin"
#
# # Быстрая генерация и упаковка данных в бинарную строку (bytearray)
# # Для больших массивов байт-буфер работает эффективнее
# with open(file_path, "wb") as f:
#   # Записываем пачками или генерируем байты через байт-массив / map
#   # Пример записи по одному циклу (для наглядности) или через байтовую сборку:
#   chunk_size = 1024  # пишем блоками по 1024 элемента (4 КБ)
#   for i in range(0, num_elements, chunk_size):
#     # Упаковываем пачку чисел в 4-байтовом формате каждое
#     data =(0xAAAAAAAA).to_bytes(4, 'big')
#     # print(data,i)
#     chunk_data = [
#       struct.pack(data_format, data) for x in range(i, i + chunk_size)
#     ]
#     with open('output.txt','w') as f_txt:
#       f_txt.write(str(chunk_data))
#     f.write(b"".join(chunk_data))
#
# print(f"Файл {file_path} успешно записан. Размер: {num_elements * 4} байт.")

import struct,secrets

# Размер файла в байтах и размер одного блока (4 байта)
total_size = 2097152
chunk_size = 4

# Вычисляем количество повторений значения
count = total_size // chunk_size

# Упаковываем 0xAAAAAAAA в 4 байта (<' -little-endian, 'I' - unsigned int)
# Для big-endian используйте '>' вместо '<'
data = struct.pack('<I', 0xAAAAAAAA) * count

# Записываем в бинарный файл
with open('output.bin', 'wb') as f:
    f.write(data)

import struct

file_size = 2097152
chunk_size = 4
value = 0xABCD5432

# Считаем количество элементов
count = file_size // chunk_size

# Упаковываем все значения в бинарную строку (большой порядок байт '>' или системный '=')
# Используем '<I' для little-endian (младшим байтом вперед) или '>I' для big-endian
data = struct.pack(f'<{count}I', *([value] * count))

# Записываем в бинарный файл
with open('output1.bin', 'wb') as f:
    f.write(data)


import os

# Настройки
FILE_NAME = "random_data.bin"
FILE_SIZE = 2097152  # 2 МБ в байтах

# Генерируем случайные байты
# Так как нам нужны 4-байтовые значения, os.urandom заполнит файл случайным потоком байт,
# который при чтении по 4 байта даст нужные случайные hex-значения.
random_bytes = os.urandom(FILE_SIZE)

# Записываем байты в бинарный файл
with open(FILE_NAME, "wb") as f:
    f.write(random_bytes)


import struct

# Размер файла в байтах и размер одного блока (4 байта)
total_size = 262080
chunk_size = 4

# Вычисляем количество повторений значения
count = total_size // chunk_size

# Упаковываем 0xAAAAAAAA в 4 байта (<' -little-endian, 'I' - unsigned int)
# Для big-endian используйте '>' вместо '<'
data = struct.pack('<I', 0xFFFFFFFF) * count

# Записываем в бинарный файл
with open('erase.bin', 'wb') as f:
    f.write(data)
