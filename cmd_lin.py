# -*- coding: utf-8 -*-
import subprocess,os,struct,pickle
from subprocess import Popen,PIPE
import numpy as np

# try:
#     subprocess.Popen("D:\msys64\opt\elvees\mcprog\mcprog.exe")
# except FileNotFoundError:
#     print("Неверный каталог")
#     subprocess.Popen("D:\env\msys64\opt\elvees\mcprog\mcprog.exe")

# arg = ['cd', 'station_data']
# subprocess.run(arg)

# os.system('cd station_data/ && git rev-parse HEAD')
# os.system("D:/env/msys64/opt/elvees/mcprog/mcprog.exe")

# parse xml -------------------------------------------------------------
import xml.etree.ElementTree as ET

# tree = ET.parse('appt.xml')
tree = ET.parse('params.xml')
root = tree.getroot()

# # BBB
control_block = 0
count = 0
for setting in root.findall('.//setting'):
    designation = setting.attrib.get('designation')
    number = setting.attrib.get('number')
    dimension = setting.attrib.get('dimension')
    default_value = setting.attrib.get('default_value')
    c_type = setting.attrib.get('ctype')
    for products in setting.findall('products/'):
        product = products.tag
        if product =='SES200M':
            control_block = products.attrib.get('cb')
            if ((control_block == 'BU_50') or (control_block == 'BU_50')):
                count =count+1
                print(number,'',dimension,'',default_value,'',c_type)
                # file.write(number +' '+designation+' '+dimension+' '+default_value+ "\n")
print(count)

#end parse xml -------------------------------------------------------------
# with open("preset2.bin","r+b") as file_preset:
#     data_byte = file_preset.read()
#     a = struct.unpack("39if", data_byte[:160])
#     print(a)
#     # b = struct.unpack("f", data_byte[76:80])
#     # print(b)
#     print(data_byte[76:84])
#
# print('=================')
# e = struct.pack('i',5)
# print(e)
# c = struct.unpack("f",e)
# print(c)



# Поиск файла в каталоге
# for root, dirs, files in os.walk('D:\env'):
#     for file in files:
#         if file.endswith('mcprog.exe'):
#             print(os.path.join(root, file))