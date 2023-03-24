
import xml.etree.ElementTree as ET
import csv

tree = ET.parse('params.xml')
root = tree.getroot()

def unique(iter):
    args = []
    for a in iter:
        if a not in args:
            args.append(a)
            yield a

SEP30m = 0
params_xml_list =[]
a = []
preset_xml_list =[]
for preset in root.findall('.//parameter'):
    preset_number = preset.attrib.get('number')
    preset_designation = preset.attrib.get('designation')
    preset_dimension = preset.attrib.get('dimension')
    preset_default_value = preset.attrib.get('default_value')
    preset_name = preset.attrib.get('name')
    preset_type = preset.attrib.get('type')
    for products in preset.findall('products/'):
        SEP30m1 = products.tag
        if SEP30m1 =='SEP30M':
            SEP30m = products.attrib.get('cb')
    for products1 in preset.findall('.//SEP30M/'):
        calibr = products1.tag
        if calibr =='calibration' and SEP30m =='BU_SEP':
            print(calibr)
            print(preset_designation)
            print(preset_name)
            params_xml_list.append([preset_name, preset_designation+'_k'])
            params_xml_list.append([preset_name, preset_designation+'_b'])
#--------------------------------------------------------------------------------------------
# print(params_xml_list)
# print('Количество уставок с повторениями =',len(params_xml_list))
preset_xml_list.append(list(unique(params_xml_list)))
# print(*preset_xml_list)
# print('Количество уставок с неповторениями = ',len(*preset_xml_list))
#--------------------------------------------------------------------------------------------

#Запись в csv
head_myData = [["Name","Designation"]]
myFile = open('parametres.csv', 'w', encoding='utf-32', newline='')
with myFile:
    writer = csv.writer(myFile, delimiter='\t')
    writer.writerows(head_myData)
    writer.writerows(*preset_xml_list)
    # writer.writerows(params_xml_list)
print("Writing complete")

