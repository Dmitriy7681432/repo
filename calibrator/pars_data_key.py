import xml.etree.ElementTree as ET



class DataKey(object):

    def __int__(self):
        tree = ET.parse('params.xml')
        self.root = tree.getroot()
        self.file = open('data_key.txt', 'w+',encoding='utf-8')
        self.units = 0
        self.count = 0
        self.count1 = 0
        self.lst_com_id = []
        self.flag_1=0
        self.flag_2=0
        self.flag_4=0

    def pars_unit(self):
        for unit in self.root.findall('.//unit'):
            unit_range = unit.attrib.get('range')
            unit_name = unit.attrib.get('name')
            self.count1=int(unit_range)
            com_id = int(unit_range)
            flag = 0
            self.flag_4 = 0
            # print('for1')
            # print(count1)
            for parameter in unit.findall('parameter'):
                parameter_designation = parameter.attrib.get('designation')
                parameter_name = parameter.attrib.get('name')
                parameter_type = parameter.attrib.get('type')
                parameter_common_id = parameter.attrib.get('common_id')
                parameter_common_id_1 = parameter.attrib.get('common_id')
                # print(parameter_common_id)

                # print('for2')
                flag_3=0
                for products in parameter.findall('products/'):
                    SES200M1 = products.tag
                    # print('for3')
                    if SES200M1 =='SES200M' and flag_3==0:
                        self.unit = products.attrib.get('cb')
                        if self.flag_4 ==0:
                            self.file.write('\n' + '// Агрегат '+unit_name + '\n'+'\n')
                            self.flag_4=1
                        # print('for4')
                        if ((self.units == 'BU_50') or (self.units == 'BU_SES')or (self.units == 'BU_400'))\
                        and ((parameter_type =='Измеряемый') or (parameter_type =='Вычисляемый')or
                        (parameter_type =='Внешний') or (parameter_type =='Дискретный')or
                        (parameter_type =='Сводный') or (parameter_type =='Команда')):
                            if parameter_common_id == None:
                                if flag ==1:
                                    parameter_common_id = serial.count1 + 1
                                    com_id = parameter_common_id
                                elif flag==0:
                                    parameter_common_id=com_id +300
                                    com_id = parameter_common_id
                                    flag=1
                                   # print('PRINTF')
                                elif flag==2:
                                    parameter_common_id = com_id + 1
                                    com_id = parameter_common_id
                            else:
                                if flag==1: flag =2
                            self.count1 = int(parameter_common_id)
                            # print('for5')
                            flag_3=1

                            self.count =self.count+1
                            # print(parameter_designation)
                            if parameter_common_id_1 != None: self.lst_com_id.append(parameter_common_id_1)
                            if parameter_common_id_1!=None:
                                if self.flag_1 ==0:
                                    prm_com_id = int(parameter_common_id_1)
                                    self.flag_1 = 1
                                elif self.flag_1 ==1:
                                    prm_com_id_1 = int(parameter_common_id_1)
                                    self.flag_1=0
                                    self.flag_2 = 1
                                if self.flag_2==1:
                                    if prm_com_id >=prm_com_id_1:
                                        print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                                    self.flag_2=2
                                elif self.flag_2==2:
                                    if prm_com_id_1 >=prm_com_id:
                                        print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                                    self.flag_1=1
                                    self.flag_2 = 0
                            # file.write(parameter_designation + parameter_common_id + "\n")
                           # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                           #            str(count1) + " p " + str(count) + "\n")
                            self.file.write('// '+ parameter_name + '\n'+ parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + "\n")

                            # print(lst_com_id)
                            # file.write(parameter_designation + ", 0 - " + parameter_name+ "\n")

            for event in unit.findall('event'):
                event_designation = event.attrib.get('designation')
                event_name = event.attrib.get('name')
                event_common_id = event.attrib.get('common_id')
                event_common_id_1 = event.attrib.get('common_id')
                # print(parameter_common_id)
                # print('for2')
                flag_3=0
                for products in event.findall('products/'):
                    SES200M1 = products.tag
                    # print('for3')
                    if SES200M1 =='SES200M' and flag_3==0:
                        self.units = products.attrib.get('cb')
                        # print('for4')
                        if ((self.units == 'BU_50') or (self.units == 'BU_SES')or (self.units == 'BU_400')):
                            if event_common_id == None:
                                if flag ==1:
                                    event_common_id = self.count1 + 1
                                    com_id =event_common_id
                                elif flag==0:
                                    event_common_id =com_id +300
                                    com_id = event_common_id
                                    flag=1
                                   # print('PRINTF')
                                elif flag==2:
                                    event_common_id = com_id + 1
                                    com_id = event_common_id
                            else:
                                if flag==1: flag =2
                            self.count1 = int(event_common_id )
                            # print('for5')
                            flag_3=1

                            self.count =self.count+1
                            # print(event_designation)
                            if event_common_id_1 != None: self.lst_com_id.append(event_common_id_1)
                            if event_common_id_1!=None:
                                if self.flag_1 ==0:
                                    prm_com_id = int(event_common_id_1)
                                    self.flag_1 = 1
                                elif self.flag_1 ==1:
                                    prm_com_id_1 = int(event_common_id_1)
                                    self.flag_1=0
                                    self.flag_2 = 1
                                if self.flag_2==1:
                                    if prm_com_id >=prm_com_id_1:
                                        print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                                    self.flag_2=2
                                elif self.flag_2==2:
                                    if prm_com_id_1 >=prm_com_id:
                                        print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                                    self.flag_1=1
                                    self.flag_2 = 0
                            # file.write(parameter_designation + parameter_common_id + "\n")
                           # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                           #            str(count1) + " p " + str(count) + "\n")
                            self.file.write('// '+ event_name + '\n'+ event_designation +" "+ "KEY("+ str(event_common_id)+ ")"+ " " + "\n")

                            # print(lst_com_id)


            for limit in unit.findall('limit'):
                limit_designation = limit.attrib.get('designation')
                limit_name = limit.attrib.get('name')
                limit_common_id = limit.attrib.get('common_id')
                limit_common_id_1 = limit.attrib.get('common_id')
                # print(parameter_common_id)
                # print('for2')
                flag_3=0
                for products in limit.findall('products/'):
                    SES200M1 = products.tag
                    # print('for3')
                    if SES200M1 =='SES200M' and flag_3==0:
                        self.units = products.attrib.get('cb')
                        # print('for4')
                        if ((self.units == 'BU_50') or (self.units == 'BU_SES')or (self.units == 'BU_400')):
                            if limit_common_id == None:
                                if flag ==1:
                                    limit_common_id = self.count1 + 1
                                    com_id = limit_common_id
                                elif flag==0:
                                    limit_common_id =com_id +300
                                    com_id = limit_common_id
                                    flag=1
                                   # print('PRINTF')
                                elif flag==2:
                                    limit_common_id = com_id + 1
                                    com_id = limit_common_id
                            else:
                                if flag==1: flag =2
                            self.count1 = int(limit_common_id)
                            # print('for5')
                            flag_3=1

                            self.count =self.count+1
                            # print(limit_designation)
                            if limit_common_id_1 != None: self.lst_com_id.append(limit_common_id_1)
                            if limit_common_id_1 !=None:
                                if self.flag_1 ==0:
                                    prm_com_id = int(limit_common_id_1)
                                    self.flag_1 = 1
                                elif self.flag_1 ==1:
                                    prm_com_id_1 = int(limit_common_id_1)
                                    self.flag_1=0
                                    self.flag_2 = 1
                                if self.flag_2==1:
                                    if prm_com_id >=prm_com_id_1:
                                        print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                                    self.flag_2=2
                                elif self.flag_2==2:
                                    if prm_com_id_1 >=prm_com_id:
                                        print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                                    self.flag_1=1
                                    self.flag_2 = 0
                            # file.write(parameter_designation + parameter_common_id + "\n")
                           # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                           #            str(count1) + " p " + str(count) + "\n")
                            self.file.write('// '+ limit_name + '\n'+ limit_designation +" "+ "KEY("+ str(limit_common_id)+ ")"+ " " + "\n")

                            # print(lst_com_id)
    def pars_device(self):
        for unit in self.root.findall('.//device'):
            unit_range = unit.attrib.get('range')
            unit_name = unit.attrib.get('name')
            self.count1=int(unit_range)-1
            com_id = int(unit_range)
            flag = 0
            self.flag_4 = 0
            # print('for1')
            # print(count1)
            for parameter in unit.findall('parameter'):
                parameter_designation = parameter.attrib.get('designation')
                parameter_name = parameter.attrib.get('name')
                parameter_type = parameter.attrib.get('type')
                parameter_common_id = parameter.attrib.get('common_id')
                parameter_common_id_1 = parameter.attrib.get('common_id')
                # print(parameter_common_id)

                # print('for2')
                flag_3=0
                for products in parameter.findall('products/'):
                    SES200M1 = products.tag
                    # print('for3')
                    if SES200M1 =='SES200M' and flag_3==0:
                        unint = products.attrib.get('cb')
                        if self.flag_4 ==0:
                            self.file.write('\n' + '// Устройство '+unit_name + '\n'+'\n')
                            self.flag_4=1
                        # print('for4')
                        if ((self.units == 'BU_50') or (self.units == 'BU_SES')or (self.units == 'BU_400'))\
                        and ((parameter_type =='Измеряемый') or (parameter_type =='Вычисляемый')or
                        (parameter_type =='Внешний') or (parameter_type =='Дискретный')or
                        (parameter_type =='Сводный') or (parameter_type =='Команда')):
                            if parameter_common_id == None:
                                parameter_common_id = self.count1 + 1
                            self.count1 = int(parameter_common_id)
                            # print('for5')
                            flag_3=1

                            self.count =self.count+1
                            # print(parameter_designation)
                            if parameter_common_id_1 != None: self.lst_com_id.append(parameter_common_id_1)
                            if parameter_common_id_1!=None:
                                if self.flag_1 ==0:
                                    prm_com_id = int(parameter_common_id_1)
                                    self.flag_1 = 1
                                elif self.flag_1 ==1:
                                    prm_com_id_1 = int(parameter_common_id_1)
                                    self.flag_1=0
                                    self.flag_2 = 1
                                if self.flag_2==1:
                                    if prm_com_id >=prm_com_id_1:
                                        print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                                    self.flag_2=2
                                elif self.flag_2==2:
                                    if prm_com_id_1 >=prm_com_id:
                                        print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                                    self.flag_1=1
                                    self.flag_2 = 0
                            # file.write(parameter_designation + parameter_common_id + "\n")
                           # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                           #            str(count1) + " p " + str(count) + "\n")
                            self.file.write('// '+ parameter_name + '\n'+ parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + "\n")

                            # print(lst_com_id)
                            # file.write(parameter_designation + ", 0 - " + parameter_name+ "\n")

            for event in unit.findall('event'):
                event_designation = event.attrib.get('designation')
                event_name = event.attrib.get('name')
                event_common_id = event.attrib.get('common_id')
                event_common_id_1 = event.attrib.get('common_id')
                # print(parameter_common_id)
                # print('for2')
                flag_3=0
                for products in event.findall('products/'):
                    SES200M1 = products.tag
                    # print('for3')
                    if SES200M1 =='SES200M' and flag_3==0:
                        self.units = products.attrib.get('cb')
                        # print('for4')
                        if ((self.units == 'BU_50') or (self.units == 'BU_SES')or (self.units == 'BU_400')):
                            if event_common_id == None:
                                event_common_id = self.count1 + 1
                            self.count1 = int(event_common_id )
                            # print('for5')
                            flag_3=1
                            self.count =self.count+1
                            # print(event_designation)
                            if event_common_id_1 != None: self.lst_com_id.append(event_common_id_1)
                            if event_common_id_1!=None:
                                if self.flag_1 ==0:
                                    prm_com_id = int(event_common_id_1)
                                    self.flag_1 = 1
                                elif self.flag_1 ==1:
                                    prm_com_id_1 = int(event_common_id_1)
                                    self.flag_1=0
                                    self.flag_2 = 1
                                if self.flag_2==1:
                                    if prm_com_id >=prm_com_id_1:
                                        print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                                    self.flag_2=2
                                elif self.flag_2==2:
                                    if prm_com_id_1 >=prm_com_id:
                                        print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                                    self.flag_1=1
                                    self.flag_2 = 0
                            # file.write(parameter_designation + parameter_common_id + "\n")
                           # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                           #            str(count1) + " p " + str(count) + "\n")
                            self.file.write('// '+ event_name + '\n'+ event_designation +" "+ "KEY("+ str(event_common_id)+ ")"+ " " + "\n")

                            # print(lst_com_id)


            for limit in unit.findall('limit'):
                limit_designation = limit.attrib.get('designation')
                limit_name = limit.attrib.get('name')
                limit_common_id = limit.attrib.get('common_id')
                limit_common_id_1 = limit.attrib.get('common_id')
                # print(parameter_common_id)
                # print('for2')
                flag_3=0
                for products in limit.findall('products/'):
                    SES200M1 = products.tag
                    # print('for3')
                    if SES200M1 =='SES200M' and flag_3==0:
                        self.units = products.attrib.get('cb')
                        # print('for4')
                        if ((self.units == 'BU_50') or (self.units == 'BU_SES')or (self.unit == 'BU_400')):
                            if limit_common_id == None:
                                limit_common_id = self.count1 + 1
                            self.count1 = int(limit_common_id)
                            # print('for5')
                            flag_3=1
                            self.count =self.count+1
                            # print(limit_designation)
                            if limit_common_id_1 != None: self.lst_com_id.append(limit_common_id_1)
                            if limit_common_id_1 !=None:
                                if self.flag_1 ==0:
                                    prm_com_id = int(limit_common_id_1)
                                    self.flag_1 = 1
                                elif self.flag_1 ==1:
                                    prm_com_id_1 = int(limit_common_id_1)
                                    self.flag_1=0
                                    self.flag_2 = 1
                                if self.flag_2==1:
                                    if prm_com_id >=prm_com_id_1:
                                        print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                                    self.flag_2=2
                                elif self.flag_2==2:
                                    if prm_com_id_1 >=prm_com_id:
                                        print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                                    self.flag_1=1
                                    self.flag_2 = 0
                            # file.write(parameter_designation + parameter_common_id + "\n")
                           # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                           #            str(count1) + " p " + str(count) + "\n")
                            self.file.write('// '+ limit_name + '\n'+ limit_designation +" "+ "KEY("+ str(limit_common_id)+ ")"+ " " + "\n")

                            # print(lst_com_id)


        self.file.close()

