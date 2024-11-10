import serial, time, binascii, struct
import serial.tools.list_ports
from lxml import etree
from debug import printf
from read_data import transformed_in_value,transformed_in_address,transformed_in_bytes
from class_read_data import Calibrator
a = 3218341888
a = 0xBFD40000
print(a)
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
