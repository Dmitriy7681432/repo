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
comment = [rev.text for rev in soup.find_all('p', class_ = 'responses-text')]
# reviews_1 = soup.find_all('div', class_ = 'responses-content')

print(comment)
print('--'*50)
# print(marka_1.find_all('div',class_ = 'responses-content'))
marka_1 = BeautifulSoup(page.text, 'html.parser')
marka = [hh.h3.text for hh in marka_1.find_all('div',class_ = 'responses-content')]
print(marka)
print('--'*50)
date = [dates.text for dates in soup.find_all(style = 'float: right')]
print(date)
print('--'*50)
#-------------------------------------------------------------------------------------------
list_temp = []
list_csv =[]
# list_csv= [list_temp.append(i,j) for i,j in marka]
    # list_temp.append(i)
    # list_temp.append(j)
    # list_csv.append(list_temp)
count =0
for i in marka:
    list_temp.append(i)
    print(list_temp,'0')
    for j in date[count:]:
        list_temp.append(j)
        print(list_temp,'1')
        list_csv.append(list_temp)
        print(list_csv)
        list_temp.clear()
        count = count+1
        break
print(list_csv)

a = [1,2]
b = [3,4]
c = []
c.append(a)
c.append(b)
c.clear()
c.append(b)
print(c)

alex = 'Alex'
brian = 'Brian'
tom = 'Tom'
smith = 'Smith'

head_myData = ["auto" ';' "date comment" ';' 'comment']
myData =  [['Alex' ';' 'Brian' ';',comment[0]],
          ['Tom' ';' 'Smith' ';', comment[1]],
          ['Tom' ';' 'Smith' ';', comment[2]]]
print(myData)
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
#-------------------------------------------------------------------------------------------

import csv

header = ['name'';' 'area'';' 'country_code2'';' 'country_code3']
data = ['Afghanistan'';' '652090' ';' 'AF'';' 'AFG']


with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerow(data)
