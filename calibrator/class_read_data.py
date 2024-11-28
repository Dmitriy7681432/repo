# -*- coding: utf-8 -*-
import serial, time, binascii, struct
import serial.tools.list_ports
from lxml import etree
from debug import printf


class Connect(object):
    def __init__(self):
        # Поиск устройства
        # ports = serial.tools.list_ports.comports()
        # for port in ports:
        #     print(port.device)
        #     port = port.device
        # self.ser = serial.Serial(port =port,baudrate=3000000,timeout=0.1)
        self.ser = serial.Serial(port='COM88', baudrate=3000000, timeout=0.1)
        self.can_open_O(self.ser)

    # Выбор режима com_port
    def can_open_O(self, arg):
        printf('can_open')
        arg.timeot = 0.1
        msg = b"C\r"
        arg.write(msg)
        msg = b"S5\rZ1\r"
        arg.write(msg)
        msg = b"O\r"
        arg.write(msg)

    # Закрытие com_port
    def can_close(self, arg):
        printf('can_close')
        msg = b"C\r"
        arg.write(msg)
        arg.close()


class Calibrator(Connect):

    # Инициализация входных данных
    def __init__(self, product, control_block):
        self.product = product
        self.control_block = control_block
        if self.product == "SES200M":
            if self.control_block == 'BU_SES':
                self.partel_id = b't0328'
                self.read_id = b't60E8'
                self.data_id = b't640'
                self.preset_designation = 'ADDR_PRESET_ROM'
                self.calibr_designation = 'ADDR_CALIBR_ROM'
                self.filter_designation = 'ADDR_FILTR_ROM'
            elif self.control_block == 'BU_50':
                self.partel_id = b't0338'
                self.read_id = b't6188'
                self.data_id = b't64A'
                self.preset_designation = 'ADDR_PRESET_ROM2'
                self.calibr_designation = 'ADDR_CALIBR_ROM2'
                self.filter_designation = 'ADDR_FILTR_ROM2'
            elif self.control_block == "BU_400":
                self.partel_id = b't0348'
                self.read_id = b't6228'
                self.data_id = b't654'
                self.preset_designation = 'ADDR_PRESET_ROM3'
                self.calibr_designation = 'ADDR_CALIBR_ROM3'
                self.filter_designation = 'ADDR_FILTR_ROM3'
        # Считывание,преобразование global_id параметров в формaт can и сохранение их в списке
        self.data_can_list = []
        preset_data_can = self.parse_xml_designation(self.preset_designation)
        calibr_data_can = self.parse_xml_designation(self.calibr_designation)
        filter_data_can = self.parse_xml_designation(self.filter_designation)
        self.data_can_list.append(preset_data_can)
        self.data_can_list.append(calibr_data_can)
        self.data_can_list.append(filter_data_can)

        self.file_open = open('read_data.txt', 'wb')

    # Преобразование байтового типа в тип целочисленного значения и адреса
    def transformed_in_value_and_address(self, arg):
        value = arg[13:21]
        value = value[6:8] + value[4:6] + value[2:4] + value[0:2]
        value = value.decode('utf-8')
        value = struct.unpack('!I', bytes.fromhex(value))
        address = arg[5:13]
        address = address[6:8] + address[4:6] + address[2:4] + address[0:2]
        address = address.decode('utf-8')
        address = struct.unpack('!I', bytes.fromhex(address))
        return value[0], address[0]

    # Преобразование целочисленного значения в байтовый тип формата can
    def transformed_in_bytes(self, arg, id):
        # read_id = b't' + hex(self.read_id).upper().encode('utf-8')[2:] + b'8'
        arg = hex(arg)[2:].upper()
        arg = arg[6:8] + arg[4:6] + arg[2:4] + arg[0:2]
        arg = arg.encode('utf-8')
        arg = id + arg + b'000000000000' + b'\r'
        return arg

    # Перевод числа из hex в decimal
    def transformed_hex_to_dec(self, value, type):
        if type == "float":
            value = struct.unpack('!f', bytes.fromhex(value))
            return value[0]
        elif type == 'int':
            value = struct.unpack('!f', bytes.fromhex(value))
            return value[0]
        return value

    # Считывание global_id параметра с params.xml
    def parse_xml_designation(self, designation):
        doc = etree.parse('params.xml')
        for setting in doc.findall('.//parameter'):
            designation_get = setting.attrib.get('designation')
            if designation_get == designation:
                global_id = int(setting.attrib.get('common_id'))
                global_id_can_format = self.transformed_in_bytes(global_id, self.partel_id)
        return global_id_can_format

    # Считывание адреса по global_id параметра
    def _begin_data_read(self, data_can):
        while True:
            read_data = self.ser.read(1024)
            if data_can[:12] in read_data:
                list_read_data = read_data.split(b'\r')
                for i in list_read_data:
                    if data_can[:12] in read_data and len(i) > 21:
                        read_data = i
                        value, address = self.transformed_in_value_and_address(read_data)
                        return address

    def _header_data_read(self, data_can):
        count = 0
        flag = 0
        addr = self._begin_data_read(data_can)
        while True:
            msg_bytes = self.transformed_in_bytes(addr, self.read_id)
            addr += 4
            count += 1
            printf(msg_bytes)
            self.ser.write(msg_bytes)
            while True:
                read_data = self.ser.read(1024)
                if self.data_id in read_data:
                    list_read_data = read_data.split(b'\r')
                    for i in list_read_data:
                        if i[:4] == self.data_id in i and len(i) > 21:
                            read_data = i
                            printf(read_data)
                            value, address = self.transformed_in_value_and_address(read_data)
                            print(value)
                            print(address)
                            self.file_open.write(hex(address).encode('utf-8') + b'\t')
                            self.file_open.write(hex(value).encode('utf-8') + b'\n')
                            flag = 1
                            break
                    if flag == 1: flag = 0;break
            if count == 7: count = 0;break
        return addr

    # Считывание уставок, калибровок, и сохранение их в списки
    def parse_data_xml(self):
        preset_list_data = []
        calibr_list_data = []
        doc = etree.parse('params.xml')
        # Уставки
        for setting in doc.findall('.//setting'):
            number = setting.attrib.get('number')
            c_type = setting.attrib.get('ctype')
            designation = setting.attrib.get('designation')
            for products in setting.findall('products/'):
                product = products.tag
                if product == self.product:
                    cb = products.attrib.get('cb')
                    if cb == self.control_block:
                        preset_list_data.append(number)
                        preset_list_data.append(designation)
                        # preset_list_data.append(c_type)
        # Калибровки
        for setting in doc.findall('.//parameter'):
            designation = setting.attrib.get('designation')
            name = setting.attrib.get('name')
            for products1 in setting.findall(f'.//{self.product}'):
                cb = products1.attrib.get('cb')
                if cb == self.control_block:
                    for products2 in products1.findall('.//calibration'):
                        if len(products2.getchildren()) != 0:
                            for i in products2.findall('.//k'):
                                calibr_list_data.append(designation + '_' + i.attrib.get('IND'))
                                calibr_list_data.append(name)
                                # calibr_list_data.append(i.attrib.get('value'))
                        else:
                            calibr_list_data.append(designation + '_k')
                            calibr_list_data.append(name)
                            # calibr_list_data.append('1.0')
                            calibr_list_data.append(designation + '_b')
                            calibr_list_data.append(name)
                            # calibr_list_data.append('1.0')
        return preset_list_data,calibr_list_data

    def main_data_read(self):
        for data_can in self.data_can_list:
            count = 0
            addr = self._header_data_read(data_can)
            doc = etree.parse('params.xml')
            for setting in doc.findall('.//setting'):
                number = setting.attrib.get('number')
                ctype = setting.attrib.get('ctype')
                for products in setting.findall('products/'):
                    product = products.tag
                    if product == self.product:
                        cb = products.attrib.get('cb')
                        if cb == self.control_block:
                            while True:
                                count += 1
                                if count > 4: count = 0;break
                                printf(number)
                                msg_bytes = self.transformed_in_bytes(addr, self.read_id)
                                addr += 4
                                printf(msg_bytes)
                                self.ser.write(msg_bytes)
                                while True:
                                    read_data = self.ser.read(1024)
                                    if self.data_id in read_data:
                                        list_read_data = read_data.split(b'\r')
                                        for i in list_read_data:
                                            if i[:4] == self.data_id and len(i) > 21:
                                                read_data = i
                                                printf(read_data)
                                                value, address = self.transformed_in_value_and_address(read_data)
                                                value_dec = self.transformed_hex_to_dec(value, ctype)
                                                printf(value)
                                                self.file_open.write(hex(address).encode('utf-8') + b'\t')
                                                self.file_open.write(hex(value).encode('utf-8') + b'\t')
                                                self.file_open.write(hex(value_dec).encode('utf-8') + b'\n')
                                                flag = 1
                                                break
                                        if flag == 1: flag = 0; break
        self.file_open.close()
        return 'End main_data_read'


cal = Calibrator('SES200M', 'BU_SES')
cal1 = Calibrator('SES200M', 'BU_50')
cal2 = Calibrator('SES200M', 'BU_400')
# a = b't0328FF2E00000000D4BF\r'
# b, c = cal.transformed_in_value_and_address(a)
# print(b)
# print(c)
a,b = cal1.parse_data_xml()
print(a)
print(b)