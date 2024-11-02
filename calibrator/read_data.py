import serial,time
import serial.tools.list_ports

def can_open(arg):
    arg.timeot = 0.01
    msg = b"C\r"
    arg.write(msg)
    print("T>",msg)
    # print("R>", arg.read(1000))
    msg = b"S5\rZ1\r"
    arg.write(msg)
    print("T>",msg)
    # print("R>", arg.read(1000))
    msg = b"L\r"
    arg.write(msg)
    return 0

def can_close(arg):
    msg = b"C\r"
    arg.write(msg)
    print(msg,'can_close')
    return 0

ports = serial.tools.list_ports.comports()

for port in ports:
    print(port.device)

port = "COM88"  # Replace with the appropriate COM port name
baudrate = 3000000 # Replace with the desired baud rate
count = 0
list_read_data = []
with serial.Serial(port, baudrate=baudrate,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS) as ser:
   can_open(ser)
   # with open('read_data.txt','wb') as f:
   #     while True:
   #         count +=1
   #         read_data = ser.read(100)
   #         read_data = read_data.replace(b'\r',b'\n')
   #         if b'033' in read_data and b'002F0000' in read_data:
   #             list_read_data = read_data.split(b'\n')
   #             for i in list_read_data:
   #                 if b'033' in i and b'002F0000' in i:
   #                     read_data = i
   #                     value = read_data[15:21]
   #             print(read_data)
   #             print(value)
   #             break
   can_close(ser)

b=b't0338002F00000000D4BF0CC3'
# b = b't0088EB2E0000245600000380\nt0338002F00000000D4BF03E7\nt0338002F00000000D4BF03E8\nt0338002F00000000D4BF0'
b = b[13:21]
print(b)
b = b[6:8]+b[4:6]+b[2:4]+b[0:2]
b = b.decode('utf-8')
print(b)
import  struct
b = struct.unpack('i', bytes.fromhex(b))
print(b)

# a = b'A8\r'
# # a = a.lstrip(b'\r')
# a =a.replace(b'\r',b'\n')
# print(a)





