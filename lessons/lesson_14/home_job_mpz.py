from bs4 import BeautifulSoup
import requests
#from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import re, csv

# response = requests.get('url', auth = HTTPBasicAuth('ypur_login', 'your_password'))

# URL = 'https://www.exist.ru/Catalog/Accessory/Cars/'
URL = 'https://auto.exist.ru/'

page = requests.get(URL)

print(page.status_code)
# print(page.text)
soup = BeautifulSoup(page.text, 'html.parser')
reviews = soup.find_all('p', class_ = 'responses-text')
print(len(reviews))
print(reviews)
comment = []
for rev in reviews:
    comment.append(rev.text)
print(comment[0])

#find_all
# a_tags = soup.find_all('p')
# print(type(a_tags))
# print(len(a_tags))
# print(a_tags)
#Получение всех ссылок
# for ref in a_tags:
#     print(ref.get('class'))
alex = 'Alex'
brian = 'Brian'
tom = 'Tom'
smith = 'Smith'
for 
head_myData = ["auto" ';' "comment" ';' 'date comment']
# myData =  [['Alex' ';' 'Brian' ';',comment[0]],
#           ['Tom' ';' 'Smith' ';', comment[1]],
#           ['Tom' ';' 'Smith' ';', comment[2]]]

a = []
for a1 in myData:
    a.append(a1)
myFile = open('example2.csv', 'w', newline='')
# csv.register_dialect('my_dialect',delimiter='\t',doublequote=';',escapechar=':',skipinitialspace='True')
with myFile:
    # for data in a:
            # print(data)
            writer = csv.writer(myFile,delimiter='\t')
            # writer = csv.writer(myFile,'my_dialect')
            writer.writerows(head_myData)
            writer.writerows(myData)
print("Writing complete")

print("Writing complete")

import csv

header = ['name'';' 'area'';' 'country_code2'';' 'country_code3']
data = ['Afghanistan'';' '652090' ';' 'AF'';' 'AFG']


with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerow(data)
