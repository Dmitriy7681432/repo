import serial, time, binascii, struct
import serial.tools.list_ports
from lxml import etree
from debug import printf

class Calibrator(object):

    # Инициализация входных данных
    def __init__(self,product, control_block):
        self.product = product
        self.control_block = control_block
        self.preset_addr = 0xBFD40000
        self.calibr_addr = 0xBFD42000
        self.filter_addr = 0xBFD44000
        if self.product =="SES200M":
            if self.control_block == 'BU_SES':
                self.read_id = b't60E8'
                self.data_id = b't640'
            elif self.control_block == 'BU_50':
                self.read_id = b't6188'
                self.data_id = b't64A'
        # Поиск устройства
        ports = serial.tools.list_ports.comports()
        for port in ports:
            print(port.device)
            port = port.device
        self.ser = serial.Serial(port =port,baudrate=3000000,timeout=0.1)

    # Выбор режима com_port
    def can_open_O(self,arg):
        printf('can_open')
        arg.timeot = 0.1
        msg = b"C\r"
        arg.write(msg)
        msg = b"S5\rZ1\r"
        arg.write(msg)
        msg = b"O\r"
        arg.write(msg)

    # Закрытие com_port
    def can_close(self,arg):
        printf('can_close')
        msg = b"C\r"
        arg.write(msg)

    # Преобразование байтового типа в тип целочисленного значения и адреса
    def transformed_in_value_and_address(self,arg):
        value = arg[13:21]
        value = value[6:8] + value[4:6] + value[2:4] + value[0:2]
        value = value.decode('utf-8')
        value = struct.unpack('!I', bytes.fromhex(value))
        address = arg[5:13]
        address = address[6:8] + address[4:6] + address[2:4] + address[0:2]
        address = address.decode('utf-8')
        address = struct.unpack('!I', bytes.fromhex(address))
        return value,address

    # Преобразование целочисленного значения в байтовый тип формата can
    def transformed_in_bytes(self,arg):
        # read_id = b't' + hex(self.read_id).upper().encode('utf-8')[2:] + b'8'
        arg = hex(arg)[2:].upper()
        arg = arg[6:8] + arg[4:6] + arg[2:4] + arg[0:2]
        arg = arg.encode('utf-8')
        arg = self.read_id +arg+b'00000000'+ b'\r'
        return arg

    def _header_data_write(self,addr):
        count = 0
        flag = 0
        self.file_open = open('read_data.txt','wb')
        while True:
            msg_bytes = self.transformed_in_bytes(addr)
            addr += 4
            count += 1
            printf(msg_bytes)
            self.ser.write(msg_bytes)
            while True:
                read_data = self.ser.read(1024)
                if self.data_id in read_data:
                    list_read_data = read_data.split(b'\r')
                    for i in list_read_data:
                        if i[0:4] == self.data_id in i and len(i) > 21:
                            read_data = i
                            printf(read_data)
                            can_value,can_address = self.transformed_in_value_and_address(read_data)
                            print(can_value)
                            print(can_address)
                            self.file_open.write(hex(can_address).encode('utf-8') + b'\t')
                            self.file_open.write(hex(can_value).encode('utf-8') + b'\n')
                            flag = 1
                            break
                    if flag == 1:
                        flag = 0;break
            if count == 7: count = 0;break
        return addr
