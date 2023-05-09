# -*- coding: utf-8 -*-
import socket

listener =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
IP = socket.gethostbyname(socket.gethostname())
print(IP)
PORT = 12333
listener.bind((IP,PORT))
listener.listen(0)

connection, address = listener.accept()

print('lol')
connection.send('Привет, подключайся!'.encode('utf-8'))
connection.send('Привет!'.encode('utf-8'))
while True:
    data_output = ''
    while True:
        data = connection.recv(1024).decode('utf-8')
        data_output+=data
        if not data:
            break
    print(data_output)



connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = '192.168.43.100'
PORT =12333
connection.connect((IP, PORT))
rd = connection.recv(1024)
print(rd.decode('utf-8'))
connection.send('И тебе привет!'.encode('utf-8'))
connection.close()
