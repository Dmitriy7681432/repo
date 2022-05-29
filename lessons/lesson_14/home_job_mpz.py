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

csv.re

myData = [["auto" ';' "comment" ';' 'date comment'],
          ['Alex' ';' 'Brian' ';'],
          ['Tom' ';' 'Smith' ';' 'B']]
myData[1].append(str(comment[0]))
print(myData,'--------------------')
a = []
for a1 in myData:
    a.append(a1)
print(a,'=============')
myFile = open('example2.csv', 'w', newline='')
for er in myData[1]:
    print(er,'+++++++++++')

with myFile:
    for data in a:
            # data.remove(',')
            print(data)
            writer = csv.writer(myFile)
            writer.writerow(data)
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
