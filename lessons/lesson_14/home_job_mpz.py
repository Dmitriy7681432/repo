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
a = 'EEEEE'
myData = [["auto" ';' "comment" ';' 'date comment'],
          ['Alex' ';' 'Brian' ';', comment[0]],
          ['Tom' ';' 'Smith' ';' 'B']]

myFile = open('example2.csv', 'w')
with myFile:
    writer = csv.writer(myFile,)
    writer.writerows(myData)
print("Writing complete")

