from bs4 import BeautifulSoup
import requests
#from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import re, csv

# response = requests.get('url', auth = HTTPBasicAuth('ypur_login', 'your_password'))

# URL = 'https://www.exist.ru/Catalog/Accessory/Cars/'
marka = []
comment = []
date = []
lst = []
count1 = 1
count = -1
URL = 'https://auto.exist.ru/otzyvy?page=1'
while(count1<3):
    print(URL)
    page = requests.get(URL)
    # print(page.status_code)
    # print(page.text)
    soup = BeautifulSoup(page.text, 'html.parser')
    [comment.append(rev.text) for rev in soup.find_all('p', class_ = 'responses-text')]
    # reviews_1 = soup.find_all('div', class_ = 'responses-content')
    # print(marka_1.find_all('div',class_ = 'responses-content'))
    marka_1 = BeautifulSoup(page.text, 'html.parser')
    [marka.append(hh.h3.text) for hh in marka_1.find_all('div',class_ = 'responses-content')]
    [date.append(dates.text) for dates in soup.find_all(style = 'float: right')]
    print(len(comment))
    print(comment)
    print(len(marka))
    print(marka)
    print(len(date))
    print(date)
    #-------------------------------------------------------------------------------------------
    for i in range(5):
        count=count+1
        lst.append([marka[count],';',date[count],';',comment[count]])
    print(lst)
    URL = URL.replace(str(count1), str(count1 + 1))
    count1 = count1 + 1
    #-------------------------------------------------------------------------------------------
head_myData = [["auto" ';' "date comment" ';' 'comment']]
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
# lt = []
# lt1 = [1,2,3,4,5,6]
# lt2 = [7,8,9,0]
# count2 = 0
# while(count2<4):
#     [lt.append(i) for i in lt1]
#     count2 =count2+1
# print(lt)

import csv

header = ['name'';' 'area'';' 'country_code2'';' 'country_code3']
data = ['Afghanistan'';' '652090' ';' 'AF'';' 'AFG']


with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerow(data)
