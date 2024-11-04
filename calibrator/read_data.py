import serial, time, binascii, struct
import serial.tools.list_ports
from lxml import etree


def can_open(arg):
    arg.timeot = 0.01
    msg = b"C\r"
    arg.write(msg)
    print("T>", msg)
    # print("R>", arg.read(1000))
    msg = b"S5\rZ1\r"
    arg.write(msg)
    print("T>", msg)
    # print("R>", arg.read(1000))
    msg = b"L\r"
    arg.write(msg)
    return 0


def can_close(arg):
    msg = b"C\r"
    arg.write(msg)
    print(msg, 'can_close')
    return 0


def trasformed_in_value(arg):
    arg = arg[13:21]
    arg = arg[6:8] + arg[4:6] + arg[2:4] + arg[0:2]
    arg = arg.decode('utf-8')
    arg = struct.unpack('!I', bytes.fromhex(arg))
    return arg[0]


def transformed_in_bytes(arg):
    arg = hex(arg)[2:].upper()
    arg = arg[6:8] + arg[4:6] + arg[2:4] + arg[0:2]
    arg = arg.encode('utf-8')
    arg = b't618800000000' + arg
    return arg


def parse_preset(xmlFile, arg):
    value = 0
    doc = etree.parse(xmlFile)
    for setting in doc.findall('.//can'):
        number = setting.attrib.get('number')
        for products in setting.findall('products/'):
            product = products.tag
            if product == 'SES200M':
                cb = products.attrib.get('cb')
                if cb == 'BU_50':
                    print(number)
                    arg += 4


# ports = serial.tools.list_ports.comports()
#
# for port in ports:
#     print(port.device)

port = "COM88"  # Replace with the appropriate COM port name
baudrate = 3000000  # Replace with the desired baud rate
count = 0
list_read_data = []
with serial.Serial(port, baudrate=baudrate, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS) as ser:
    can_open(ser)
    while True:
        read_data = ser.read(100)
        read_data = read_data.replace(b'\r', b'\n')
        if b'033' in read_data and b'002F0000' in read_data:
            list_read_data = read_data.split(b'\n')
            for i in list_read_data:
                if b'033' in i and b'002F0000' in i:
                    read_data = i
                    value = trasformed_in_value(read_data)
                    print(read_data)
                    print(value)
                    break
        break

    with open('read_data.txt', 'wb') as f:
        doc = etree.parse('params.xml')
        for setting in doc.findall('.//setting'):
            number = setting.attrib.get('number')
            for products in setting.findall('products/'):
                product = products.tag
            if product == 'SES200M':
                cb = products.attrib.get('cb')
            if cb == 'BU_50':
                print(number)
                value += 4
                msg_bytes = transformed_in_bytes(value)
                print(msg_bytes)
                f.write(msg_bytes)
                ser.write(msg_bytes)
                time.sleep(1)
                while True:
                    read_data = ser.read(100)
                    read_data = read_data.replace(b'\r', b'\n')
                    if b'64A' in read_data:
                        list_read_data = read_data.split(b'\n')
                        for i in list_read_data:
                            if b'64A' in i:
                                read_data = i
                                f.write(read_data)
                                value = trasformed_in_value(read_data)
                                f.write(hex(value).encode('utf-8'))
                                break
                break

    can_close(ser)

b = b't0338002F00000000D4BF0CC3'
print(hex(b[0]))
b = trasformed_in_value(b)
b = hex(b).encode('utf-8')
print(b)
with open('read_data.txt', 'wb') as f:
    f.write(b)


# a = b'A8\r'
# # a = a.lstrip(b'\r')
# a =a.replace(b'\r',b'\n')
# print(a)
