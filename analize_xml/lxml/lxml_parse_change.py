# -*- coding: utf-8 -*-
from lxml import etree

#Изменение xml
def parseXML(xmlFile):

    doc = etree.parse(xmlFile)
    for setting in doc.findall('.//can'):
        puprose = setting.attrib.get('puprose')
        if puprose =="XML_VERSION":
            value = setting.attrib.get('value')
            setting.attrib['value'] = '00020000'
            print(value)

    doc.write('params.xml',encoding='utf-8')

if __name__ == "__main__":
    parseXML("params.xml")



# import xml.etree.ElementTree as ET
#
# tree = ET.parse('params.xml')
# root = tree.getroot()
#
# value =0
# for setting in root.findall('.//can'):
#     puprose = setting.attrib.get('puprose')
#     if puprose == "XML_VERSION":
#         value = setting.attrib.get('value')
#         setting.set('value','00010004')
#
#
#     print(int(value))
#
# tree.write('params.xml',encoding='utf-8',short_empty_elements=True)