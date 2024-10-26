## @file xml_versin.py
#  @brief Автоматическая генерация версии params.xml 
#  @details Автоматическая генерация версии блока для трех блоков управления
#  @date 27.10.2024
#  @author Алексин Д.В.
#  @version 0.0.1

# Пример запуска
# /etc/Python37/python \
#     py_scripts/bu_version.py \
#     src/generated/xml_version.c

# импорт внешних библиотек
from lxml import etree
import subprocess, io,re
# импорт встроенных модулей
import sys,os
import argparse
import datetime
encoding = 'utf-8'
# Увеличение версии
def cnt_increase(a: str) -> str:
    if a[7] == '9' and a[5] != '9' and a[3] != 9:
        a = a.replace('9', '0')
        b = int(a[5]) + 1
        a = a[:5]+str(b)+a[6:]
    elif a[5] == '9' and a[7] == '9' and a[3] != '9':
        a = a.replace('9', '0')
        b = int(a[3]) + 1
        a = a.replace(a[3], str(b))
    elif a[3] == '9' and a[5] == '9' and a[7] == '9':
        a = a.replace('9', '0')
        a = a.replace('9', '0')
        print(a[:2])
        a = a[:2] + '1' + a[3:]
    else:
        a = str(int(a) + 1)
        b = 8 - len(a)
        a = b * '0' + a
    return a

def main():
    # Смена кодировки вывода на utf-8
    sys.stdout.reconfigure(encoding=encoding)
    sys.stderr.reconfigure(encoding=encoding)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=encoding)
    # Печать на экран названия текущего скрипта
    print("bu_version.py")

    # Создание парсера аргументов
    # Чтобы посмотреть какие есть аргументы, нужно запустить скрипт с параметром --help
    # Например, python event_names.py --help
    parser = argparse.ArgumentParser()
    # parser.add_argument("params_xml_filename", help="params.xml filename with path")
    # аргумент <out_filename> - исходящий файл
    parser.add_argument("out_filename", help="output filename with path")
    # Парсинг аргументов
    args = parser.parse_args()

    # Печать на экран информации о именах исходных и выходных файлов
    print(f"create {args.out_filename}")

    file_bu_version_commit = 'bu_version_commit.txt'

    # Изменен ли главный модуль
    modified_files = subprocess.run('git status', shell=True, capture_output=True, text=True,encoding=encoding)
    modified_files = modified_files.stdout
    modified_files = modified_files.split('\n')

   # Есть ли изменения в главном модуле, кроме субмодулей и log_commit.txt
    flag = 0
    for i in modified_files:
        if 'изменено' in i and 'содержимое' not in i and \
                'log_commit.txt' not in i:
            flag =1

    # Если есть в главном модуле изменения есть
    if flag == 1:
        file_exist = os.path.isfile(file_bu_version_commit)
        # Существует ли файл bu_version_commit.txt
        if file_exist:
            print(f'file exist {file_bu_version_commit}')
            # Читаем текущий коммит и ветку
            head_commit = subprocess.run('git rev-parse HEAD', shell=True, capture_output=True,
                                         text=True, encoding=encoding)
            branch_head = subprocess.run('git symbolic-ref --short HEAD', shell=True,
                                         capture_output=True, text=True, encoding=encoding)
            # Читаем файл bu_version_commit.txt
            with open(file_bu_version_commit, 'r') as f2:
                data_file = f2.readlines()
                bu_version = data_file[2]
            # Если текущий коммит не равен коммиту из файла и текущая ветка равна ветки с файла 
            if head_commit.stdout != data_file[0] and data_file[1] == branch_head.stdout:
                print(f'change {file_bu_version_commit}')
                head_commit = subprocess.run('git rev-parse HEAD', shell=True,
                                             capture_output=True, text=True, encoding=encoding)
                # Увеличиваем версию на +1
                bu_version = cnt_increase(data_file[2])
                data_file.pop(0)
                data_file.pop(1)
                data_file.insert(0, head_commit.stdout)
                data_file.append(bu_version)
                # Записываем версию в файл
                with open(file_bu_version_commit, 'w') as f:
                    f.writelines(data_file)
            else:
                print(f'no change {file_bu_version_commit}')
        # Не существует файл bu_version_commit.txt
        else:
            # Поиск define SOFTWARE_VERSION
            software_version = subprocess.run('cd src/ && git grep SOFTWARE_VERSION', shell=True,
                                              capture_output=True, text=True, encoding=encoding)
            # Читаем текущий коммит и ветку
            data_file1 = []
            head_commit = subprocess.run('git rev-parse HEAD', shell=True, capture_output=True,
                                         text=True, encoding=encoding)
            data_file1.append(head_commit.stdout)

            branch_head = subprocess.run('git symbolic-ref --short HEAD', shell=True,
                                         capture_output=True, text=True, encoding=encoding)
            # Если мы стоим на ветке
            if branch_head.stdout:
                data_file1.append(branch_head.stdout)
            elif branch_head.stderr:
                data_file1.append('no_branch!!!')

            # Если define SOFTWARE_VERSION найден
            if software_version.stdout:
                print(f'create {file_bu_version_commit}')
                software_version_stdout =software_version.stdout.split(')')[1][2:]
                # Увеличиваем версию на +1
                bu_version = cnt_increase(software_version_stdout)
                data_file1.append(bu_version)
                # Записываем версию в файл
                with open(file_bu_version_commit, 'w') as f:
                    f.writelines(data_file1)
            else:
                print(f'no {file_bu_version_commit}')
    else:
        file_exist = os.path.isfile(file_bu_version_commit)
        # Существует ли файл bu_version_commit.txt
        if file_exist:
            # Читаем файл bu_version_commit.txt
            with open(file_bu_version_commit, 'r') as f2:
                data_file = f2.readlines()
                bu_version = data_file[2]
            print(f'no change main module and read bu_version with {file_bu_version_commit}')
        else:
            # Поиск define SOFTWARE_VERSION
            software_version = subprocess.run('cd src/ && git grep SOFTWARE_VERSION', shell=True, capture_output=True, text=True,encoding=encoding)
            if software_version.stdout:
                bu_version = software_version.stdout.split(')')[1][2:]
                print('no change main module and find SOFTWARE_VERSION ok')
            else:    
                bu_version = '000100000'
                print('no change main module and no find SOFTWARE_VERSION, bu_version default')
    
    print('BU_VERSION', bu_version)

    # Сохраняем новый файл
    with open(args.out_filename, "w", encoding=encoding) as f:
        f.write("//AUTOGENERATED FILE, DO NOT EDIT\n"\
        +"// Дата и время обновления: "\
        + datetime.datetime.now().strftime("%d.%m.%Y %H:%M") +'\n'\
        +f'#define BU_VERSION ((uint32_t)0x{bu_version})')


if __name__ == "__main__":
    main()
