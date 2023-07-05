# import serial
# ser = serial.Serial('COM2', 9600)
# print(ser)
# s =ser.readlines(100)
# # s =ser.readinto()
# print(s)

# ss = s.decode('utf-8')
# a =ss.count('\n', 0,len(ss))
# ss = ss.split('\n',a)
# print(ss)

# f = open('C:\\repo\date1','rb')
# ff =f.read().decode('utf-8')
# a =ff.count('\n', 0,len(ff))
# ss = ff.split('\n',a)
# print(ss)
# print(int(ss[0][20:25]))
# print(ss[0][20:25])
# print(ss[1][20:25])
# print(ss[2][20:25])

import random
class Date():
   def __init__(self):
      pass

   def date(self):
      return random.randint(1,100)

date = Date()
while(1):
   ask = date.date()
   print(ask)

# bin_s = bin(int(ss[0]))
# print(bin_s)
# print(bin_df)
# print(ss)
# lst.append(ss)
# print(lst)
# for i in ss:
#     if i =='\n': count =count+1

# ss = int.from_bytes(s, "big")
# print(ss)
# for i in s:
#     print(i)
# while(1):
#     print(s)
#     count=count+1
#     if count >10: break
# ser.close()