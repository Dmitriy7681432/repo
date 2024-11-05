import serial, time, binascii, struct
import serial.tools.list_ports
from lxml import etree
from debug import printf
from read_data import transformed_in_value
# b = b't64A8E400000000E50000'
# b = b't64A8E400000000E500009'
b = b'AAB8E400000000E5000064A8\nA64A8E400000000E50000930D'
if b't64A' in b:
# b = b[1:4]
    print(b)
# b = transformed_in_value(b)
# print(b)
# port = "COM88"  # Replace with the appropriate COM port name
# baudrate = 3000000  # Replace with the desired baud rate
# count = 0
# list_read_data = []
# value = 0
# with serial.Serial(port, baudrate=baudrate, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS) as ser:
#     msg = b"L\r"
#     ser.write(msg)
