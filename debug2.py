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
    return re.match('^[0-9]*[.][0-9]+$', data) is not None

# data = "gkegfemeeуууее&@("
data = "1..1"


print(is_valid_email(data))

df ='8'
if float(df):
    print('OOOO')
print(float(df))


lst = ['1','2']
lst [0] = '3'
print(lst)
x = {'one': 1, 'two': 2, 'three': 3, 'four': 4}

def foo(data):
    if not hasattr(foo, "counter"):
        foo.counter = 0
    foo.counter += 1
    print("counter is", foo.counter)
    return foo.counter

print(foo(1))
print(foo(2))
import struct
f = open('preset1.bin','wb')
sr = struct.pack('f', 0.1)
sr1 = struct.pack('f', 0.8)
sr2 = struct.pack('f', 0.8)
sr3 = struct.pack('f', 0.8)
print(sr)
print(sr1)
f.write(sr)
f.write(sr1)
f.write(sr2)
f.write(sr3)
f.close()

a = '00000320'
# a = '3f4ccccd'
a = struct.unpack('!i', bytes.fromhex(a))[0]
print(a)
a = '0.1'
a = int(float(a)*100)
print(a)