from bs4 import BeautifulSoup
import requests
#from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import re

# URL = 'https://www.mvideo.ru/products/stiralnaya-mashina-uzkaya-beko-wspe7612w-20067847'
URL =  'https://www.mvideo.ru/products/stiralnaya-mashina-uzkaya-beko-wspe7612w-20067847'
# URL =  'https://www.drom.ru/reviews/volvo/v40/'
page = requests.get(URL)

print(page.status_code)
print(page.text)