## @file xml_versin.py
#  @brief Автоматическая генерация версии params.xml 
#  @details Автоматическая генерация версии params.xml для трех блоков управления
#  @date 17.10.2024
#  @author Алексин Д.в.
#  @version 0.0.1

# Пример запуска
# /etc/Python37/python \
#     py_scripts/xml_version.py \
#     -station SES200M
#     -control_block BU_50
#     tests/data_in/5/params.xml
#     src/generated/xml_version.c

# импорт внешних библиотек
from lxml import etree
import os, subprocess, sys, io,re
# импорт встроенных модулей
import sys
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

# Изменение xml
def read_write_XML(xmlFile,operation='r')->str:
    value =0
    doc = etree.parse(xmlFile)
    for setting in doc.findall('.//can'):
        puprose = setting.attrib.get('purpose')
        if puprose == "XML_VERSION":
            value = setting.attrib.get('value')
            if operation =='w':
                value_cnt = cnt_increase(value)
                setting.attrib['value'] = value_cnt

    if operation == 'w':
        doc.write(xmlFile, encoding=encoding)
    return value

def main():
    # Смена кодировки вывода на utf-8
    sys.stdout.reconfigure(encoding=encoding)
    sys.stderr.reconfigure(encoding=encoding)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=encoding)
    # Печать на экран названия текущего скрипта
    print("xml_version.py")

    # Создание парсера аргументов
    # Чтобы посмотреть какие есть аргументы, нужно запустить скрипт с параметром --help
    # Например, python event_names.py --help
    parser = argparse.ArgumentParser()
    # аргумент -station <station>
    # аргумент <params_xml_filename> - входящий файл
    parser.add_argument("params_xml_filename", help="params.xml filename with path")
    # аргумент <out_filename> - исходящий файл
    parser.add_argument("out_filename", help="output filename with path")
    # Парсинг аргументов
    args = parser.parse_args()

    # Печать на экран информации о именах исходных и выходных файлов
    print(f"{args.params_xml_filename} -> {args.out_filename}")

    dir = re.findall(r'\w+', args.params_xml_filename)
    catalog = dir[0] +'/'
    file =dir[1] + '.' + dir[2]

    file_xml_commit = catalog + 'xml_commit.txt'

    # Изменен ли params.xml
    modified_files = subprocess.run(f'cd {catalog} && git status', shell=True, capture_output=True, text=True,encoding=encoding)
    modified_files = modified_files.stdout
    modified_files = modified_files.split('\n')

    flag = 0
    for i in modified_files:
        if file in i:
            flag = 1

    if flag == 1:
        file_exist = os.path.isfile(file_xml_commit)
        if file_exist:
            head_commit = subprocess.run(f'cd {catalog} && git rev-parse HEAD', shell=True, capture_output=True,
                                         text=True, encoding=encoding)
            branch_head = subprocess.run(f'cd {catalog} && git symbolic-ref --short HEAD', shell=True,
                                         capture_output=True, text=True, encoding=encoding)
            with open(file_xml_commit, 'r') as f2:
                data_file = f2.readlines()
            if head_commit.stdout != data_file[0] and data_file[1] == branch_head.stdout:
                print('change_xml_version')
                head_commit = subprocess.run(f'cd {catalog} && git rev-parse HEAD', shell=True,
                                             capture_output=True, text=True, encoding=encoding)

                data_file.pop(0)
                data_file.insert(0, head_commit.stdout)
                with open(file_xml_commit, 'w') as f:
                    f.writelines(data_file)
                read_write_XML(args.params_xml_filename,'w')
            else:
                print('no change_xml_version')
        else:
            data_file1 = []
            print('create xml_commit.txt and change_xml_version')
            head_commit = subprocess.run(f'cd {catalog} && git rev-parse HEAD', shell=True, capture_output=True,
                                         text=True, encoding=encoding)
            data_file1.append(head_commit.stdout)

            branch_head = subprocess.run(f'cd {catalog} && git symbolic-ref --short HEAD', shell=True,
                                         capture_output=True, text=True, encoding=encoding)
            if branch_head.stdout:
                data_file1.append(branch_head.stdout)
            elif branch_head.stderr:
                data_file1.append('no_branch!!!')
            with open(file_xml_commit, 'w') as f:
                f.writelines(data_file1)
            read_write_XML(args.params_xml_filename,'w')
    else:
        print('no change_xml_version and no modified params.xml')

    value = read_write_XML(args.params_xml_filename)
    print('XML_VERSION',value)

    # Сохраняем новый файл
    with open(args.out_filename, "w", encoding=encoding) as f:
        f.write("//AUTOGENERATED FILE, DO NOT EDIT\n"\
        +"// Дата и время обновления: "\
        + datetime.datetime.now().strftime("%d.%m.%Y %H:%M") +'\n'\
        +f'#define XML_VERSION ((uint32_t)0x{value})')


if __name__ == "__main__":
    main()
