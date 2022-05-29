from bs4 import BeautifulSoup
import requests
#from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import re

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
for rev in reviews:
    print(rev.text)

#find_all
# a_tags = soup.find_all('p')
# print(type(a_tags))
# print(len(a_tags))
# print(a_tags)
#Получение всех ссылок
# for ref in a_tags:
#     print(ref.get('class'))


import csv

myData = [["first_name", "second_name", "Grade"],
          ['Alex', 'Brian', 'A'],
          ['Tom', 'Smith', 'B']]

myFile = open('example2.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(myData)

print("Writing complete")

import csv

header = ['name', 'area', 'country_code2', 'country_code3']
data = ['Afghanistan', 652090, 'AF', 'AFG']


with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerow(data)