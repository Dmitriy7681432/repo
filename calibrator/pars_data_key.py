import xml.etree.ElementTree as ET

def func_val_to_hex_can_flip(c):
    c = hex(c)[2:].upper()
    if len(c) == 1:
        c = '0' + c + "000000"
    elif len(c) == 2:
        c = c + "000000"
    elif len(c) == 3:
        c = c[1:] + '0' + c[:1] + '0000'
    elif len(c) == 4:
        c = c[len(c) - 2:] + \
            c[len(c) - 4:len(c) - 2] + "0000"
    elif len(c) == 5:
        c = c[-2:] + c[1:3] + '0' + c[:1] + '00'
    elif len(c) == 6:
        c = c[len(c) - 2:] + c[len(c) - 4:len(c) - 2] + \
            c[len(c) - 6:len(c) - 4] + "00"
    elif len(c) == 7:
        c = c[-2:] + c[3:5] + c[1:3] + '0' + c[:1]
    elif len(c) == 8:
        c = c[len(c) - 2:] + c[len(c) - 4:len(c) - 2] + \
            c[len(c) - 6:len(c) - 4] + c[len(c) - 8:len(c) - 6]
    return c


class DataKey():
    units = 0
    count = 0
    count1 = 0
    lst_com_id = []
    flag_1 = 0
    flag_2 = 0
    flag_4 = 0

    def __init__(self,file_xml,prodeuct):
        tree = ET.parse(file_xml)
        self.root = tree.getroot()
        self.product = prodeuct

    def main_pars(self):
        self.file = open('data_key2.txt', 'w+', encoding='utf-8')

        if self.product =='SES200M':
            self.cb = ['BU_50','BU_SES',"BU_400"]
        elif self.product =='SEP30M':
            self.cb = ['BU_SEP', 'BU_SEP', "BU_400"]
        # lst_elem = ['parameter','event','limit']
        lst_elem = ['parameter']
        for i in lst_elem:
            self.pars_unit(i,self.product,self.cb)
        for i in lst_elem:
            self.pars_device(i,self.product,self.cb)

        self.file.close()

    def pars_unit(self,arg,prod,cb):
        for unit in self.root.findall('.//unit'):
            unit_range = unit.attrib.get('range')
            unit_name = unit.attrib.get('name')
            self.count1=int(unit_range)
            com_id = int(unit_range)
            flag = 0
            self.flag_4 = 0
            # print('for1')
            # print(count1)
            for elem in unit.findall(arg):
                designation = elem.attrib.get('designation')
                name = elem.attrib.get('name')
                if arg == 'parameter':
                    type = elem.attrib.get('type')
                common_id = elem.attrib.get('common_id')
                common_id_1 = elem.attrib.get('common_id')
                # print(parameter_common_id)

                # print('for2')
                flag_3=0
                for products in elem.findall('products/'):
                    product = products.tag
                    # print('for3')
                    if product == prod and flag_3==0:
                        self.units = products.attrib.get('cb')
                        if self.flag_4 ==0 and arg == 'parameter':
                            self.file.write('\n' + '// Агрегат '+unit_name + '\n'+'\n')
                            self.flag_4=1
                        # print('for4')
                        # if arg == 'parameter':
                        if ((self.units == cb[0]) or (self.units == cb[1]) or (self.units == cb[2])):
                        # and ((type =='Измеряемый') or (type =='Вычисляемый')or
                        # (type =='Внешний') or (type =='Дискретный')or
                        # (type =='Сводный') or (type =='Команда')):
                            if common_id == None:
                                if flag ==1:
                                    common_id = self.count1 + 1
                                    com_id = common_id
                                elif flag==0:
                                    common_id=com_id +300
                                    com_id = common_id
                                    flag=1
                                   # print('PRINTF')
                                elif flag==2:
                                    common_id = com_id + 1
                                    com_id = common_id
                            else:
                                if flag==1: flag =2
                            self.count1 = int(common_id)
                            # print('for5')
                            flag_3=1

                            self.count =self.count+1
                            # print(parameter_designation)
                            if common_id_1 != None: self.lst_com_id.append(common_id_1)
                            # if common_id_1!=None:
                            #     if self.flag_1 ==0:
                            #         prm_com_id = int(common_id_1)
                            #         self.flag_1 = 1
                            #     elif self.flag_1 ==1:
                            #         prm_com_id_1 = int(common_id_1)
                            #         self.flag_1=0
                            #         self.flag_2 = 1
                            #     if self.flag_2==1:
                            #         if prm_com_id >=prm_com_id_1:
                            #             print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                            #         self.flag_2=2
                            #     elif self.flag_2==2:
                            #         if prm_com_id_1 >=prm_com_id:
                            #             print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                            #         self.flag_1=1
                            #         self.flag_2 = 0
                            # file.write(parameter_designation + parameter_common_id + "\n")
                           # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                           #            str(count1) + " p " + str(count) + "\n")
                            hex_common_id = 'hex=' + hex(int(common_id))[2:].upper() + ' '
                            hex_flip_common_id = 'hex_flip= ' + func_val_to_hex_can_flip(int(common_id))
                            self.file.write('// ' + name + '\n' + '#define KEY_' + designation + \
                                       ' ((uint32_t)(' + str(
                                common_id) + ")) " + hex_common_id + hex_flip_common_id + " " + "\n")
                            # self.file.write('// '+ name + '\n'+ "#define KEY_" + designation + " ((uint32_t)(" +str(common_id)+"))" + "\n")

                            # print(lst_com_id)
                            # file.write(parameter_designation + ", 0 - " + parameter_name+ "\n")

            # for event in unit.findall('event'):
            #     event_designation = event.attrib.get('designation')
            #     event_name = event.attrib.get('name')
            #     event_common_id = event.attrib.get('common_id')
            #     event_common_id_1 = event.attrib.get('common_id')
            #     # print(parameter_common_id)
            #     # print('for2')
            #     flag_3=0
            #     for products in event.findall('products/'):
            #         SES200M1 = products.tag
            #         # print('for3')
            #         if SES200M1 =='SES200M' and flag_3==0:
            #             self.units = products.attrib.get('cb')
            #             # print('for4')
            #             if ((self.units == 'BU_50') or (self.units == 'BU_SES')or (self.units == 'BU_400')):
            #                 if event_common_id == None:
            #                     if flag ==1:
            #                         event_common_id = self.count1 + 1
            #                         com_id =event_common_id
            #                     elif flag==0:
            #                         event_common_id =com_id +300
            #                         com_id = event_common_id
            #                         flag=1
            #                        # print('PRINTF')
            #                     elif flag==2:
            #                         event_common_id = com_id + 1
            #                         com_id = event_common_id
            #                 else:
            #                     if flag==1: flag =2
            #                 self.count1 = int(event_common_id )
            #                 # print('for5')
            #                 flag_3=1
            #
            #                 self.count =self.count+1
            #                 # print(event_designation)
            #                 if event_common_id_1 != None: self.lst_com_id.append(event_common_id_1)
            #                 if event_common_id_1!=None:
            #                     if self.flag_1 ==0:
            #                         prm_com_id = int(event_common_id_1)
            #                         self.flag_1 = 1
            #                     elif self.flag_1 ==1:
            #                         prm_com_id_1 = int(event_common_id_1)
            #                         self.flag_1=0
            #                         self.flag_2 = 1
            #                     if self.flag_2==1:
            #                         if prm_com_id >=prm_com_id_1:
            #                             print("Error com_id", prm_com_id, 'и', prm_com_id_1)
            #                         self.flag_2=2
            #                     elif self.flag_2==2:
            #                         if prm_com_id_1 >=prm_com_id:
            #                             print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
            #                         self.flag_1=1
            #                         self.flag_2 = 0
            #                 # file.write(parameter_designation + parameter_common_id + "\n")
            #                # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
            #                #            str(count1) + " p " + str(count) + "\n")
            #                 self.file.write('// '+ event_name + '\n'+ event_designation +" "+ "KEY("+ str(event_common_id)+ ")"+ " " + "\n")
            #
            #                 # print(lst_com_id)
            #
            #
            # for limit in unit.findall('limit'):
            #     limit_designation = limit.attrib.get('designation')
            #     limit_name = limit.attrib.get('name')
            #     limit_common_id = limit.attrib.get('common_id')
            #     limit_common_id_1 = limit.attrib.get('common_id')
            #     # print(parameter_common_id)
            #     # print('for2')
            #     flag_3=0
            #     for products in limit.findall('products/'):
            #         SES200M1 = products.tag
            #         # print('for3')
            #         if SES200M1 =='SES200M' and flag_3==0:
            #             self.units = products.attrib.get('cb')
            #             # print('for4')
            #             if ((self.units == 'BU_50') or (self.units == 'BU_SES')or (self.units == 'BU_400')):
            #                 if limit_common_id == None:
            #                     if flag ==1:
            #                         limit_common_id = self.count1 + 1
            #                         com_id = limit_common_id
            #                     elif flag==0:
            #                         limit_common_id =com_id +300
            #                         com_id = limit_common_id
            #                         flag=1
            #                        # print('PRINTF')
            #                     elif flag==2:
            #                         limit_common_id = com_id + 1
            #                         com_id = limit_common_id
            #                 else:
            #                     if flag==1: flag =2
            #                 self.count1 = int(limit_common_id)
            #                 # print('for5')
            #                 flag_3=1
            #
            #                 self.count =self.count+1
            #                 # print(limit_designation)
            #                 if limit_common_id_1 != None: self.lst_com_id.append(limit_common_id_1)
            #                 if limit_common_id_1 !=None:
            #                     if self.flag_1 ==0:
            #                         prm_com_id = int(limit_common_id_1)
            #                         self.flag_1 = 1
            #                     elif self.flag_1 ==1:
            #                         prm_com_id_1 = int(limit_common_id_1)
            #                         self.flag_1=0
            #                         self.flag_2 = 1
            #                     if self.flag_2==1:
            #                         if prm_com_id >=prm_com_id_1:
            #                             print("Error com_id", prm_com_id, 'и', prm_com_id_1)
            #                         self.flag_2=2
            #                     elif self.flag_2==2:
            #                         if prm_com_id_1 >=prm_com_id:
            #                             print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
            #                         self.flag_1=1
            #                         self.flag_2 = 0
            #                 # file.write(parameter_designation + parameter_common_id + "\n")
            #                # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
            #                #            str(count1) + " p " + str(count) + "\n")
            #                 self.file.write('// '+ limit_name + '\n'+ limit_designation +" "+ "KEY("+ str(limit_common_id)+ ")"+ " " + "\n")
            #
            #                 # print(lst_com_id)
    def pars_device(self,arg,prod,cb):
        for unit in self.root.findall('.//device'):
            unit_range = unit.attrib.get('range')
            unit_name = unit.attrib.get('name')
            self.count1=int(unit_range)-1
            com_id = int(unit_range)
            flag = 0
            self.flag_4 = 0
            # print('for1')
            # print(count1)
            for elem in unit.findall(arg):
                designation = elem.attrib.get('designation')
                name = elem.attrib.get('name')
                if arg =='parameter':
                    type = elem.attrib.get('type')
                common_id = elem.attrib.get('common_id')
                common_id_1 = elem.attrib.get('common_id')
                # print(parameter_common_id)
                # print('for2')
                flag_3=0
                for products in elem.findall('products/'):
                    product = products.tag
                    # print('for3')
                    if product == prod and flag_3==0:
                        self.units = products.attrib.get('cb')
                        if self.flag_4 ==0 and arg =='parameter':
                            self.file.write('\n' + '// Устройство '+unit_name + '\n'+'\n')
                            self.flag_4=1
                        # print('for4')
                        if ((self.units == cb[0]) or (self.units == cb[1])or (self.units == cb[2])):
                        # and ((type =='Измеряемый') or (type =='Вычисляемый')or
                        # (type =='Внешний') or (type =='Дискретный')or
                        # (type =='Сводный') or (type =='Команда')):
                            if common_id == None:
                                common_id = self.count1 + 1
                            self.count1 = int(common_id)
                            # print('for5')
                            flag_3=1
                            self.count =self.count+1
                            # print(parameter_designation)
                            if common_id_1 != None: self.lst_com_id.append(common_id_1)
                            # if common_id_1!=None:
                            #     if self.flag_1 ==0:
                            #         prm_com_id = int(common_id_1)
                            #         self.flag_1 = 1
                            #     elif self.flag_1 ==1:
                            #         prm_com_id_1 = int(common_id_1)
                            #         self.flag_1=0
                            #         self.flag_2 = 1
                            #     if self.flag_2==1:
                            #         if prm_com_id >=prm_com_id_1:
                            #             print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                            #         self.flag_2=2
                            #     elif self.flag_2==2:
                            #         if prm_com_id_1 >=prm_com_id:
                            #             print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                            #         self.flag_1=1
                            #         self.flag_2 = 0
                            # file.write(parameter_designation + parameter_common_id + "\n")
                           # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                           #            str(count1) + " p " + str(count) + "\n")
                            hex_common_id = 'hex=' + hex(int(common_id))[2:].upper() + ' '
                            hex_flip_common_id = 'hex_flip= ' + func_val_to_hex_can_flip(int(common_id))
                            self.file.write('// ' + name + '\n' + '#define KEY_' + designation + \
                                            ' ((uint32_t)(' + str(
                                common_id) + ")) " + hex_common_id + hex_flip_common_id + " " + "\n")
                            # self.file.write(
                            # '// ' + name + '\n' + "#define KEY_" + designation + " ((uint32_t)(" + str(common_id) + "))" + "\n")

                        # print(lst_com_id)
                            # file.write(parameter_designation + ", 0 - " + parameter_name+ "\n")

            # for event in unit.findall('event'):
            #     event_designation = event.attrib.get('designation')
            #     event_name = event.attrib.get('name')
            #     event_common_id = event.attrib.get('common_id')
            #     event_common_id_1 = event.attrib.get('common_id')
            #     # print(parameter_common_id)
            #     # print('for2')
            #     flag_3=0
            #     for products in event.findall('products/'):
            #         SES200M1 = products.tag
            #         # print('for3')
            #         if SES200M1 =='SES200M' and flag_3==0:
            #             self.units = products.attrib.get('cb')
            #             # print('for4')
            #             if ((self.units == 'BU_50') or (self.units == 'BU_SES')or (self.units == 'BU_400')):
            #                 if event_common_id == None:
            #                     event_common_id = self.count1 + 1
            #                 self.count1 = int(event_common_id )
            #                 # print('for5')
            #                 flag_3=1
            #                 self.count =self.count+1
            #                 # print(event_designation)
            #                 if event_common_id_1 != None: self.lst_com_id.append(event_common_id_1)
            #                 if event_common_id_1!=None:
            #                     if self.flag_1 ==0:
            #                         prm_com_id = int(event_common_id_1)
            #                         self.flag_1 = 1
            #                     elif self.flag_1 ==1:
            #                         prm_com_id_1 = int(event_common_id_1)
            #                         self.flag_1=0
            #                         self.flag_2 = 1
            #                     if self.flag_2==1:
            #                         if prm_com_id >=prm_com_id_1:
            #                             print("Error com_id", prm_com_id, 'и', prm_com_id_1)
            #                         self.flag_2=2
            #                     elif self.flag_2==2:
            #                         if prm_com_id_1 >=prm_com_id:
            #                             print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
            #                         self.flag_1=1
            #                         self.flag_2 = 0
            #                 # file.write(parameter_designation + parameter_common_id + "\n")
            #                # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
            #                #            str(count1) + " p " + str(count) + "\n")
            #                 self.file.write('// '+ event_name + '\n'+ event_designation +" "+ "KEY("+ str(event_common_id)+ ")"+ " " + "\n")
            #
            #                 # print(lst_com_id)
            #
            #
            # for limit in unit.findall('limit'):
            #     limit_designation = limit.attrib.get('designation')
            #     limit_name = limit.attrib.get('name')
            #     limit_common_id = limit.attrib.get('common_id')
            #     limit_common_id_1 = limit.attrib.get('common_id')
            #     # print(parameter_common_id)
            #     # print('for2')
            #     flag_3=0
            #     for products in limit.findall('products/'):
            #         SES200M1 = products.tag
            #         # print('for3')
            #         if SES200M1 =='SES200M' and flag_3==0:
            #             self.units = products.attrib.get('cb')
            #             # print('for4')
            #             if ((self.units == 'BU_50') or (self.units == 'BU_SES')or (self.unit == 'BU_400')):
            #                 if limit_common_id == None:
            #                     limit_common_id = self.count1 + 1
            #                 self.count1 = int(limit_common_id)
            #                 # print('for5')
            #                 flag_3=1
            #                 self.count =self.count+1
            #                 # print(limit_designation)
            #                 if limit_common_id_1 != None: self.lst_com_id.append(limit_common_id_1)
            #                 if limit_common_id_1 !=None:
            #                     if self.flag_1 ==0:
            #                         prm_com_id = int(limit_common_id_1)
            #                         self.flag_1 = 1
            #                     elif self.flag_1 ==1:
            #                         prm_com_id_1 = int(limit_common_id_1)
            #                         self.flag_1=0
            #                         self.flag_2 = 1
            #                     if self.flag_2==1:
            #                         if prm_com_id >=prm_com_id_1:
            #                             print("Error com_id", prm_com_id, 'и', prm_com_id_1)
            #                         self.flag_2=2
            #                     elif self.flag_2==2:
            #                         if prm_com_id_1 >=prm_com_id:
            #                             print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
            #                         self.flag_1=1
            #                         self.flag_2 = 0
            #                 # file.write(parameter_designation + parameter_common_id + "\n")
            #                # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
            #                #            str(count1) + " p " + str(count) + "\n")
            #                 self.file.write('// '+ limit_name + '\n'+ limit_designation +" "+ "KEY("+ str(limit_common_id)+ ")"+ " " + "\n")
            #
            #                 # print(lst_com_id)



if __name__ == '__main__':
    pars_data_key = DataKey('params_sep30m.xml','SEP30M')
    pars_data_key.main_pars()
