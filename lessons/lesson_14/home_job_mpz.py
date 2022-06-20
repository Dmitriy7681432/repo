from bs4 import BeautifulSoup
import requests
#from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import re, csv

# response = requests.get('url', auth = HTTPBasicAuth('ypur_login', 'your_password'))

# URL = 'https://www.exist.ru/Catalog/Accessory/Cars/'
# URL = 'https://auto.exist.ru/'
cnt=0
marka = []

while(cnt !=2):
    if cnt ==0:
        URL = 'https://auto.exist.ru/otzyvy?page=12'
    elif cnt ==1:
        URL = 'https://auto.exist.ru/otzyvy?page=2'
    page = requests.get(URL)
    print(page.status_code)
    # print(page.text)
    soup = BeautifulSoup(page.text, 'html.parser')
    comment = [rev.text for rev in soup.find_all('p', class_ = 'responses-text')]
    # reviews_1 = soup.find_all('div', class_ = 'responses-content')
    # print(marka_1.find_all('div',class_ = 'responses-content'))
    marka_1 = BeautifulSoup(page.text, 'html.parser')
    # marka = [hh.h3.text for hh in marka_1.find_all('div',class_ = 'responses-content')]
    [marka.append(hh.h3.text) for hh in marka_1.find_all('div',class_ = 'responses-content')]
    date = [dates.text for dates in soup.find_all(style = 'float: right')]
    # marka1 = []
    # for i in marka:
    #     marka1.append(i)
    print(marka)
    cnt = cnt + 1
    #-------------------------------------------------------------------------------------------
lst = []
count =-1
for i in range(4):
    count=count+1
    lst.append([marka[count],';',date[count],';',comment[count]])
print(lst)
#-------------------------------------------------------------------------------------------
head_myData = [["auto" ';' "date comment" ';' 'comment']]
myFile = open('example2.csv', 'w', newline='')
# csv.register_dialect('my_dialect',delimiter='\t',doublequote=';',escapechar=':',skipinitialspace='True')
csv.register_dialect('my_dialect',delimiter = '\a',doublequote=True)
with myFile:
    # for data in a:
            # print(data)
            # writer = csv.writer(myFile,quotechar=',', quoting=csv.QUOTE_MINIMAL)
            # writer = csv.writer(myFile,delimiter = '\t')
            writer = csv.writer(myFile,'my_dialect')
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
