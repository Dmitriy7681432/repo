import xml.etree.ElementTree as ET

# tree = ET.parse('appt.xml')
tree = ET.parse('example1.xml')
root = tree.getroot()


# №2
# neighbor =0
# for year in root.findall('./country/year'):
#     # year = country.find('year').attrib.get('name')
#     # atttrib = country.find('.//neighbor').attrib.get('name')
#     year_name = year.attrib.get('name')
#     # print(year_name)
#     for year1 in year.findall('year1/'):
#     # neighbor = year.find('year1')
#     # if name =='Malaysia':
#         neighbor = year1.attrib.get('name')
#         # neighbor1 = year1.tag
#         # print(neighbor)
#     # print(neighbor)
#     # if neighbor == 'Malaysia' or neighbor == 'Maiami'or neighbor == 'Vegas'or neighbor == 'Kazan':
#     #     print('LOL',year_name)
file = open('file.txt', 'w+')
# # BBB
SEP30M = 0
count = 0
for parameter in root.findall('.//parameter'):
    parameter_designation = parameter.attrib.get('designation')
    parameter_name = parameter.attrib.get('name')
    parameter_type = parameter.attrib.get('type')
    for products in parameter.findall('products/'):
        SEP30M1 = products.tag
        if SEP30M1 =='SEP30M':
            SEP30M = products.attrib.get('cb')
            if ((SEP30M == 'BU_SEP') or (SEP30M == 'BU_400')) and ((parameter_type =='Измеряемый')
            or (parameter_type =='Вычисляемый')or (parameter_type =='Внешний')
            or (parameter_type =='Дискретный')or (parameter_type =='Сводный')):
                count =count+1
                print(parameter_designation)
                file.write(parameter_designation + ", 0 - " + parameter_name+ "\n")
print(count)
file.close()