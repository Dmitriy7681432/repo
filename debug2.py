# -*- coding: utf-8 -*-
# import serial.tools.list_ports
# ports = serial.tools.list_ports.comports()
#
# for port in ports:
#     print(port.device)
#
# import serial
#
# port = "COM88"  # Replace with the appropriate COM port name
# baudrate = 3000000# Replace with the desired baud rate
#
# ser = serial.Serial(port, baudrate=baudrate,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
# print(ser.isOpen())

# Perform operations on the COM port

# ser.timeout = 0.01
# print("port:", port)
# msg = b"C\r"
# ser.write(msg)
# print("T>", msg)
# print("R>", ser.read(1000))
# msg = b"S5\rZ1\r"
# ser.write(msg)
# print("T>", msg)
# print("R>", ser.read(1000))
# msg = b"L\r"
# ser.write(msg)
# print("T>", msg)

# ser.timeout = 0.1
# # print("port:", port)
# msg = b"C\r"
# ser.write(msg)
# msg = b"S5\rZ1\r"
# ser.write(msg)
# msg = b"L\r"
# ser.write(msg)
# # msg1 = b"t00A8EB2E000000005500\r"
#
# # Reading data
# data = ser.read(1024)  # Read 10 bytes from the COM port
# # # ser.write(package)
# print(data)
# ser.close()  # Remember to close the connection when done

# msg = b"C\r"
# ser.write(msg)












#
# print(package)
# import can
# # bus = can.interfaces.slcan.slcanBus('COM80',ttyBaudrate=9600)
# import can
# import time

# Configuration for the SLCAN device
# slcan_device = 'COM88'
# baud_rate = 1000000# Set the appropriate baud rate for your setup
#
# # Create a CAN bus instance using the SLCAN interface
# bus = can.interface.Bus(interface='slcan', channel=slcan_device, bitrate=baud_rate)
# #
# # Define a simple CAN message
# can_id = 0xA  # CAN ID
# data = [0xEB, 0x2E, 0x00, 0x00, 0x00, 0x00, 0x55, 0x00]  # 8 bytes of data
# # data = [0x55]
# # Create a CAN message
# message = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
# try:
#     # while True:
#     # Send the CAN message
#     bus.send(message)
#     print(f"Sent: {message}")
#
#     # Wait for a second before sending the next message
#     time.sleep(1)
#
# except KeyboardInterrupt:
#     print("Stopped by user")
#
# except can.CanError as e:
#     print(f"CAN error: {e}")

# count =0
# try:
#     # with open('data_titan1.txt','w') as f:
#     #     while count <200:
#     count +=1
#     data = bus.recv()
#     # f.writelines(str(data)+'\n')
#     print(data)
# except KeyboardInterrupt:
#     print("Stopped by user")

# except can.CanError as e:
#     print(f"CAN error: {e}")

import struct
# C Z1 L
# msg = b"C\r"
# msg = b"S5\rZ1\r"
# msg = b"L\r"
# # a = struct.unpack('!i', msg)
# a = msg.decode('utf-8')
# print(a)


a = '3z.0'
b = '0'
if a.isalnum():
    print('Yes')


import re

data_pattern = "^[a-zA-Zа-яА-ЯёЁ]+$"
data_pattern1 = "^[0-9.]+$"
def is_valid_email(data):
    """
    Расшифровка:
    ^ - начало строки;
    -? - символ "минус" ноль или один раз;
    \d + - цифры, минимум одна штука
    \.? - символ точки ноль или один раз
    \d * - снова цифры, но в этот раз минимум ноль раз
    $ - конец строки
    """
    # return re.match('^[-]+[0-9]*[.][0-9]+$', data) is not None
    return re.match('^-?\d+\.?\d*$', data) is not None


# data = "gkegfemeeуууее&@("
data = "1"
if not '.' in data and is_valid_email(data):
    print('Yes')


print(is_valid_email(data))

df ='8'
if float(df):
    print('OOOO')
# print(float(df))


lst = ['1','2']
lst [0] = '3'
# print(lst)
x = {'one': 1, 'two': 2, 'three': 3, 'four': 4}
xx = x.copy()
xx['one'] = 2
# print(x)
# print(xx)

def foo(data):
    if not hasattr(foo, "counter"):
        foo.counter = 0
    foo.counter += 1
    # print("counter is", foo.counter)
    return foo.counter

# print(foo(1))
# print(foo(2))
import struct
f = open('preset1.bin','wb')
sr = struct.pack('f', 0.1)
sr1 = struct.pack('f', 0.8)
sr2 = struct.pack('f', 0.8)
sr3 = struct.pack('f', 0.8)
# print(sr)
# print(sr1)
f.write(sr)
f.write(sr1)
f.write(sr2)
f.write(sr3)
f.close()

a = '00000320'
a = 'c2e70000'
a = struct.unpack('!f', bytes.fromhex(a))[0]
# print(a)

text1 = 'Параметры уставки калибровки классы аt'
text1 = list(text1)
# text1 = ''.join(text1)
# print(text1)

def fun_text(text):
    pass

dct = {}
dct['ar'] = {}

# print(dct)
dct['ar']['N_U'] = ['reo','qw']
dct['ar']['N1_U'] = ['reo','qw']
dct['ar1'] = {}
dct['ar1']['N2_U'] = ['reo','qw']
dct['ar1']['N3_U'] = ['reo','qw']
dct['ar']['N4_U'] = dct['ar'].pop('N_U')
# dct['rr'] = dct['ar']; del dct['ar']
# print(dct)


param_dict  ={'BU_400': {'ElectroStation': {'ALARM_REACT_CHANGE': ['Изменение реакции аварий', 'int']}, 'Net': {'N_STATE': ['Состояние', 'int'], 'NET1_NORM': ['Параметры сети 1 в норме', 'int']}, 'Net2': {'N2_STATE': ['Состояние', 'int'], 'NET2_NORM': ['Параметры сети 2 в норме', 'int']}, 'EA': {'EA_STATE': ['Состояние', 'int'], 'EA_t_COOL': ['t охлаждающей жидкости, °C', 'float']}, 'BU': {'AIR_TEMP': ['T воздуха в отсеке, °C', 'float']}, 'FUEL_PUMP': {'LEVEL_FUEL': ['Уровень топлива во внутреннем баке с датчика, мм*10^-1', 'int'], 'LEVEL_EXT_FUEL': ['Уровень топлива во внешнем баке с датчика, мм*10^-1', 'int'], 'GRADIENT_LEVEL_FUEL': ['Градиент уровня топлива во внутреннем баке', 'float'], 'GRADIENT_LEVEL_EXT_FUEL': ['Градиент уровня топлива во внешнем баке', 'float'], 'NZT_STATE': ['Состояние НЗТ', 'int'], 'LEVEL_FUEL_CALC': ['Уровень топлива во внутреннем баке, вычисляемый, %', 'float'], 'LEVEL_EXT_FUEL_CALC': ['Уровень топлива во внешнем баке, вычисляемый, %', 'float'], 'NZT_MODE': ['Режим работы НЗТ', 'int']}, 'FC1': {'FC1_U_A': ['U фазы А, В', 'float'], 'FC1_U_B': ['U фазы B, В', 'float'], 'FC1_U_C': ['U фазы C, В', 'float'], 'FC1_F_U_A': ['F U фазы А, Гц', 'float'], 'FC1_F_U_B': ['F U фазы B, Гц', 'float'], 'FC1_F_U_C': ['F U фазы C, Гц', 'float'], 'FC1_PHI_U_A': ['Угол U фазы А, °', 'float'], 'FC1_PHI_U_B': ['Угол U фазы B, °', 'float'], 'FC1_PHI_U_C': ['Угол U фазы C, °', 'float'], 'FC1_I_A': ['I фазы А, А', 'float'], 'FC1_I_B': ['I фазы B, А', 'float'], 'FC1_I_C': ['I фазы C, А', 'float'], 'FC1_PHI_I_A': ['Угол I фазы А, °', 'float'], 'FC1_PHI_I_B': ['Угол I фазы B, °', 'float'], 'FC1_PHI_I_C': ['Угол I фазы C, °', 'float'], 'FC1_U_A2': ['U фазы А2, В', 'float'], 'FC1_F_U_A2': ['F U фазы А2, Гц', 'float'], 'FC1_PHI_U_A2': ['Угол U фазы А2, °', 'float'], 'FC1_AE_STATE': ['Состояние АД ПЧ', 'int'], 'FC1_GEN_STATE': ['Состояние генератора ПЧ 1', 'int'], 'FC1_P': ['Активная мощность ПЧ 1, кВт', 'float']}, 'FC2': {'FC2_U_A': ['U фазы А, В', 'float'], 'FC2_U_B': ['U фазы B, В', 'float'], 'FC2_U_C': ['U фазы C, В', 'float'], 'FC2_F_U_A': ['F U фазы А, Гц', 'float'], 'FC2_F_U_B': ['F U фазы B, Гц', 'float'], 'FC2_F_U_C': ['F U фазы C, Гц', 'float'], 'FC2_PHI_U_A': ['Угол U фазы А, °', 'float'], 'FC2_PHI_U_B': ['Угол U фазы B, °', 'float'], 'FC2_PHI_U_C': ['Угол U фазы C, °', 'float'], 'FC2_I_A': ['I фазы А, А', 'float'], 'FC2_I_B': ['I фазы B, А', 'float'], 'FC2_I_C': ['I фазы C, А', 'float'], 'FC2_PHI_I_A': ['Угол I фазы А, °', 'float'], 'FC2_PHI_I_B': ['Угол I фазы B, °', 'float'], 'FC2_PHI_I_C': ['Угол I фазы C, °', 'float'], 'FC2_U_A2': ['U фазы А2, В', 'float'], 'FC2_F_U_A2': ['F U фазы А2, Гц', 'float'], 'FC2_PHI_U_A2': ['Угол U фазы А2, °', 'float'], 'FC2_AE_STATE': ['Состояние АД ПЧ', 'int'], 'FC2_GEN_STATE': ['Состояние генератора ПЧ', 'int'], 'FC2_P': ['Активная мощность ПЧ2, кВт', 'float']}, 'UKPT2': {'STATUS_IVEP': ['Состояние ИВЭП', 'int']}}}
# param_dict['BU_400']['Cредство электроснабжения СЭС-200М'] = param_dict['BU_400'].pop('ElectroStation')
# print(param_dict['BU_400'].items())
for elem, i in zip(range(0,10),param_dict['BU_400'].items()):
    j = [j for j in i[1].values()]
    # print(i[0],j[0][0])
    # print(elem)

def trans_str(metric,text):
    flag = 0
    if metric >269:
        len_text = int(269/7)
        # printf(len_text,len(text),text)
        text = list(text)
        # print(text)
        for i in range(0,len(text)):
            if i*7>269:
                if text[i] != ' ':
                    if flag==0:
                        j = i
                        flag=1
                    if flag==1:
                        j-=1
                        if text[j]==' ':
                            text[j] = '\n'
                            break
                elif text[i] == ' ':
                    text[i] = '\n'
                    break
        text = ''.join(text)
        return [text]
    else: return [text]

text = 'Уровень топлива во внутреннем баке с датчика, мм*10^-1'
a = trans_str(365,text)
# print(a)

addr1 = 0xbfdc0000
addr2 = 0xbfdc0000
addr3 = 0xbfdc0000
ad_lst1 = []
ad_lst2 = []

# while(addr1 <= 0xbfdfffc0):
#     addr1 += 32
#     ad_lst1.append(hex(addr1))
# print(ad_lst1)
# while(addr2 <= 0xbfdfffc0):
#     addr2 += 24
#     ad_lst2.append(hex(addr2))
# print(ad_lst2)

while(addr3 <= 0xbfdfffc0):
    addr3 +=36
    # print(hex(addr3))

for i in range(0,5):
    pass
    # print(i)