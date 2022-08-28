import xml.etree.ElementTree as ET

# tree = ET.parse('appt.xml')
tree = ET.parse('example2.xml')
root = tree.getroot()



file = open('file1.txt', 'w+')
# # BBB
SES200m = 0
count = 0
count1 = 0
flag =0
for unit in root.findall('.//unit'):
    unit_range = unit.attrib.get('range')
    count1=int(unit_range)
    print('for1')
    try:
        # for parameter in root.findall('.//parameter'):
        for parameter in root.find('.//parameter'):
            parameter_designation = parameter.attrib.get('designation')
            parameter_name = parameter.attrib.get('name')
            parameter_type = parameter.attrib.get('type')
            parameter_common_id = parameter.attrib.get('common_id')
            count1 = int(parameter_common_id)
            print('for2')
            for products in parameter.findall('products/'):
                SES200M1 = products.tag
                print('for3')
                if SES200M1 =='SES200M':
                    SES200m = products.attrib.get('cb')
                    print('for4')
                    if ((SES200m == 'BU_50') or (SES200m == 'BU_50')or (SES200m == 'BU_50'))\
                            and ((parameter_type =='Измеряемый')
                    or (parameter_type =='Вычисляемый')or (parameter_type =='Внешний')
                    or (parameter_type =='Дискретный')or (parameter_type =='Сводный')):
                        print('for5')
                        count =count+1
                        print(parameter_designation)
                        # file.write(parameter_designation + parameter_common_id + "\n")
                        file.write(parameter_designation +" "+ "KEY("+ parameter_common_id+ ")"+ " " + str(count1) + "\n")
                        # file.write(parameter_designation + ", 0 - " + parameter_name+ "\n")
    except TypeError:
        print("ERROR")
                        # if flag ==0:
                        #     count1=count1+300
                        #     flag =1
                        # file.write(parameter_designation + " " + "KEY(" + parameter_common_id + ")" + " " + str(count1) + "\n")
# print(count)
# print(len(params_xml_list))
# print(params_xml_list)
file.close()

