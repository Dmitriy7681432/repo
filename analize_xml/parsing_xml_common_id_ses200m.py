import xml.etree.ElementTree as ET

# tree = ET.parse('appt.xml')
tree = ET.parse('example2.xml')
root = tree.getroot()



file = open('file1.txt', 'w+')
# # BBB
SES200m = 0
count = 0
count1 = 0
lst_com_id = []
flag_1=0
flag_2=0
for unit in root.findall('.//unit'):
    unit_range = unit.attrib.get('range')
    count1=int(unit_range)
    com_id = int(unit_range)
    flag = 0
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
                SES200m = products.attrib.get('cb')
                # print('for4')
                if ((SES200m == 'BU_50') or (SES200m == 'BU_SES')or (SES200m == 'BU_400'))\
                and ((parameter_type =='Измеряемый') or (parameter_type =='Вычисляемый')or
                (parameter_type =='Внешний') or (parameter_type =='Дискретный')or
                (parameter_type =='Сводный') or (parameter_type =='Команда')):
                    if parameter_common_id == None:
                        if flag ==1:
                            parameter_common_id = count1 + 1
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
                    count1 = int(parameter_common_id)
                    # print('for5')
                    flag_3=1

                    count =count+1
                    print(parameter_designation)
                    if parameter_common_id_1 != None: lst_com_id.append(parameter_common_id_1)
                    if parameter_common_id_1!=None:
                        if flag_1 ==0:
                            prm_com_id = int(parameter_common_id_1)
                            flag_1 = 1
                        elif flag_1 ==1:
                            prm_com_id_1 = int(parameter_common_id_1)
                            flag_1=0
                            flag_2 = 1
                        if flag_2==1:
                            if prm_com_id >=prm_com_id_1:
                                print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                            flag_2=2
                        elif flag_2==2:
                            if prm_com_id_1 >=prm_com_id:
                                print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                            flag_1=1
                            flag_2 = 0
                    # file.write(parameter_designation + parameter_common_id + "\n")
                   # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                   #            str(count1) + " p " + str(count) + "\n")
                    file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + "\n")

                    print(lst_com_id)
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
                SES200m = products.attrib.get('cb')
                # print('for4')
                if ((SES200m == 'BU_50') or (SES200m == 'BU_SES')or (SES200m == 'BU_400')):
                    if event_common_id == None:
                        if flag ==1:
                            event_common_id = count1 + 1
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
                    count1 = int(event_common_id )
                    # print('for5')
                    flag_3=1

                    count =count+1
                    print(event_designation)
                    if event_common_id_1 != None: lst_com_id.append(event_common_id_1)
                    if event_common_id_1!=None:
                        if flag_1 ==0:
                            prm_com_id = int(event_common_id_1)
                            flag_1 = 1
                        elif flag_1 ==1:
                            prm_com_id_1 = int(event_common_id_1)
                            flag_1=0
                            flag_2 = 1
                        if flag_2==1:
                            if prm_com_id >=prm_com_id_1:
                                print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                            flag_2=2
                        elif flag_2==2:
                            if prm_com_id_1 >=prm_com_id:
                                print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                            flag_1=1
                            flag_2 = 0
                    # file.write(parameter_designation + parameter_common_id + "\n")
                   # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                   #            str(count1) + " p " + str(count) + "\n")
                    file.write(event_designation +" "+ "KEY("+ str(event_common_id)+ ")"+ " " + "\n")

                    print(lst_com_id)


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
                SES200m = products.attrib.get('cb')
                # print('for4')
                if ((SES200m == 'BU_50') or (SES200m == 'BU_SES')or (SES200m == 'BU_400')):
                    if limit_common_id == None:
                        if flag ==1:
                            limit_common_id = count1 + 1
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
                    count1 = int(limit_common_id)
                    # print('for5')
                    flag_3=1

                    count =count+1
                    print(limit_designation)
                    if limit_common_id_1 != None: lst_com_id.append(limit_common_id_1)
                    if limit_common_id_1 !=None:
                        if flag_1 ==0:
                            prm_com_id = int(limit_common_id_1)
                            flag_1 = 1
                        elif flag_1 ==1:
                            prm_com_id_1 = int(limit_common_id_1)
                            flag_1=0
                            flag_2 = 1
                        if flag_2==1:
                            if prm_com_id >=prm_com_id_1:
                                print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                            flag_2=2
                        elif flag_2==2:
                            if prm_com_id_1 >=prm_com_id:
                                print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                            flag_1=1
                            flag_2 = 0
                    # file.write(parameter_designation + parameter_common_id + "\n")
                   # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                   #            str(count1) + " p " + str(count) + "\n")
                    file.write(limit_designation +" "+ "KEY("+ str(limit_common_id)+ ")"+ " " + "\n")

                    print(lst_com_id)

for unit in root.findall('.//device'):
    unit_range = unit.attrib.get('range')
    count1=int(unit_range)
    com_id = int(unit_range)
    flag = 0
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
                SES200m = products.attrib.get('cb')
                # print('for4')
                if ((SES200m == 'BU_50') or (SES200m == 'BU_SES')or (SES200m == 'BU_400'))\
                and ((parameter_type =='Измеряемый') or (parameter_type =='Вычисляемый')or
                (parameter_type =='Внешний') or (parameter_type =='Дискретный')or
                (parameter_type =='Сводный') or (parameter_type =='Команда')):
                    if parameter_common_id == None:
                        if flag ==1:
                            parameter_common_id = count1 + 1
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
                    count1 = int(parameter_common_id)
                    # print('for5')
                    flag_3=1

                    count =count+1
                    print(parameter_designation)
                    if parameter_common_id_1 != None: lst_com_id.append(parameter_common_id_1)
                    if parameter_common_id_1!=None:
                        if flag_1 ==0:
                            prm_com_id = int(parameter_common_id_1)
                            flag_1 = 1
                        elif flag_1 ==1:
                            prm_com_id_1 = int(parameter_common_id_1)
                            flag_1=0
                            flag_2 = 1
                        if flag_2==1:
                            if prm_com_id >=prm_com_id_1:
                                print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                            flag_2=2
                        elif flag_2==2:
                            if prm_com_id_1 >=prm_com_id:
                                print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                            flag_1=1
                            flag_2 = 0
                    # file.write(parameter_designation + parameter_common_id + "\n")
                   # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                   #            str(count1) + " p " + str(count) + "\n")
                    file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + "\n")

                    print(lst_com_id)
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
                SES200m = products.attrib.get('cb')
                # print('for4')
                if ((SES200m == 'BU_50') or (SES200m == 'BU_SES')or (SES200m == 'BU_400')):
                    if event_common_id == None:
                        if flag ==1:
                            event_common_id = count1 + 1
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
                    count1 = int(event_common_id )
                    # print('for5')
                    flag_3=1

                    count =count+1
                    print(event_designation)
                    if event_common_id_1 != None: lst_com_id.append(event_common_id_1)
                    if event_common_id_1!=None:
                        if flag_1 ==0:
                            prm_com_id = int(event_common_id_1)
                            flag_1 = 1
                        elif flag_1 ==1:
                            prm_com_id_1 = int(event_common_id_1)
                            flag_1=0
                            flag_2 = 1
                        if flag_2==1:
                            if prm_com_id >=prm_com_id_1:
                                print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                            flag_2=2
                        elif flag_2==2:
                            if prm_com_id_1 >=prm_com_id:
                                print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                            flag_1=1
                            flag_2 = 0
                    # file.write(parameter_designation + parameter_common_id + "\n")
                   # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                   #            str(count1) + " p " + str(count) + "\n")
                    file.write(event_designation +" "+ "KEY("+ str(event_common_id)+ ")"+ " " + "\n")

                    print(lst_com_id)


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
                SES200m = products.attrib.get('cb')
                # print('for4')
                if ((SES200m == 'BU_50') or (SES200m == 'BU_SES')or (SES200m == 'BU_400')):
                    if limit_common_id == None:
                        if flag ==1:
                            limit_common_id = count1 + 1
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
                    count1 = int(limit_common_id)
                    # print('for5')
                    flag_3=1

                    count =count+1
                    print(limit_designation)
                    if limit_common_id_1 != None: lst_com_id.append(limit_common_id_1)
                    if limit_common_id_1 !=None:
                        if flag_1 ==0:
                            prm_com_id = int(limit_common_id_1)
                            flag_1 = 1
                        elif flag_1 ==1:
                            prm_com_id_1 = int(limit_common_id_1)
                            flag_1=0
                            flag_2 = 1
                        if flag_2==1:
                            if prm_com_id >=prm_com_id_1:
                                print("Error com_id", prm_com_id, 'и', prm_com_id_1)
                            flag_2=2
                        elif flag_2==2:
                            if prm_com_id_1 >=prm_com_id:
                                print("Error com_id1", prm_com_id_1, 'и', prm_com_id)
                            flag_1=1
                            flag_2 = 0
                    # file.write(parameter_designation + parameter_common_id + "\n")
                   # file.write(parameter_designation +" "+ "KEY("+ str(parameter_common_id)+ ")"+ " " + \
                   #            str(count1) + " p " + str(count) + "\n")
                    file.write(limit_designation +" "+ "KEY("+ str(limit_common_id)+ ")"+ " " + "\n")

                    print(lst_com_id)


file.close()

