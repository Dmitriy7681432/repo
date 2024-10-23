# -*- coding: utf-8 -*-
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

for port in ports:
    print(port.device)

import serial

port = "COM86"  # Replace with the appropriate COM port name
baudrate = 9600  # Replace with the desired baud rate

ser = serial.Serial(port, baudrate=baudrate)
print(ser.isOpen())

# Perform operations on the COM port

# Reading data
data = ser.read(1024)  # Read 10 bytes from the COM port
print(data)
ser.close()  # Remember to close the connection when done
