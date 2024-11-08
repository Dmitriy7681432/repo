import serial, time, binascii, struct
import serial.tools.list_ports
from lxml import etree
from debug import printf
from read_data import transformed_in_value,transformed_in_address,transformed_in_bytes
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
aa = 3218341888
aa = transformed_in_bytes(aa)
print(aa)
# port = "COM88"  # Replace with the appropriate COM port name
# baudrate = 3000000  # Replace with the desired baud rate
# count = 0
# list_read_data = []
# value = 0
# with serial.Serial(port, baudrate=baudrate, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS) as ser:
#     msg = b"L\r"
#     ser.write(msg)
