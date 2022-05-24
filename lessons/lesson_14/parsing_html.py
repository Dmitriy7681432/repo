from bs4 import BeautifulSoup
import requests, re

URL = "https://www.drom.ru/reviews/volvo/v40/5kopeek/"

page = requests.get(URL)

print(page.status_code)
print(page.text)

soup = BeautifulSoup(page.text, 'html.parser')
print(type(soup))

print(soup.title) #вернет объект с первым тегом soup.teg