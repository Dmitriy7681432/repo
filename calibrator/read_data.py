import serial, time, binascii, struct
import serial.tools.list_ports
from lxml import etree
from debug import printf


def can_open(arg):
    arg.timeot = 0.1
    msg = b"C\r"
    arg.write(msg)
    # printf("T>", msg)
    # print("R>", arg.read(1000))
    msg = b"S5\rZ1\r"
    arg.write(msg)
    # printf("T>", msg)
    # print("R>", arg.read(1000))
    msg = b"L\r"
    arg.write(msg)
    return 0


def can_close(arg):
    msg = b"C\r"
    printf(msg, 'can_close')
    arg.write(msg)
    return 0


def transformed_in_value(arg):
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
                    printf(number)
                    arg += 4


# ports = serial.tools.list_ports.comports()
#
# for port in ports:
#     print(port.device)

def main():
    port = "COM88"  # Replace with the appropriate COM port name
    baudrate = 3000000  # Replace with the desired baud rate
    count = 0
    list_read_data = []
    value = 0
    with serial.Serial(port, baudrate=baudrate, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS) as ser:
        can_open(ser)
        while True:
            read_data = ser.read(100)
            read_data = read_data.replace(b'\r', b'\n')
            if b'033' in read_data and b'002F0000' in read_data:
                list_read_data = read_data.split(b'\n')
                for i in list_read_data:
                    if b'033' in i and b'002F0000' in i and len(i) > 21:
                        read_data = i
                        value = transformed_in_value(read_data)
                        printf(read_data)
                        printf(value)
                        break
                break

        with open('read_data.txt', 'wb') as f:
            while True:
                msg_bytes = transformed_in_bytes(value)
                value+=4
                count +=1
                printf(msg_bytes)
                f.write(msg_bytes+b'\n')
                ser.write(msg_bytes)
                # time.sleep(1)
                while True:
                    read_data = ser.read(100)
                    read_data = read_data.replace(b'\r', b'\n')
                    if b't64A' in read_data:
                        list_read_data = read_data.split(b'\n')
                        for i in list_read_data:
                            if i[1:4] == b'64A' in i and len(i) > 21:
                                read_data = i
                                printf(read_data)
                                f.write(read_data+b'\n')
                                address = transformed_in_value(read_data)
                                print(address)
                                f.write(hex(address).encode('utf-8')+b'\n')
                                break
                        break
                if count ==7: break
            doc = etree.parse('params.xml')
            for setting in doc.findall('.//setting'):
                number = setting.attrib.get('number')
                for products in setting.findall('products/'):
                    product = products.tag
                    if product == 'SES200M':
                        cb = products.attrib.get('cb')
                        if cb == 'BU_50':
                            printf(number)
                            msg_bytes = transformed_in_bytes(value)
                            value += 4
                            printf(msg_bytes)
                            f.write(msg_bytes+b'\n')
                            ser.write(msg_bytes)
                            # time.sleep(1)
                            while True:
                                # can_open(ser)
                                msg = b"L\r"
                                ser.write(msg)
                                read_data = ser.read(100)
                                read_data = read_data.replace(b'\r', b'\n')
                                if b't64A' in read_data:
                                    list_read_data = read_data.split(b'\n')
                                    for i in list_read_data:
                                        if i[1:4] == b'64A' and len(i) > 21:
                                            read_data = i
                                            printf(read_data)
                                            f.write(read_data+b'\n')
                                            address = transformed_in_value(read_data)
                                            printf(address)
                                            f.write(hex(address).encode('utf-8')+b'\n')
                                            break
                                    break

        can_close(ser)

if __name__ == '__main__':
    main()
# b = b't64A8E400000000E500009'
# print(len(b))

# b = b't0338002F00000000D4BF0CC3'
# b = transformed_in_value(b)
# print(b)
# printf(hex(b[0]))
# b = transformed_in_value(b)
# b = hex(b).encode('utf-8')
# printf(b)
# with open('read_data.txt', 'wb') as f:
#     f.write(b)


# a = b'A8\r'
# # a = a.lstrip(b'\r')
# a =a.replace(b'\r',b'\n')
# print(a)
