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

def main(file_xml):
    tree = ET.parse(file_xml)
    root = tree.getroot()
    file = open('data_key2.txt', 'w+',encoding='utf-8')
    count = 0
    for unit in root.findall('.//unit'):
        unit_range = unit.attrib.get('range')
        unit_name = unit.attrib.get('name')
        count1=int(unit_range)
        com_id = int(unit_range)
        flag = 0
        flag_4 = 0
        for parameter in unit.findall('parameter'):
            parameter_designation = parameter.attrib.get('designation')
            parameter_name = parameter.attrib.get('name')
            parameter_type = parameter.attrib.get('type')
            parameter_common_id = parameter.attrib.get('common_id')
            flag_3=0
            for products in parameter.findall('products/'):
                product = products.tag
                if product =='SES200M' and flag_3==0:
                    SES200m = products.attrib.get('cb')
                    if flag_4 ==0:
                        file.write('\n' + '// Агрегат '+unit_name + '\n'+'\n')
                        flag_4=1
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
                            elif flag==2:
                                parameter_common_id = com_id + 1
                                com_id = parameter_common_id
                        else:
                            if flag==1: flag =2
                        count1 = int(parameter_common_id)
                        flag_3=1
                        count =count+1
                        hex_common_id = 'hex='+hex(int(parameter_common_id))[2:].upper() +' '
                        hex_flip_common_id = 'hex_flip= ' + func_val_to_hex_can_flip(int(parameter_common_id))
                        file.write('// '+ parameter_name + '\n'+ '#define KEY_' +parameter_designation + \
                                   ' ((uint32_t)('+ str(parameter_common_id)+ ")) " + hex_common_id + hex_flip_common_id + ' ' + "\n")

        for event in unit.findall('event'):
            event_designation = event.attrib.get('designation')
            event_name = event.attrib.get('name')
            event_common_id = event.attrib.get('common_id')
            flag_3=0
            for products in event.findall('products/'):
                product = products.tag
                if product =='SES200M' and flag_3==0:
                    SES200m = products.attrib.get('cb')
                    if ((SES200m == 'BU_50') or (SES200m == 'BU_SES')or (SES200m == 'BU_400')):
                        if event_common_id == None:
                            if flag ==1:
                                event_common_id = count1 + 1
                                com_id =event_common_id
                            elif flag==0:
                                event_common_id =com_id +300
                                com_id = event_common_id
                                flag=1
                            elif flag==2:
                                event_common_id = com_id + 1
                                com_id = event_common_id
                        else:
                            if flag==1: flag =2
                        count1 = int(event_common_id )
                        flag_3=1
                        count =count+1
                        hex_common_id = 'hex='+hex(int(event_common_id))[2:].upper() +' '
                        hex_flip_common_id = 'hex_flip= ' + func_val_to_hex_can_flip(int(event_common_id))
                        file.write('// '+ event_name + '\n'+ '#define KEY_' + event_designation + \
                                   ' ((uint32_t)('+ str(event_common_id) + ")) " + hex_common_id + hex_flip_common_id + ' ' + "\n")

        for limit in unit.findall('limit'):
            limit_designation = limit.attrib.get('designation')
            limit_name = limit.attrib.get('name')
            limit_common_id = limit.attrib.get('common_id')
            flag_3=0
            for products in limit.findall('products/'):
                product = products.tag
                if product =='SES200M' and flag_3==0:
                    SES200m = products.attrib.get('cb')
                    if ((SES200m == 'BU_50') or (SES200m == 'BU_SES')or (SES200m == 'BU_400')):
                        if limit_common_id == None:
                            if flag ==1:
                                limit_common_id = count1 + 1
                                com_id = limit_common_id
                            elif flag==0:
                                limit_common_id =com_id +300
                                com_id = limit_common_id
                                flag=1
                            elif flag==2:
                                limit_common_id = com_id + 1
                                com_id = limit_common_id
                        else:
                            if flag==1: flag =2
                        count1 = int(limit_common_id)
                        flag_3=1
                        count =count+1
                        hex_common_id = 'hex='+hex(int(limit_common_id))[2:].upper() +' '
                        hex_flip_common_id = 'hex_flip= ' + func_val_to_hex_can_flip(int(limit_common_id))
                        file.write('// '+ limit_name + '\n'+ '#define KEY_' + limit_designation + \
                                   ' ((uint32_t)('+ str(limit_common_id) + ")) " + hex_common_id + hex_flip_common_id + " " + "\n")


    for unit in root.findall('.//device'):
        unit_range = unit.attrib.get('range')
        unit_name = unit.attrib.get('name')
        count1=int(unit_range)-1
        flag_4 = 0
        for parameter in unit.findall('parameter'):
            parameter_designation = parameter.attrib.get('designation')
            parameter_name = parameter.attrib.get('name')
            parameter_type = parameter.attrib.get('type')
            parameter_common_id = parameter.attrib.get('common_id')
            flag_3=0
            for products in parameter.findall('products/'):
                product = products.tag
                if product =='SES200M' and flag_3==0:
                    SES200m = products.attrib.get('cb')
                    if flag_4 ==0:
                        file.write('\n' + '// Устройство '+unit_name + '\n'+'\n')
                        flag_4=1
                    if ((SES200m == 'BU_50') or (SES200m == 'BU_SES')or (SES200m == 'BU_400'))\
                    and ((parameter_type =='Измеряемый') or (parameter_type =='Вычисляемый')or
                    (parameter_type =='Внешний') or (parameter_type =='Дискретный')or
                    (parameter_type =='Сводный') or (parameter_type =='Команда')):
                        if parameter_common_id == None:
                            parameter_common_id = count1 + 1
                        count1 = int(parameter_common_id)
                        flag_3=1
                        count =count+1
                        hex_common_id = 'hex='+hex(int(parameter_common_id))[2:].upper() +' '
                        hex_flip_common_id = 'hex_flip= ' + func_val_to_hex_can_flip(int(parameter_common_id))
                        file.write('// '+ parameter_name + '\n'+ '#define KEY_' + parameter_designation + \
                                   ' ((uint32_t)('+ str(parameter_common_id) + ")) " + hex_common_id + hex_flip_common_id + " " + "\n")

        for event in unit.findall('event'):
            event_designation = event.attrib.get('designation')
            event_name = event.attrib.get('name')
            event_common_id = event.attrib.get('common_id')
            flag_3=0
            for products in event.findall('products/'):
                product = products.tag
                if SES200M1 =='SES200M' and flag_3==0:
                    SES200m = products.attrib.get('cb')
                    if ((SES200m == 'BU_50') or (SES200m == 'BU_SES')or (SES200m == 'BU_400')):
                        if event_common_id == None:
                            event_common_id = count1 + 1
                        count1 = int(event_common_id )
                        flag_3=1
                        count =count+1
                        hex_common_id = 'hex='+hex(int(event_common_id))[2:].upper() +' '
                        hex_flip_common_id = 'hex_flip= ' + func_val_to_hex_can_flip(int(event_common_id))
                        file.write('// '+ event_name + '\n'+ '#define KEY_' + event_designation + \
                                   ' ((uint32_t)('+ str(event_common_id) + ")) " + hex_common_id + hex_flip_common_id + " " + "\n")

        for limit in unit.findall('limit'):
            limit_designation = limit.attrib.get('designation')
            limit_name = limit.attrib.get('name')
            limit_common_id = limit.attrib.get('common_id')
            flag_3=0
            for products in limit.findall('products/'):
                SES200M1 = products.tag
                if SES200M1 =='SES200M' and flag_3==0:
                    SES200m = products.attrib.get('cb')
                    if ((SES200m == 'BU_50') or (SES200m == 'BU_SES')or (SES200m == 'BU_400')):
                        if limit_common_id == None:
                            limit_common_id = count1 + 1
                        count1 = int(limit_common_id)
                        flag_3=1
                        count =count+1
                        hex_common_id = 'hex='+hex(int(limit_common_id))[2:].upper() +' '
                        hex_flip_common_id = 'hex_flip= ' + func_val_to_hex_can_flip(int(limit_common_id))
                        file.write('// '+ limit_name + '\n'+ '#define KEY_' + limit_designation +
                                   ' ((uint32_t)('+ str(limit_common_id) + ")) " + hex_common_id + hex_flip_common_id + " " + "\n")

    file.close()

