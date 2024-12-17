# -*- coding: utf-8 -*-
import serial, time, binascii, struct
import serial.tools.list_ports
from lxml import etree
from debug import printf
# from read_data import transformed_in_value,transformed_in_address,transformed_in_bytes
# from class_read_data import Calibrator
a = 3218341888
a = 0xBFD40000
a = '00010509\n)'
a.replace('\n','')
print(a)

def func ():
    # calibr_list_data = []
    # preset_list_data = []
    # filter_list_data = []
    calibr_dict = {}
    preset_dict = {}
    filter_dict = {}
    data_dict = {'calibr':{},'preset':{},'filter':{}}

    doc = etree.parse('params.xml')
    for setting in doc.findall('.//setting'):
        number = setting.attrib.get('number')
        c_type = setting.attrib.get('ctype')
        for products in setting.findall('products/'):
            product = products.tag
            if product == "SES200M":
                cb = products.attrib.get('cb')
                if cb == 'BU_50':
                    preset_dict[number] = [c_type]
                    # preset_list_data.append(number)
                    # preset_list_data.append(c_type)

    for setting in doc.findall('.//parameter'):
        designation = setting.attrib.get('designation')
        for products1 in setting.findall('.//SES200M'):
            cb = products1.attrib.get('cb')
            if cb == 'BU_50':
                for products2 in products1.findall('.//calibration'):
                    if len(products2.getchildren()) !=0:
                        for i in products2.findall('.//k'):
                            calibr_dict[designation+'_'+i.attrib.get('IND')] = [i.attrib.get('value')]
                            # calibr_list_data.append(designation+'_'+i.attrib.get('IND'))
                            # calibr_list_data.append(i.attrib.get('value'))
                    else:
                        calibr_dict[designation + '_k'] = ['1.0']
                        calibr_dict[designation + '_b'] = ['1.0']
                        # calibr_list_data.append(designation + '_k')
                        # calibr_list_data.append('1.0')
                        # calibr_list_data.append(designation + '_b')
                        # calibr_list_data.append('1.0')

                for products2 in products1.findall('.//filter'):
                    filter_dict[designation+'_FILTER'] =[products2.attrib.get('length')]
                    filter_dict[designation+'_FILTER'] =[products2.attrib.get('length')]
                    # filter_list_data.append(designation+'_FILTER')
                    # filter_list_data.append(products2.attrib.get('length'))
                    # filter_list_data.append(designation+'_FILTER')
                    # filter_list_data.append(products2.attrib.get('length'))
                    # print(products2.attrib)
    data_dict['preset'] = preset_dict
    data_dict['calibr'] = calibr_dict
    data_dict['filter'] = filter_dict
    return data_dict

a = func()
print(a)

d = {'s_zero':['Единица','int'],'s_one':['Двойка','float']}
data_dict1 = {'calibr': {}, 'preset': {}, 'filter': {}}
data_dict1['preset'] = {'s_zero'}
data_dict1['preset'] = d
for i in data_dict1['preset'].items():
    # if i[0] in 'preset':
    print(i[1].append(100))
# print(data_dict1['preset']['s_zero'].append('100'))
print(data_dict1)
d = {'preset':b't0338456500','calibr':b't0338456500','filter':b't0338456500'}
d = {'preset':'','calibr':'','filter':''}
for i in d.items():
    print(i[0])
d['preset'] = b't033876478'
print(d)

class Connect:
    def __init__(self):
        print('Init Connect')
        self.ser = 1


class Obj(Connect):
    def __init__(self):
        super().__init__()
        print('Init')
        print(self.ser)

a = Obj()
print(a)