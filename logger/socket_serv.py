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












# import socket
#
# # https://otus.ru/journal/klient-servernaya-model-v-pitone-i-sokety/#:~:text=%D0%A1%D0%BE%D0%BA%D0%B5%D1%82%20%E2%80%93%20%D1%8D%D1%82%D0%BE%E2%80%A6,%D1%81%D1%87%D0%B8%D1%82%D1%8B%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B8%20%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D0%BD%D1%8B%D1%85%20%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D0%BE%D0%B2.
# # https://www.youtube.com/watch?v=MPjgHxK8k68&list=PLJrJ8Vs86KFlGegFVjfVS_JgqZ0rigU6Q&index=1
#
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('',5050))
# data, addres = sock.recvfrom(1024)
# sock.sendto(data,addres)
#
#
# import threading
# def read_sok():
#     while 1:
#         data =sor.recv(1024)
#         print(data.decode('utf-8'))
# server = '192.168.0.1', 5050
# alias = input()
# sor = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# sor.bind(('',0))
# sor.sendto((alias+' Connect to server').encode('utf-8'), server)
# potok = threading.Thread(target=read_sok)
# potok.start()
# while 1:
#     mensahe = input()
#     sor.sendto(('['+alias+']'+mensahe).encode('utf-8'), server)
#
# key = 567
# crypt = ''
# for i in message:
#     crypt+=chr(ord(i)^key)
# message =crypt
