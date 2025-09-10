# -*- coding: utf-8 -*-
import serial, time, binascii, struct
import serial.tools.list_ports
from lxml import etree
# from debug import print
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot,QTimer,QObject
import serial.tools.list_ports
import warning
from PyQt5.QtCore import QAbstractEventDispatcher
from PyQt5.QtWidgets import QApplication
import sys,json
from debug import *


class Connect():
    # ser = serial.Serial()
    # com_port = ComPort()
    wait_receiv = 0
    buffer_receiv_begin = 0
    buffer_receiv_main = 0

    # Инфа про доступные com_port
    ports = serial.tools.list_ports.comports()
    # Открытие configs
    with open('configs.json','r') as file_configs:
        configs = json.load(file_configs)

    # Поиск com_port
    ports_lst = []
    for port in ports:
        print(port.hwid,port.name,port.vid,port.pid,port.serial_number,port.location,port.manufacturer,port.product,port.interface)
        for i in configs.values():
            if i in port.serial_number:
                ports_lst.append(port.name)
    print(ports_lst)
    # Поиск элементов configs, кроме com_port
    for i in configs.keys():
        if i == 'wait_receiv':
            wait_receiv = int(configs.get(i))
        if i == 'buffer_receiv_begin':
            buffer_receiv_begin = int(configs.get(i))
        if i == 'buffer_receiv_main':
            buffer_receiv_main = int(configs.get(i))
    try:
        if 'lin' in sys.platform:
            ser = serial.Serial(port=f'/dev/{ports_lst[0]}', baudrate=3000000, timeout=0.01)
        else:
            ser = serial.Serial(port=ports_lst[0], baudrate=3000000, timeout=0.01)
    except IndexError:
        print('ERROR')
        warning.SignalErr(True)


    # ser = serial.Serial()
    def __init__(self,com_port):
        super().__init__()
        # self.ser = serial.Serial(port=com_port, baudrate=3000000, timeout=0.01)
        # self.com_port = com_port
        # print(com_port)
        # self.ser.port = com_port
        # print(com_port)
        # self.ser.baudrate = 3000000
        # print(com_port)
        # self.ser.timeout = 0.1
        # print(com_port)

    # Выбор режима com_port
    def can_open_O(self, arg):
        print('can_open_O')
        arg.timeot = 0.01
        msg = b"C\r"
        arg.write(msg)
        msg = b"S5\rZ1\r"
        arg.write(msg)
        msg = b"O\r"
        arg.write(msg)
        # msg = b"F\r"
        # arg.write(msg)
        # print(arg.read(1024))

    def can_open_L(self, arg):
        print('can_open_L')
        arg.timeot = 0.01
        msg = b"C\r"
        arg.write(msg)
        msg = b"S5\rZ1\r"
        arg.write(msg)
        msg = b"L\r"
        arg.write(msg)

    # Закрытие com_port
    def can_close(self, arg):
        print('can_close')
        msg = b"C\r"
        arg.write(msg)
        # После закрытия необходимо заново инициалировать serial
        # arg.close()


class Calibrator(QObject):
    cal_signal = pyqtSignal(int)
    finish_cal_signal = pyqtSignal()
    flag_abort = 0

    # Инициализация входных данных
    def __init__(self, ser, product, control_block):
        super().__init__()
        # self.thread_cal = QThread()
        # self.thread_cal.start()
        # self.timer = QTimer()
        self.ser = ser
        self.product = product
        self.control_block = control_block
        if self.product == "SES200M":
            if self.control_block == 'BU_SES':
                # self.partel_id = b't0328'       # purpose="PARAMETER_VALUE_FOR_OPERATOR">
                # self.read_id = b't60E8'         # READ_DATA
                # self.data_id = b't640'          # DATA_VALUE
                # self.write_id = b't60F8'        # WRITE_DATA
                # self.confirmation_id = b't014'  # CONFIRMATION_OPERATOR
                # self.erase_id = b't6108'        # ERASE_SECTOR
                self.preset_designation = 'ADDR_PRESET_ROM'
                self.calibr_designation = 'ADDR_CALIBR_ROM'
                self.filter_designation = 'ADDR_FILTR_ROM'
            elif self.control_block == 'BU_50':
                # self.partel_id = b't0338'
                # self.read_id = b't6188'
                # self.data_id = b't64A'
                # self.write_id = b't6198'
                # self.confirmation_id = b't015'
                # self.erase_id = b't61A8'
                self.preset_designation = 'ADDR_PRESET_ROM2'
                self.calibr_designation = 'ADDR_CALIBR_ROM2'
                self.filter_designation = 'ADDR_FILTR_ROM2'
            elif self.control_block == "BU_400":
                # self.partel_id = b't0348'
                # self.read_id = b't6228'
                # self.data_id = b't654'
                # self.write_id = b't6238'
                # self.confirmation_id = b't016'
                # self.erase_id = b't6248'
                self.preset_designation = 'ADDR_PRESET_ROM3'
                self.calibr_designation = 'ADDR_CALIBR_ROM3'
                self.filter_designation = 'ADDR_FILTR_ROM3'
        if self.product == "SEP30M":
            if self.control_block == 'BU_SEP':
                # self.partel_id = b't0328'
                # self.read_id = b't60E8'
                # self.data_id = b't640'
                # self.write_id = b't60F8'
                # self.confirmation_id = b't014'
                # self.erase_id = b't6108'
                self.preset_designation = 'ADDR_PRESET_ROM'
                self.calibr_designation = 'ADDR_CALIBR_ROM'
                self.filter_designation = 'ADDR_FILTR_ROM'
            elif self.control_block == 'BU_400':
                # self.partel_id = b't0408'
                # self.read_id = b't6188'
                # self.data_id = b't64A'
                # self.write_id = b't6198'
                # self.confirmation_id = b't015'
                # self.erase_id = b't61A8'
                self.preset_designation = 'ADDR_PRESET_ROM2'
                self.calibr_designation = 'ADDR_CALIBR_ROM2'
                self.filter_designation = 'ADDR_FILTR_ROM2'

        self.parse_xml_can_id(self.product,self.control_block)

        # Главный словарь с уставками, калибровками и фильтрами для интерфейса
        self.data_dict = {'preset': {}, 'calibr': {}, 'filter': {}}
        # Словарь с параметрами для вкладки Параметры для интерфейса
        self.param_dict = {f'{self.control_block}': {}}
        # Считывание,преобразование global_id параметров в формaт can и сохранение их в словарь
        self.data_can_dict = {'preset': '', 'calibr': '', 'filter': ''}
        self.data_can_dict['preset'] = self.parse_xml_designation(self.preset_designation)
        self.data_can_dict['calibr'] = self.parse_xml_designation(self.calibr_designation)
        self.data_can_dict['filter'] = self.parse_xml_designation(self.filter_designation)
        # Заполение главного словаря данными
        self.parse_data_xml()

        self.file_open = open('read_data.txt', 'wb')
        self.flag =0

        print('wait_receiv', self.ser.wait_receiv)
        print('buffer_beg', self.ser.buffer_receiv_begin)
        print('buffer_main', self.ser.buffer_receiv_main)

    def transformed_in_value_and_address(self, arg, type,func=None):
        lst_val = []
        value = arg[13:21]
        value = value[6:8] + value[4:6] + value[2:4] + value[0:2]
        print('val',value)
        value = value.decode('utf-8')
        if type == 'int' and func =='header':
            print(value)
            value = binascii.unhexlify(value)
            print(value)
            value = int.from_bytes(value, 'big', signed=True)
            print(value)
            # value = struct.unpack('!I', bytes.fromhex(value))
            value = [bytearray(value.to_bytes(length=4, byteorder="little",signed=True))]
        elif type =='int':
            value = struct.unpack('!I', bytes.fromhex(value))
        elif type =='-int':
            value = [self.trans_neg_hex_to_dec(value)]
            print('val1',value)
            # value = struct.unpack('!I', bytes.fromhex(value))
        else:
            value = struct.unpack('!f', bytes.fromhex(value))
            lst_val.append(round(value[0],6))
            value = lst_val.copy()
        address = arg[5:13]
        address = address[6:8] + address[4:6] + address[2:4] + address[0:2]
        address = address.decode('utf-8')
        address = struct.unpack('!I', bytes.fromhex(address))
        return value[0], address[0]

    def func_val_to_hex_can(self,c):
        print(c)
        c = int(c)
        print(c)
        c = hex(c)[2:].upper()
        print(c)
        if len(c) == 1:
            print(type(c),c)
            c = '0' + c + "000000"
            print(c)
        elif len(c) == 2:
            c = c + "000000"
        elif len(c) == 4:
            c = c[len(c) - 2:] + "  " + \
                c[len(c) - 4:len(c) - 2] + "0000"
        elif len(c) == 6:
            c = c[len(c) - 2:] + "  " + \
                c[len(c) - 4:len(c) - 2] + "  " + c[len(c) - 6:len(c) - 4] + "00"
        elif len(c) == 8:
            c = c[len(c) - 2:] + "  " + \
                c[len(c) - 4:len(c) - 2] + "  " + c[len(c) - 6:len(c) - 4] + "  " + c[len(c) - 8:len(c) - 6]
        return c

    # Преобразование целочисленного значения в байтовый тип формата can
    def transformed_in_bytes(self, arg, id, val=b'000000000000',header =False):
        # read_id = b't' + hex(self.read_id).upper().encode('utf-8')[2:] + b'8'
        if val != b'000000000000':
            if header:
                val = int.from_bytes(val, 'little', signed=False)
                print(val,type(val))
                val = hex(val)[2:].upper()
                print(val)
                val = val[6:8] + val[4:6] + val[2:4] + val[0:2]
                print(val)
            else:
                print()
                val = self.func_val_to_hex_can(val)
                print(type(val),val)
            val = val.encode('utf-8') + b'0000'
            print(val)

        # print(arg)
        arg = hex(arg)[2:].upper()
        # print(arg)
        arg = arg[6:8] + arg[4:6] + arg[2:4] + arg[0:2]
        # print(arg)
        arg = arg.encode('utf-8')
        arg = id + arg + val + b'\r'
        return arg

    def transformed_in_bytes_can_id(self,arg):
        arg = hex(arg)[2:].upper()
        arg = arg.encode('utf-8')
        if len(arg) == 1: arg = b't00' + arg + b'8'
        elif len(arg) == 2: arg = b't0' + arg + b'8'
        else: arg = b't' + arg + b'8'
        return arg


    # Перевод числа из hex в decimal
    def transformed_hex_to_dec(self, value, type):
        if type == "float":
            value = struct.unpack('!f', bytes.fromhex(str(value)))
            return value[0]
        elif type == 'int':
            print(value)
            value = struct.unpack('!f', bytes.fromhex(str(value)))
            return value[0]
        return value

    def trans_neg_hex_to_dec(self,arg):
        arg = '0x' + arg
        arg = int(arg, 16)
        t = bin(arg)
        s = str.maketrans('01', '10')
        s1 = t[2:].translate(s)
        s2 = (int(s1, 2) + 1) * -1
        # print(s2+1)
        return s2

    # Считывание global_id параметра с params.xml
    def parse_xml_designation(self, designation):
        self.product_lower = self.product.lower()
        doc = etree.parse(f'params_{self.product_lower}.xml')
        for setting in doc.findall('.//parameter'):
            designation_get = setting.attrib.get('designation')
            if designation_get == designation:
                global_id = int(setting.attrib.get('common_id'))
                global_id_can_format = self.transformed_in_bytes(global_id, self.partel_id)
        # Пример возвращаемого значения: b't0338002F000000000000\r'
        return global_id_can_format

    # Считывание can_id с params.xml
    def parse_xml_can_id(self,name_product,name_cb):
        lst_can_id = []
        self.product_lower = self.product.lower()
        doc = etree.parse(f'params_{self.product_lower}.xml')
        for setting in doc.findall('.//can'):
            purpose = setting.attrib.get('purpose')
            for products1 in setting.findall(f'.//{name_product}'):
                cb = products1.attrib.get('cb')
                if cb == name_cb:
                    if purpose =="PARAMETER_VALUE_FOR_OPERATOR":
                        self.partel_id = self.transformed_in_bytes_can_id(int(products1.attrib.get('value')))
                        print('partel_id',self.partel_id)
                    if purpose == "READ_DATA":
                        self.read_id = self.transformed_in_bytes_can_id(int(products1.attrib.get('value')))
                        print('read_id', self.read_id)
                    if purpose == "DATA_VALUE":
                        self.data_id = self.transformed_in_bytes_can_id(int(products1.attrib.get('value')))[:-1]
                        print('data_id', self.data_id)
                    if purpose == "WRITE_DATA":
                        self.write_id = self.transformed_in_bytes_can_id(int(products1.attrib.get('value')))
                        print('write_id', self.write_id)
                    if name_product =='SES200M' or name_product =='SES150':
                        if purpose == "CONFIRMATION_OPERATOR":
                            self.confirmation_id = self.transformed_in_bytes_can_id(int(products1.attrib.get('value')))[:-1]
                            printf('confirmation_id', self.confirmation_id)
                    else:
                        if purpose == "CONFIRMATION":
                            self.confirmation_id = self.transformed_in_bytes_can_id(int(products1.attrib.get('value')))[:-1]
                            printf('confirmation_id', self.confirmation_id)
                    if purpose == "ERASE_SECTOR":
                        self.erase_id = self.transformed_in_bytes_can_id(int(products1.attrib.get('value')))
                        printf('erase_id', self.erase_id)

                        # Считывание уставок, калибровок, фильтров и сохранение их в списки
    def parse_data_xml(self):
        start = time.time()
        flag = 0
        preset_dict = {}
        calibr_dict = {}
        filter_dict = {}
        params_dict = {}
        self.product_lower = self.product.lower()
        doc = etree.parse(f'params_{self.product_lower}.xml')
        # Уставки
        for setting in doc.findall('.//setting'):
            number = setting.attrib.get('number')
            c_type = setting.attrib.get('ctype')
            min = setting.attrib.get('min')
            default_value = setting.attrib.get('default_value')
            max = setting.attrib.get('max')
            dimension = setting.attrib.get('dimension')
            designation = setting.attrib.get('designation')
            for products in setting.findall('products/'):
                product = products.tag
                if product == self.product:
                    cb = products.attrib.get('cb')
                    if cb == self.control_block and '-' in default_value and c_type =='int':
                        preset_dict[number] = [designation, '-'+ c_type,dimension,min,default_value,default_value,max]
                    elif cb == self.control_block:
                        preset_dict[number] = [designation, c_type,dimension,min,default_value,default_value,max]

        # Калибровки
        for setting in doc.findall('.//parameter'):
            designation = setting.attrib.get('designation')
            name = setting.attrib.get('name')
            type = setting.attrib.get('type')
            ctype = setting.attrib.get('ctype')
            for products1 in setting.findall(f'.//{self.product}'):
                cb = products1.attrib.get('cb')
                hidden = products1.attrib.get('hidden')
                if cb == self.control_block and hidden == None:
                    if type == 'Измеряемый' or type == 'Вычисляемый':
                        unit = setting.getparent().attrib.get('name')
                        if flag == 0:
                            # unit1 = self.pars_eskd(unit)
                            unit1 = unit
                            params_dict[unit1] ={}
                            flag = 1
                        else:
                            if unit1 != unit:
                                unit1 = unit
                                # unit1 = self.pars_eskd(unit)
                                params_dict[unit1] = {}
                        params_dict[unit1][designation] = [name,ctype]
                if cb ==self.control_block:
                    for products2 in products1.findall('.//calibration'):
                        if len(products2.getchildren()) != 0:
                            for i in products2.findall('.//k'):
                                calibr_dict[designation + '_' + i.attrib.get('IND')] = [name,i.attrib.get('value')]
                                # calibr_list_data.append(i.attrib.get('value'))
                        else:
                            calibr_dict[designation + '_k'] = [name,'1.0']
                            calibr_dict[designation + '_b'] = [name,'0.0']
                            # calibr_list_data.append('1.0')
                            # calibr_list_data.append('1.0')
                # Фильтры
                if cb == self.control_block:
                    for products2 in products1.findall('.//filter'):
                        # filter_dict[designation + '_FILTER'] = [products2.attrib.get('length')]
                        # filter_dict[designation + '_FILTER'] = [products2.attrib.get('length')]
                        filter_dict[designation + '_FILTER'] = []
                        filter_dict[designation + '_FILTER'] = []
        self.data_dict['preset'] = preset_dict
        self.data_dict['calibr'] = calibr_dict
        self.data_dict['filter'] = filter_dict
        self.param_dict[self.control_block] = params_dict
        # printf(self.param_dict)
        self.pars_eskd()
        end = time.time()
        # print(end - start)
        flag = 0
        return self.data_dict

    def pars_eskd(self):
        self.product_lower = self.product.lower()
        doc = etree.parse(f'params_{self.product_lower}.xml')
        for eskd in doc.findall('.//system_parts/'):
            product = eskd.getparent().getparent().tag
            units = eskd.tag
            if product ==self.product:
                for i in self.param_dict[self.control_block].keys():
                    if units ==i:
                        self.param_dict[self.control_block][eskd.text] = self.param_dict[self.control_block].pop(i)
                        break
        #printf(self.param_dict)

            # if product==self.product and units==unit:
            #     return eskd.text

    # Считывание адреса по global_id параметра
    def _begin_data_read(self, data_can_dict_value):
        tmp_cnt =0
        cnt_ports =0
        while True:
            tmp_cnt+=1
            read_data = self.ser.ser.read(self.ser.buffer_receiv_begin)
            # Костыль
            if tmp_cnt >=self.ser.wait_receiv:
                print('tmp_cnt1',tmp_cnt)
                cnt_ports+=1
                if cnt_ports>= len(self.ser.ports_lst):
                    print("END COM PORT")
                    return 'ERR'

                if 'lin' in sys.platform:
                    self.ser.ser.port = f'/dev/{self.ser.ports_lst[cnt_ports]}'
                else:
                    self.ser.ser.port = self.ser.ports_lst[cnt_ports]
                self.ser.can_open_O(self.ser.ser)
                print('ports_lst',self.ser.ports_lst[cnt_ports])
                tmp_cnt=0
            # print(data_can_dict_value)
            # self.ser.port = 'COM15'
            # self.ser = serial.Serial(port='COM15', baudrate=3000000, timeout=0.01)
            # self.can_open_O(self.ser)
            # print(read_data)
            if self.flag_abort ==1:
                return 'ABORT'
            if data_can_dict_value[:13] in read_data:
                print('tmp_cnt', tmp_cnt)
                list_read_data = read_data.split(b'\r')
                print(list_read_data)
                for i in list_read_data:
                    if data_can_dict_value[:13] in i and len(i) > 21:
                        print(read_data)
                        read_data = i
                        print(read_data)
                        value, address = self.transformed_in_value_and_address(read_data, 'int')
                        print(data_can_dict_value[:13])
                        print(value)
                        return value

    def _header_data_read(self, data_can_dict_value, data_can, mode):

        count = 0
        count1 = 0
        flag = 0
        # self.timer.start(100)
        # self.timer.timeout.connect(lambda: self._begin_data_read(data_can_dict_value))
        # if mode == 'r':
        #     # Копирование главного словаря для хранения значений шапки
        addr = self._begin_data_read(data_can_dict_value)

        if addr =='ERR':
            return 'ERR'
        elif addr == 'ABORT':
            return 'ABORT'

        # addr = 0
        while True:
            if mode == "w":
                print(addr,self.write_id,self.header_data_dict[data_can][count])
                msg_bytes = self.transformed_in_bytes(addr, self.write_id, self.header_data_dict[data_can][count],header=True)
                print()
                id = self.confirmation_id
            else:
                msg_bytes = self.transformed_in_bytes(addr, self.read_id)
                id = self.data_id
            addr += 4
            count += 1
            print(msg_bytes)
            self.ser.ser.write(msg_bytes)
            cnt_recept=0
            while True:
                if self.flag_abort == 1:
                    return 'ABORT'
                cnt_recept+=1
                read_data = self.ser.ser.read(self.ser.buffer_receiv_main)
                if cnt_recept >= 10:
                    print('er_recept_head')
                    self.ser.ser.write(msg_bytes)
                    cnt_recept = 0
                if id in read_data and msg_bytes[5:13] in read_data:
                    list_read_data = read_data.split(b'\r')
                    for i in list_read_data:
                        if i[:4] == id in i and len(i) > 21 and msg_bytes[5:13] in i:
                            read_data = i
                            print(read_data)
                            value, address = self.transformed_in_value_and_address(read_data, 'int','header')
                            print(value)
                            print(address)

                            if mode == 'w':
                                value_write, address_write = self.transformed_in_value_and_address(read_data, 'int')
                                # Если отправленное значение отличается от значения в квитанции, то
                                # повторяем отправку
                                # if value_write != value and count < 20: addr -= 4; count -= 1; count1 += 1
                            else:
                                self.header_data_dict[data_can].append(value)
                                self.file_open.write(hex(address).encode('utf-8') + b'\t')
                                # self.file_open.write(hex(value).encode('utf-8') + b'\n')
                                self.file_open.write(value)
                            flag = 1
                            break
                    if flag == 1: flag = 0;break
            if count == 7: count = 0; count1 = 0; break
        return addr
    def rest(self):
        print('func rest')
        # while True:
        for i in range(1,10):
            time.sleep(1)
            self.cal_signal.emit(i)
            print('rest')
    def main_data_read(self, mode):
        print('main_data_read',mode)
        # Открытие порта
        self.ser.can_open_O(self.ser.ser)

        if mode =='r':
            # Обновление главного словаря данных
            self.header_data_dict = {'preset': [], 'calibr': [], 'filter': []}
            self.data_dict = {'preset': {}, 'calibr': {}, 'filter': {}}
            self.parse_data_xml()

        proc_elem = round((
            (len(self.data_dict['preset']) + len(self.data_dict['calibr']) + len(self.data_dict['filter'])) / 100)+0.5)
        print(len(self.data_dict['preset']) + len(self.data_dict['calibr']) + len(self.data_dict['filter']))
        count_elem = 0
        step = 0

        # Если на запись данных
        if mode == 'w':
            # Стереть сектор
            msg_bytes = self.transformed_in_bytes(0xBFD44000, self.erase_id)
            self.ser.ser.write(msg_bytes)
            time.sleep(0.5)

        for data_can in self.data_can_dict:
            count = 0
            count2 = 0
            # printf(self.data_can_dict[data_can])
            if mode == 'w':
                addr = self._header_data_read(self.data_can_dict[data_can], data_can, 'w')
                id = self.confirmation_id
            else:
                addr = self._header_data_read(self.data_can_dict[data_can], data_can, 'r')
                id = self.data_id
                print(addr)

            if addr =='ERR': return 'ERR'
            elif addr =='ABORT': return 'ABORT'

            # Парсер главного словаря с данными
            for data_main in self.data_dict[data_can].items():
                print(data_main)
                print(self.data_dict[data_can].items())
                count_elem +=1
                if count_elem == proc_elem:
                    step +=1
                    self.cal_signal.emit(step)
                    count_elem =0

                # Запрос с адресом в can
                while True:
                    if self.flag_abort == 1:
                        return 'ABORT'

                    count += 1
                    count2+=count+1
                    # Если парсятся уставки
                    if data_can == 'preset':
                        if count > 4: count = 0; break
                        if mode == 'w':
                            print(self.data_dict[data_can][data_main[0]][count2+1])
                            print(self.data_dict[data_can][data_main[0]])
                            msg_bytes = self.transformed_in_bytes(addr, self.write_id, self.data_dict[data_can] \
                                [data_main[0]][count2 + 1])
                    elif data_can == 'filter':
                        if count > 2: count = 0; break
                        if mode == 'w':
                            msg_bytes = self.transformed_in_bytes(addr, self.write_id, self.data_dict[data_can] \
                                [data_main[0]][count-1])
                    elif data_can == 'calibr':
                        if count > 1: count = 0; break
                        if mode == 'w':
                            msg_bytes = self.transformed_in_bytes(addr, self.write_id, self.data_dict[data_can] \
                                [data_main[0]][count])

                    # printf(number)
                    if mode == 'r':
                        msg_bytes = self.transformed_in_bytes(addr, self.read_id)
                    addr += 4
                    print(msg_bytes)
                    self.ser.ser.write(msg_bytes)
                    cnt_recept =0
                    # Чтение с can значение и адреса
                    while True:
                        cnt_recept+=1
                        read_data = self.ser.ser.read(self.ser.buffer_receiv_main)
                        print(id,'---',read_data)
                        if cnt_recept>=10:
                            print('er_recept')
                            self.ser.ser.write(msg_bytes)
                            cnt_recept =0
                        if id in read_data and msg_bytes[5:13] in read_data:
                            list_read_data = read_data.split(b'\r')
                            for i in list_read_data:
                                if i[:4] == id and len(i) > 21 and msg_bytes[5:13] in i:
                                    read_data = i
                                    print(read_data)

                                    # Конвертируем значения hex в dec
                                    if data_can == 'preset':
                                        # value_dec = self.transformed_hex_to_dec(value, data_main[1][1])
                                        value, address = self.transformed_in_value_and_address(read_data,
                                                                                               data_main[1][1])
                                        if mode == 'w':
                                            value_write, address_write = self.transformed_in_value_and_address \
                                                (msg_bytes, data_main[1][1])
                                        else:
                                            # Добавление вычитаных значений в главный словарь
                                            self.data_dict[data_can][data_main[0]].append(value)
                                    elif data_can == 'calibr':
                                        # value_dec = self.transformed_hex_to_dec(value, 'float')
                                        value, address = self.transformed_in_value_and_address(read_data, 'float')

                                        if mode == 'w':
                                            value_write, address_write = self.transformed_in_value_and_address \
                                                (msg_bytes, 'float')
                                        else:
                                            # Добавление вычитаных значений в главный словарь
                                            self.data_dict[data_can][data_main[0]].append(value)
                                    else:
                                        # value_dec = self.transformed_hex_to_dec(value, 'int')
                                        value, address = self.transformed_in_value_and_address(read_data, 'int')

                                        if mode == 'w':
                                            value_write, address_write = self.transformed_in_value_and_address \
                                                (msg_bytes, 'int')
                                        else:
                                            # Добавление вычитаных значений в главный словарь
                                            self.data_dict[data_can][data_main[0]].append(value)

                                    # Если отправленное значение отличается от значения в квитанции, то
                                    # повторяем отправку
                                    # if value_write != value and count < 20: addr -= 4; count -= 1; count1 += 1

                                    print(value)
                                    # self.file_open.write(hex(address).encode('utf-8') + b'\t')
                                    # self.file_open.write(hex(value).encode('utf-8') + b'\n')

                                    # self.file_open.write(hex(value_dec).encode('utf-8') + b'\n')
                                    flag = 1
                                    break
                            if flag == 1: flag = 0; break
        # self.file_open.close()
        self.ser.can_close(self.ser.ser)
        print(self.data_dict)
        print(self.header_data_dict)
        return 'End main_data_read'

    def param_read(self,global_id):
        while True:
            read_data = self.ser.ser.read(1024)


    def test_data_dict(self,data):
        print(self.data_dict)
        count =0
        if self.flag <2:
            print('FLAG')
            for i in self.data_dict[data].items():
                count+=1
                if data =='preset':
                    if i[1][1] =='float':
                        count =float(count)
                    else:
                        count = int(count)
                    i[1].append(count)
                else:
                    i[1].append(float(count))
        # self.flag +=1
        return self.data_dict
    def update_data_dict(self,data_dict):
        self.data_dict = data_dict
        self.data_dict = data_dict


# cal = Calibrator('SES200M', 'BU_SES')
# ser = Connect()
# cal1 = Calibrator(ser.ser, 'SES200M', 'BU_50')
# cal1.main_data_read('r')
# cal1.main_data_read('w')
# printf(cal1.data_dict)
