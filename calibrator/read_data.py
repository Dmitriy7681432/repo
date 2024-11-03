import serial,time,binascii,struct
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

def trasformed_in_value(arg):
    arg = arg[13:21]
    arg = arg[6:8]+arg[4:6]+arg[2:4]+arg[0:2]
    arg = arg.decode('utf-8')
    arg = struct.unpack('!I', bytes.fromhex(arg))
    return arg[0]

def transformed_in_bytes(arg):
    arg= hex(arg)[2:].upper()
    arg = arg[6:8] + arg[4:6] + arg[2:4] + arg[0:2]
    arg = arg.encode('utf-8')
    arg = b't64A800000000' + arg
    return arg
# ports = serial.tools.list_ports.comports()
#
# for port in ports:
#     print(port.device)

port = "COM88"  # Replace with the appropriate COM port name
baudrate = 3000000 # Replace with the desired baud rate
count = 0
list_read_data = []
# with serial.Serial(port, baudrate=baudrate,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS) as ser:
#    can_open(ser)
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
   # can_close(ser)


b=b't0338002F00000000D4BF0CC3'
print(hex(b[0]))
b = trasformed_in_value(b)
print(b)
while count <20:
    count += 1
    b +=4
    a = transformed_in_bytes(b)
    print(a)

# a = b'A8\r'
# # a = a.lstrip(b'\r')
# a =a.replace(b'\r',b'\n')
# print(a)





