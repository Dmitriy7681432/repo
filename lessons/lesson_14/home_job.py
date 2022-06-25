from bs4 import BeautifulSoup
import requests
# from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import re, csv
import unicodedata

# response = requests.get('url', auth = HTTPBasicAuth('ypur_login', 'your_password'))

# URL = 'https://www.exist.ru/Catalog/Accessory/Cars/'
marka = []
comment = []
date = []
positive = []
negative = []
my_opinion = []
lst = []
count1 = 46
count = -1
flag =0; cnt2=0; cnt1=[];cnt=0;cnt3=0
URL = 'https://auto.exist.ru/otzyvy?page=46'
while (count1 < 48):
    print(URL)
    page = requests.get(URL)
    # print(page.status_code)
    # print(page.text)
    soup = BeautifulSoup(page.text, 'html.parser')
    # [comment.append(rev.text) for rev in soup.find_all('p', class_='responses-text')]
    for i in soup.find_all('a', class_='readmore'):
        page1 = requests.get(i.get('href'))
        soup1 = BeautifulSoup(page1.text, 'html.parser')
        ad = soup1.find_all('div', class_='error-title')
        if ad ==[]:
            cnt=cnt+1
            print('cnt=',cnt)
        elif ad != []:
            cnt1.append(cnt+1)
            print('cnt1=',cnt1)
        try:
            com = soup1.find('div', class_='review-text').find('div')
            mpa = dict.fromkeys(range(32))  # Удаление управлящих символов
            comment.append(com.text.translate(mpa))


            pos = soup1.find('div', class_='grid_12 alpha omega blockFormat Positive').find('div', class_='block_item')
            mpa1 = dict.fromkeys(range(32))  # Удаление управлящих символов
            positive.append(pos.text.translate(mpa1))
            # print(pos)
            neg = soup1.find('div', class_='grid_12 alpha omega blockFormat Negative').find('div', class_='block_item')
            mpa2 = dict.fromkeys(range(32))  # Удаление управлящих символов
            negative.append(neg.text.translate(mpa2))

            opin = soup1.find('div', class_='grid_12 alpha omega blockFormat').find('div', class_='block_item')
            mpa3 = dict.fromkeys(range(32))  # Удаление управлящих символов
            my_opinion.append(opin.text.translate(mpa3))
        except AttributeError:
            print('Отзыв удален')
            flag =flag +1


    # [marka.append(hh.h3.text) for hh in soup.find_all('div', class_='responses-content') if ad==[]]
    for hh in soup.find_all('div', class_='responses-content'):
        cnt2=cnt2+1
        print('cnt2=',cnt2)
        if flag!=0:
            for i in range(5):
                if cnt2!=:
                    marka.append(hh.h3.text)
        else: marka.append(hh.h3.text)
    # [date.append(dates.text) for dates in soup.find_all(style='float: right') if ad==[]]
    for dates in soup.find_all(style='float: right'):
        cnt3 = cnt3 + 1
        print('cnt3=',cnt3)
        if cnt3 != cnt1:
            date.append(dates.text)

    # print(len(comment))
    # print(comment)
    # print(len(marka))
    # print(marka)
    # print(len(date))
    # print(date)
    # print(len(positive))
    # print(positive)
    # print(len(negative))
    # print(negative)
    # print(len(my_opinion))
    # print(my_opinion)
    # -------------------------------------------------------------------------------------------
    for i in range(5-flag):
        count = count + 1
        lst.append([marka[count], date[count], comment[count], positive[count], negative[count], my_opinion[count]])
    # print(lst)
    flag =0;cnt2=0;cnt1=[0,0,0,0,0];cnt=0;cnt3=0
    URL = URL.replace(str(count1), str(count1 + 1))
    count1 = count1 + 1
    # -------------------------------------------------------------------------------------------
head_myData = [["auto", "date comment", 'comment', 'positive', 'negative', 'my opinion']]
myFile = open('example2.csv', 'w', encoding='utf-32', newline='')
# csv.register_dialect('my_dialect',delimiter='\t',doublequote=';',escapechar=':',skipinitialspace='True')
# csv.register_dialect('my_dialect',delimiter = '\t',doublequote=True)
with myFile:
    # for data in a:
    # print(data)
    # writer = csv.writer(myFile,quotechar=',', quoting=csv.QUOTE_MINIMAL)
    writer = csv.writer(myFile, delimiter='\t')
    # writer = csv.writer(myFile,'my_dialect')
    writer.writerows(head_myData)
    writer.writerows(lst)
print("Writing complete")
# -------------------------------------------------------------------------------------------
