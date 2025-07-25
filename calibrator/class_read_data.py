# -*- coding: utf-8 -*-
import serial, time, binascii, struct
import serial.tools.list_ports
from lxml import etree
from debug import printf
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot,QTimer,QObject

class Connect(object):
    ser = serial.Serial(port='COM16', baudrate=3000000, timeout=0.1)
    # ser = serial.Serial()

    # def __init__(self):
    # Поиск устройства
    # ports = serial.tools.list_ports.comports()
    # for port in ports:
    #     print(port.device)
    #     port = port.device
    # self.ser = serial.Serial(port =port,baudrate=3000000,timeout=0.1)
    # self.ser = serial.Serial(port='COM88', baudrate=3000000, timeout=0.1)

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
        # После закрытия необходимо заново инициалировать serial
        # arg.close()


class Calibrator(QObject,Connect):
    cal_signal = pyqtSignal(int)
    finish_cal_signal = pyqtSignal()

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
                self.partel_id = b't0328'
                self.read_id = b't60E8'
                self.data_id = b't640'
                self.write_id = b't60F8'
                self.confirmation_id = b't014'
                self.erase_id = b't6108'
                self.preset_designation = 'ADDR_PRESET_ROM'
                self.calibr_designation = 'ADDR_CALIBR_ROM'
                self.filter_designation = 'ADDR_FILTR_ROM'
            elif self.control_block == 'BU_50':
                self.partel_id = b't0338'
                self.read_id = b't6188'
                self.data_id = b't64A'
                self.write_id = b't6198'
                self.confirmation_id = b't015'
                self.erase_id = b't61A8'
                self.preset_designation = 'ADDR_PRESET_ROM2'
                self.calibr_designation = 'ADDR_CALIBR_ROM2'
                self.filter_designation = 'ADDR_FILTR_ROM2'
            elif self.control_block == "BU_400":
                self.partel_id = b't0348'
                self.read_id = b't6228'
                self.data_id = b't654'
                self.write_id = b't6238'
                self.confirmation_id = b't016'
                self.erase_id = b't6248'
                self.preset_designation = 'ADDR_PRESET_ROM3'
                self.calibr_designation = 'ADDR_CALIBR_ROM3'
                self.filter_designation = 'ADDR_FILTR_ROM3'
        # Главный словарь с уставками, калибровками и фильтрами для интерфейса
        self.data_dict = {'preset': {}, 'calibr': {}, 'filter': {}}
        # Словарь с параметрами для вкладки Параметры для интерфейса
        self.param_dict = {f'{self.control_block}': {}}
        # Считывание,преобразование global_id параметров в формaт can и сохранение их в словарь
        self.data_can_dict = {'preset': '', 'calibr': '', 'filter': ''}
        self.data_can_dict['preset'] = self.parse_xml_designation(self.preset_designation)
        self.data_can_dict['calibr'] = self.parse_xml_designation(self.calibr_designation)
        self.data_can_dict['filter'] = self.parse_xml_designation(self.filter_designation)
        # Копирование главного словаря для хранения значений шапки
        self.header_data_dict = {'preset': [], 'calibr': [], 'filter': []}
        # Заполение главного словаря данными
        self.parse_data_xml()

        self.file_open = open('read_data.txt', 'wb')
        self.flag =0
    def transformed_in_value_and_address(self, arg, type):
        value = arg[13:21]
        value = value[6:8] + value[4:6] + value[2:4] + value[0:2]
        value = value.decode('utf-8')
        if type == 'int':
            value = struct.unpack('!I', bytes.fromhex(value))
        else:
            value = struct.unpack('!I', bytes.fromhex(value))
        address = arg[5:13]
        address = address[6:8] + address[4:6] + address[2:4] + address[0:2]
        address = address.decode('utf-8')
        address = struct.unpack('!I', bytes.fromhex(address))
        return value[0], address[0]

    # Преобразование целочисленного значения в байтовый тип формата can
    def transformed_in_bytes(self, arg, id, val=b'000000000000'):
        # read_id = b't' + hex(self.read_id).upper().encode('utf-8')[2:] + b'8'
        if val != b'000000000000':
            val = hex(val)[2:].upper()
            val = val[6:8] + val[4:6] + val[2:4] + val[0:2]
            val = val.encode('utf-8') + b'0000'

        arg = hex(arg)[2:].upper()
        arg = arg[6:8] + arg[4:6] + arg[2:4] + arg[0:2]
        arg = arg.encode('utf-8')
        arg = id + arg + val + b'\r'
        return arg

    # Перевод числа из hex в decimal
    def transformed_hex_to_dec(self, value, type):
        if type == "float":
            value = struct.unpack('!f', bytes.fromhex(str(value)))
            return value[0]
        elif type == 'int':
            printf(value)
            value = struct.unpack('!f', bytes.fromhex(str(value)))
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
        # Пример возвращаемого значения: b't0338002F000000000000\r'
        return global_id_can_format

    # Считывание уставок, калибровок, фильтров и сохранение их в списки
    def parse_data_xml(self):
        flag = 0
        preset_dict = {}
        calibr_dict = {}
        filter_dict = {}
        params_dict = {}
        doc = etree.parse('params.xml')
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
                    if cb == self.control_block:
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
        return self.data_dict

    def pars_eskd(self):
        doc = etree.parse('params.xml')
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
        while True:
            read_data = self.ser.read(1024)
            printf(data_can_dict_value)
            # printf(read_data)
            if data_can_dict_value[:13] in read_data:
                list_read_data = read_data.split(b'\r')
                printf(list_read_data)
                for i in list_read_data:
                    if data_can_dict_value[:13] in i and len(i) > 21:
                        printf(read_data)
                        read_data = i
                        printf(read_data)
                        value, address = self.transformed_in_value_and_address(read_data, 'int')
                        printf(data_can_dict_value[:13])
                        printf(value)
                        return value

    def _header_data_read(self, data_can_dict_value, data_can, mode):
        count = 0
        count1 = 0
        flag = 0
        # self.timer.start(100)
        # self.timer.timeout.connect(lambda: self._begin_data_read(data_can_dict_value))
        addr = self._begin_data_read(data_can_dict_value)
        # addr = 0
        while True:
            if mode == "w":
                msg_bytes = self.transformed_in_bytes(addr, self.write_id, self.header_data_dict[data_can][count])
                id = self.confirmation_id
            else:
                msg_bytes = self.transformed_in_bytes(addr, self.read_id)
                id = self.data_id
            addr += 4
            count += 1
            printf(msg_bytes)
            self.ser.write(msg_bytes)
            while True:
                read_data = self.ser.read(1024)
                if id in read_data:
                    list_read_data = read_data.split(b'\r')
                    for i in list_read_data:
                        if i[:4] == id in i and len(i) > 21:
                            read_data = i
                            printf(read_data)
                            value, address = self.transformed_in_value_and_address(read_data, 'int')
                            printf(value)
                            printf(address)

                            if mode == 'w':
                                value_write, address_write = self.transformed_in_value_and_address(read_data, 'int')
                                # Если отправленное значение отличается от значения в квитанции, то
                                # повторяем отправку
                                # if value_write != value and count < 20: addr -= 4; count -= 1; count1 += 1
                            else:
                                self.header_data_dict[data_can].append(value)
                                self.file_open.write(hex(address).encode('utf-8') + b'\t')
                                self.file_open.write(hex(value).encode('utf-8') + b'\n')
                            flag = 1
                            break
                    if flag == 1: flag = 0;break
            if count == 7: count = 0; count1 = 0; break
        return addr
    def rest(self):
        printf('func rest')
        # while True:
        for i in range(1,10):
            time.sleep(1)
            self.cal_signal.emit(i)
            printf('rest')
    def main_data_read(self, mode):
        print('main_data_read',mode)
        # Открытие порта
        self.can_open_O(self.ser)

        # Если на запись данных
        if mode == 'w':
            # Стереть сектор
            msg_bytes = self.transformed_in_bytes(0xBFD44000, self.erase_id)
            self.ser.write(msg_bytes)
            time.sleep(0.5)

        for data_can in self.data_can_dict:
            count = 0
            # printf(self.data_can_dict[data_can])
            if mode == 'w':
                addr = self._header_data_read(self.data_can_dict[data_can], data_can, 'w')
            else:
                addr = self._header_data_read(self.data_can_dict[data_can], data_can, 'r')

            # Парсер главного словаря с данным
            for data_main in self.data_dict[data_can].items():
                printf(data_main)

                # Запрос с адресом в can
                while True:
                    count += 1
                    # Если парсятся уставки
                    if data_can == 'preset':
                        if count > 4: count = 0; break
                        if mode == 'w':
                            printf(self.data_dict[data_can][data_main[0]][count+1])
                            msg_bytes = self.transformed_in_bytes(addr, self.write_id, self.data_dict[data_can] \
                                [data_main[0]][count + 1])
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
                    printf(msg_bytes)
                    self.ser.write(msg_bytes)
                    # Чтение с can значение и адреса
                    while True:
                        read_data = self.ser.read(1024)
                        if self.data_id in read_data:
                            list_read_data = read_data.split(b'\r')
                            for i in list_read_data:
                                if i[:4] == self.data_id and len(i) > 21:
                                    read_data = i
                                    printf(read_data)

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

                                    printf(value)
                                    self.file_open.write(hex(address).encode('utf-8') + b'\t')
                                    self.file_open.write(hex(value).encode('utf-8') + b'\n')

                                    # self.file_open.write(hex(value_dec).encode('utf-8') + b'\n')
                                    flag = 1
                                    break
                            if flag == 1: flag = 0; break
        # self.file_open.close()
        self.can_close(self.ser)
        printf(self.data_dict)
        printf(self.header_data_dict)
        return 'End main_data_read'
    def test_data_dict(self,data):
        printf(self.data_dict)
        count =0
        if self.flag <2:
            printf('FLAG')
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


# cal = Calibrator('SES200M', 'BU_SES')
# ser = Connect()
# cal1 = Calibrator(ser.ser, 'SES200M', 'BU_50')
# cal1.main_data_read('r')
# cal1.main_data_read('w')
# printf(cal1.data_dict)
