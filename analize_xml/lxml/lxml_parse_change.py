# -*- coding: utf-8 -*-
from lxml import etree
import os, subprocess, sys, io

file_xml_commit = '../station_data/xml_commit.txt'


# Увеличение версии
def cnt_increase(a: str) -> str:
    if a[7] == '9' and a[5] != '9' and a[3] != 9:
        a = a.replace('9', '0')
        b = int(a[5]) + 1
        a = a.replace(a[5], str(b))
    elif a[5] == '9' and a[7] == '9' and a[3] != '9':
        a = a.replace('9', '0')
        b = int(a[3]) + 1
        a = a.replace(a[3], str(b))
    elif a[3] == '9' and a[5] == '9' and a[7] == '9':
        a = a.replace('9', '0')
        print(a[:2])
        a = a[:2] + '1' + a[3:]
    else:
        a = str(int(a) + 1)
        b = 8 - len(a)
        a = b * '0' + a
    return a


# Изменение xml
def parseXML(xmlFile):
    doc = etree.parse(xmlFile)
    for setting in doc.findall('.//can'):
        puprose = setting.attrib.get('puprose')
        if puprose == "XML_VERSION":
            value = setting.attrib.get('value')
            value_cnt = cnt_increase(value)
            setting.attrib['value'] = value_cnt
            print(value)

    doc.write(xmlFile, encoding='utf-8')


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # Изменен ли params.xml
    modified_files = subprocess.run('cd ../station_data/&& git status', shell=True, capture_output=True, text=True,
                       encoding='utf-8')
    modified_files = modified_files.stdout
    modified_files = modified_files.split('\n')

    flag = 0
    print(modified_files)
    for i in modified_files:
        if 'params.xml' in i:
            flag = 1

    if flag == 1:
        file_exist = os.path.isfile(file_xml_commit)
        print(file_exist)
        if file_exist:
            head_commit = subprocess.run('cd ../station_data/&& git rev-parse HEAD', shell=True, capture_output=True,
                                         text=True,encoding='utf-8')
            branch_head = subprocess.run('cd ../station_data/&& git symbolic-ref --short HEAD', shell=True,
                                         capture_output=True, text=True, encoding='utf-8')
            with open(file_xml_commit, 'r') as f2:
                data_file = f2.readlines()
                cnt = int(data_file[1])
            if head_commit.stdout == data_file[0] and cnt >= 1:
                print('IF')
                cnt = cnt + 1
                data_file.pop(1)
                data_file.insert(1, str(cnt)+'\n')
                print(data_file)
                with open(file_xml_commit, 'w') as f:
                    f.writelines(data_file)
            elif head_commit.stdout != data_file[0] and data_file[2] == branch_head.stdout:
                print('ELSE')
                cnt = 1
                head_commit = subprocess.run('cd ../station_data/&& git rev-parse HEAD', shell=True,
                                             capture_output=True, text=True, encoding='utf-8')

                data_file.pop(0)
                data_file.pop(0)
                data_file.insert(0, head_commit.stdout)
                data_file.insert(1, str(cnt))
                with open(file_xml_commit, 'w') as f:
                    f.writelines(data_file)
                parseXML('../station_data/params.xml')
        else:
            data_file1 = []
            print('else')
            cnt = '1\n'
            head_commit = subprocess.run('cd ../station_data/&& git rev-parse HEAD', shell=True, capture_output=True,
                                         text=True, encoding='utf-8')
            data_file1.append(head_commit.stdout)
            data_file1.append(cnt)

            branch_head = subprocess.run('cd ../station_data/&& git symbolic-ref --short HEAD', shell=True,
                                         capture_output=True, text=True, encoding='utf-8')
            if branch_head.stdout:
                data_file1.append(branch_head.stdout)
            elif branch_head.stderr:
                data_file1.append('no_branch!!!')
            print(data_file1)
            with open(file_xml_commit, 'w') as f:
                f.writelines(data_file1)
            parseXML('../station_data/params.xml')


if __name__ == "__main__":
    main()

# import xml.etree.ElementTree as ET
#
# tree = ET.parse('params.xml')
# root = tree.getroot()
#
# value =0
# for setting in root.findall('.//can'):
#     puprose = setting.attrib.get('puprose')
#     if puprose == "XML_VERSION":
#         value = setting.attrib.get('value')
#         setting.set('value','00010004')
#
#
#     print(int(value))
#
# tree.write('params.xml',encoding='utf-8',short_empty_elements=True)
