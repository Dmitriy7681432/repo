from bs4 import BeautifulSoup
import requests
# from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import re, csv
import unicodedata

# response = requests.get('url', auth = HTTPBasicAuth('ypur_login', 'your_password'))

# URL = 'https://www.exist.ru/Catalog/Accessory/Cars/'
marka = []
year = []
comment = []
date = []
positive = []
negative = []
my_opinion = []
lst = []
# max =559
count1 = 1
count = -1
flag =0; cnt1=[];cnt=0;cnt3=0;error_page=0
URL = 'https://auto.exist.ru/otzyvy?page=1'
while (count1 < 3):
    print(URL)
    page = requests.get(URL)
    # print(page.status_code)
    # print(page.text)
    soup = BeautifulSoup(page.text, 'html.parser')
    er_page= soup.find('div', class_="infoBlock3 marginBottom30").find('p')
    if er_page.text[10:28] =='Отзывов не найдено':
        error_page =1
    if error_page==0:
        for i in soup.find_all('a', class_='readmore'):
            page1 = requests.get(i.get('href'))
            soup1 = BeautifulSoup(page1.text, 'html.parser')
            ad = soup1.find_all('div', class_='error-title')

            if ad ==[]:
                cnt=cnt+1
                # print('cnt=',cnt)
            elif ad != []:
                cnt=cnt+1
                cnt1.append(cnt)
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

                # print('AAAAAAAAAAAAAAA', soup1.title.text)
                pattern = r'\w+'
                # pattern = r'[^Отзыв о Auto.Exist]\w+'
                marka.append(' '.join((re.findall(pattern, soup1.title.text))[2:-3]))
                year.append((re.findall(pattern, soup1.title.text))[2:-2][-1])
            except AttributeError:
                print('Отзыв удален')
                flag =flag +1

        #Бывает так, когда парсишь страницу некоторые отзывы удалены, а дату их нельзя добавлять в список
        # поэтому приходится что-то додумаывать с помощью флагов
        for dates in soup.find_all(style='float: right'):
            cnt3 = cnt3 + 1
            # print('cnt3=',cnt3)
            if flag==1:
                if cnt3 == cnt1[0]: pass
                else:date.append(dates.text)
            if flag==2:
                if cnt3 == cnt1[0] or cnt3==cnt1[1]:pass
                else:date.append(dates.text)
            if flag==3:
                if cnt3 == cnt1[0] or cnt3==cnt1[1] or cnt3==cnt1[2]: pass
                else:date.append(dates.text)
            if flag==4:
                if cnt3 == cnt1[0] or cnt3==cnt1[1] or cnt3==cnt1[2] or cnt3==cnt1[3]: pass
                else:date.append(dates.text)
            if flag==5:
                if cnt3 == cnt1[0] or cnt3==cnt1[1] or cnt3==cnt1[2] or cnt3==cnt1[3]or cnt3==cnt1[4]: pass
                else:date.append(dates.text)
            elif flag ==0:date.append(dates.text)

        for i in range(5-flag):
            count = count + 1
            lst.append([marka[count], year[count], date[count], comment[count], positive[count], negative[count], my_opinion[count]])
        # print(lst)

    flag =0;cnt1=[];cnt=0;cnt3=0;error_page=0
    URL = URL.replace(str(count1), str(count1 + 1))
    count1 = count1 + 1
    # -------------------------------------------------------------------------------------------
head_myData = [["auto","year of manufacture", "date comment", 'comment', 'positive', 'negative', 'my opinion']]
myFile = open('example2.csv', 'w', encoding='utf-32', newline='')
# csv.register_dialect('my_dialect',delimiter='\t',doublequote=';',escapechar=':',skipinitialspace='True')
# csv.register_dialect('my_dialect',delimiter = '\t',doublequote=True)
print(lst)
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
