import xml.etree.ElementTree as ET
import csv


def unique(iter):
    args = []
    for a in iter:
        if a not in args:
            args.append(a)
            yield a

def main():
    
    tree = ET.parse('params.xml')
    root = tree.getroot()
    SES150 = 0
    params_xml_list =[]
    preset_xml_list =[]
    for preset in root.findall('.//setting'):
        preset_number = preset.attrib.get('number')
        preset_designation = preset.attrib.get('designation')
        preset_dimension = preset.attrib.get('dimension')
        preset_default_value = preset.attrib.get('default_value')
        preset_name = preset.attrib.get('name')
        preset_type = preset.attrib.get('type')
        for products in preset.findall('products/'):
            SES150_1 = products.tag
            if SES150_1 =='SES150':
                SES150 = products.attrib.get('cb')
                if (SES150 == 'BU_SES'):
                    params_xml_list.append([preset_number,preset_designation,preset_dimension,preset_default_value])
                    # print(preset_number)
    #--------------------------------------------------------------------------------------------
    # print(params_xml_list)
    # print('Количество уставок с повторениями =',len(params_xml_list))
    preset_xml_list.append(list(unique(params_xml_list)))
    # print(*preset_xml_list)
    # print('Количество уставок с неповторениями = ',len(*preset_xml_list))
    #--------------------------------------------------------------------------------------------

    ##Запись в h
    myFile = open('presets.h', 'w', encoding='utf-32', newline='')
    with myFile:
        myFile.write('Hello')
    ##Запись в csv
    #head_myData = [["Number","Designation", "Dimension", "Default_value"]]
    #myFile = open('presets.csv', 'w', encoding='utf-32', newline='')
    #with myFile:
    #    writer = csv.writer(myFile, delimiter='\t')
    #    writer.writerows(head_myData)
    #    writer.writerows(*preset_xml_list)
    #    # writer.writerows(params_xml_list)
    ##print("Writing complete")
    #print("Update count_presets.csv")

if __name__ == "__main__":
    main()
