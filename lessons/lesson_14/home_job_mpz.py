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
lst = []
count =0
count1 =0
flag = 0
for i in marka:
    i=i+';'
    list_temp.append(i)
    for j in date[count:]:
        if flag ==1:
            flag = 0
            break
        j=j+';'
        list_temp.append(j)
        count = count+1
        for k in comment[count1:]:
            list_temp.append(k)
            lst.append(list_temp)
            list_temp = []
            count1 = count1 +1
            flag = 1
            break
print(lst)
A = []
for i in range(3):
    for j in range(3):
        A[i][j] = 2

print(A,'AAAA')
#-------------------------------------------------------------------------------------------
head_myData = [["auto" ';' "date comment" ';' 'comment']]
myData =  [['Alex' ';' 'Brian' ';',comment[0]],
          ['Tom' ';' 'Smith' ';', comment[1]],
          ['Tom' ';' 'Smith' ';', comment[2]]]
print(myData)

myFile = open('example2.csv', 'w', newline='')
# csv.register_dialect('my_dialect',delimiter='\t',doublequote=';',escapechar=':',skipinitialspace='True')
# csv.register_dialect('my_dialect',delimiter = '\t',doublequote=True)
with myFile:
    # for data in a:
            # print(data)
            # writer = csv.writer(myFile,quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer = csv.writer(myFile,delimiter = '\t')
            # writer = csv.writer(myFile,'my_dialect')
            writer.writerows(head_myData)
            writer.writerows(lst)
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
