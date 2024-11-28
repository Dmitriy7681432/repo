import serial, time, binascii, struct
import serial.tools.list_ports
from lxml import etree
from debug import printf
# from read_data import transformed_in_value,transformed_in_address,transformed_in_bytes
# from class_read_data import Calibrator
a = 3218341888
a = 0xBFD40000
a = '00010509\n)'
a.replace('\n','')
print(a)

def func ():
    calibr_list_data = []
    preset_list_data = []

    doc = etree.parse('params.xml')
    for setting in doc.findall('.//setting'):
        number = setting.attrib.get('number')
        c_type = setting.attrib.get('ctype')
        for products in setting.findall('products/'):
            product = products.tag
            if product == "SES200M":
                cb = products.attrib.get('cb')
                if cb == 'BU_50':
                    preset_list_data.append(number)
                    preset_list_data.append(c_type)

    for setting in doc.findall('.//parameter'):
        designation = setting.attrib.get('designation')
        for products1 in setting.findall('.//SES200M'):
            cb = products1.attrib.get('cb')
            if cb == 'BU_50':
                for products2 in products1.findall('.//calibration'):
                    if len(products2.getchildren()) !=0:
                        for i in products2.findall('.//k'):
                            calibr_list_data.append(designation+'_'+i.attrib.get('IND'))
                            calibr_list_data.append(i.attrib.get('value'))
                    else:
                        calibr_list_data.append(designation + '_k')
                        calibr_list_data.append('1.0')
                        calibr_list_data.append(designation + '_b')
                        calibr_list_data.append('1.0')
    return calibr_list_data,preset_list_data

a,b = func()
print(a)
print(b)
# b = b't64A8E400000000E50000'
# b = b't64A8E400000000E500009'
# b = b'AAB8E400000000E5000064A8\nA64A8E400000000E50000930D'
# b = b't61880400D4BF5A5AA5A5'
# c = b't6188000000000401D4BF'
# b = transformed_in_address(b)
# c = transformed_in_value(c)
# print(hex(b))
# print(hex(c))
# serial.Serial.flushInput()
# aa = hex(1550).encode('utf-8')[2:]

# print(b't'+aa+b'8')
# class Obj:
#     def __init__(self,read_id):
#         self.read_id = read_id
#     def trans(self,arg):
#         read_id = self.read_id
#         # print(arg)
#         # print(read_id)
#         return arg,read_id
#
# obj = Obj(1550)
# a,b = obj.trans(20)
# print(a)
# print(b)
