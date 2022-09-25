import xml.etree.ElementTree as ET

# tree = ET.parse('appt.xml')
tree = ET.parse('example2.xml')
root = tree.getroot()



# file = open('analize_xml/file1.txt', 'w+')
# # BBB
SES200m = 0
count = 0
params_xml_list =[]
for parameter in root.findall('.//parameter'):
    parameter_designation = parameter.attrib.get('designation')
    parameter_name = parameter.attrib.get('name')
    parameter_type = parameter.attrib.get('type')
    for products in parameter.findall('products/'):
        SES200M1 = products.tag
        if SES200M1 =='SES200M':
            SES200m = products.attrib.get('cb')
            if ((SES200m == 'BU_50') or (SES200m == 'BU_50')or (SES200m == 'BU_50'))\
                    and ((parameter_type =='Измеряемый')
            or (parameter_type =='Вычисляемый')or (parameter_type =='Внешний')
            or (parameter_type =='Дискретный')or (parameter_type =='Сводный')):
                count =count+1
                params_xml_list.append(parameter_designation)
                # print(parameter_designation)
                # file.write(parameter_designation + ", 0 - " + parameter_name+ "\n")
# print(count)
print(len(params_xml_list))
print(params_xml_list)
# file.close()


#_________________________________________________________________________________________
#Парсинг params.c
# file = open('C:/projects/TAKI00014-01/src/init/params.c', 'r', encoding='UTF-8')
file = open('params.c', 'r',encoding='utf-8')
text = file.readlines()
file.close()
# print(type(text))
text1 = (''.join(text)).split()
count =-1
prm_lst = []
for i in text1:
    if i =='init_params()':
        break
    count=count+1
    if i =='static' and text1[count+1] =='char' and text1[count+3] == '=' and text1[count-1]!='//' :
        prm_lst.append(text1[count+4])
prm_lst=((((';'.join(prm_lst)).replace(';;',' ')).replace('"','')).replace(';','')).split(' ')
print(prm_lst)
print((len(prm_lst)))
# lol1=(lol.replace(';;',' ').replace('"',''))
#_________________________________________________________________________________________


end_list=[]

for i in params_xml_list:
    if i not in prm_lst:
        end_list.append(i)
for i in prm_lst:
    if i not in params_xml_list:
        end_list.append(i)
print(end_list)
print(len(end_list))












# count=-1
# sad = ['Hello world in example\n How are you']
# spl=((''.join(sad)).split())
# print(spl)
# for i in spl:
#     count = count + 1
#     if i=="world":
#         print(spl[count])


# for i in "".join(sad):
#     print(i)