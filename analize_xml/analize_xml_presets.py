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
file = open('preset.txt','w+')
# # BBB
SEP30M = 0
count = 0
for setting in root.findall('.//setting'):
    designation = setting.attrib.get('designation')
    number = setting.attrib.get('number')
    dimension = setting.attrib.get('dimension')
    default_value = setting.attrib.get('default_value')
    for products in setting.findall('products/'):
        SEP30M1 = products.tag
        if SEP30M1 =='SEP30M':
            SEP30M = products.attrib.get('cb')
            if ((SEP30M == 'BU_SEP') or (SEP30M == 'BU_400')):
                count =count+1
                print(designation)
                file.write(number +' '+designation+' '+dimension+' '+default_value+ "\n")
print(count)
file.close()