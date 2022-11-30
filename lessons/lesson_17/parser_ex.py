from bs4 import BeautifulSoup
import requests,time
from selenium import webdriver
from selenium.webdriver.common.by import By

browser =webdriver.Chrome()
browser.get('https://www.ozon.ru/category/odeyala-15081/')

time.sleep(3)
FILTER_OZON = '//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[1]/aside/div[9]/div[2]/div/span[1]/label'
filters = browser.find_elements(by=By.CLASS_NAME, value='ui-p ui-p3 ui-q jaa3 aja3')
# classname = filters.get_attribute('class')
# filter = browser.find_element(by=By.CSS_SELECTOR, value=f"label[class='{classname}']")
# filter_ozon= browser.find_elements(by=By.CSS_SELECTOR, value=f"div[class='{classname}']")
# filter_ozon.click()
print(filters)
# for filter in filters:
#     print("Hel")
#     print(filter.text)
# time.sleep(3)

#Поиск цены
# XPATH_PRICE = '//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[1]/div[1]/div[1]/div[1]'
XPATH_PRICE= '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[1]/div[1]/div[1]/div[1]'
elements = browser.find_elements(by=By.XPATH, value=XPATH_PRICE)
classname = elements[0].get_attribute('class')
prices= browser.find_elements(by=By.CSS_SELECTOR, value=f"div[class='{classname}']")

print(len(prices))
for element in prices:
    print(element.text)






# #Кликнуть ссылки не совсем пока правильно работает, так как сликом глубоко леземе через Selenium,
# необходимо открывать в новой вкладке или окне
# XPATH_LINKS = '//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[1]/a'
# elements = browser.find_elements(by=By.XPATH, value=XPATH_LINKS)
# classname = elements[0].get_attribute('class')
# links= browser.find_elements(by=By.CSS_SELECTOR, value=f"div[class='{classname}']")
#
# print(len(prices))
# for element in prices:
#    element.click()



time.sleep(1)
browser.close()










#
# def fetch(url, params):
#     headers = params["headers"]
#     body = params['body'].encode('utf-8')
#     if params['method']=="GET":
#        return requests.get(url, headers=headers)
#     if params['method']=="POST":
#        return requests.post(url, headers=headers, data=body)
#
# moscow = fetch("https://api.domofond.ru/rpc", {
#   "headers": {
#     "accept": "*/*",
#     "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
#     "content-type": "text/plain",
#     "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-site",
#     "cookie": "dfuid=3d59ede0-c51d-4af0-9419-32a4bf5afc74; _ga=GA1.2.1906160829.1664204030; _gid=GA1.2.1360133603.1664204030; rrpvid=219160291579449; cto_bundle=E1gVeF83VUYlMkZCWVpIVk5YUUpUb3ZBUEVSQUJtNmI4enhLJTJCT2lMekZLZHZqWFFsTFpIU2dZZkQ3QWVZUnVsZkRrJTJCRnZJRkZPT1RVanZqZ3RoTWt0cTVDbk95UFpuU21QT0tjbUhRb0lvYXY1NTJsaCUyRlNWTTkyRUdTSXpRdXMlMkJmZ0ZHcCUyQko0MEkxeiUyQkR5b2xrYnU3bEo2Rks3QSUzRCUzRA; rcuid=605636b23f17ff0001cd9af0; _gat=1",
#     "Referer": "https://www.domofond.ru/",
#     "Referrer-Policy": "strict-origin-when-cross-origin"
#   },
#   "body": "{\"id\":\"1\",\"jsonrpc\":\"2.0\",\"method\":\"Item.SearchItemsV3\",\"params\":{\"meta\":{\"platform\":\"web\",\"language\":\"ru\"},\"filters\":{\"itemType\":\"Sale\",\"propertyType\":\"Apartment\",\"priceFrom\":null,\"priceTo\":null,\"rooms\":[\"Three\"],\"apartmentMaterial\":[],\"constructionMaterial\":[],\"rentalRate\":null,\"floorFrom\":null,\"floorTo\":null,\"notLastFloor\":null,\"numberOfFloorsFrom\":null,\"numberOfFloorsTo\":null,\"distanceFromMetro\":null,\"itemSoldByType\":[],\"withPhotos\":false,\"withDeposit\":null,\"withCommission\":null,\"mapped\":false,\"apartmentSaleType\":null,\"houseDescription\":[],\"houseMaterial\":[],\"distanceToCityFrom\":null,\"distanceToCityTo\":null,\"plotAreaFrom\":null,\"plotAreaTo\":null,\"plotDescription\":[],\"commercialDescription\":[],\"constructionStage\":null,\"hasDevelopmentFinishing\":null,\"projectCompletionDateYearFrom\":null,\"projectCompletionDateYearTo\":null,\"developmentPropertyType\":[],\"isPartOfRenovationProgram\":null,\"publicationTimeRange\":null,\"maxCommissionPercentage\":null,\"floorAreaFrom\":null,\"floorAreaTo\":null,\"kitchenSizeFrom\":null,\"kitchenSizeTo\":null,\"livingSizeFrom\":null,\"livingSizeTo\":null,\"buildYearFrom\":null,\"buildYearTo\":null,\"geographicWindow\":null,\"geographicPolygon\":[],\"locations\":[{\"id\":3584,\"name\":\"Москва\",\"areaType\":\"City\",\"hasMetros\":true,\"hasDistricts\":false,\"HasRoads\":false}],\"searchText\":\"\",\"excludeSearchText\":\"\"},\"order\":\"Default\",\"offset\":0,\"limit\":27,\"thumbnailUrlSize\":{\"width\":508,\"height\":373}}}",
#   "method": "POST"
# });
# print(moscow.status_code)




















#
# opel =fetch("https://auto.ru/moskva/cars/opel/all/", {
#   "headers": {
#     "accept": "application/json",
#     "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
#     "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "x-csrf-token": "4bcefaab37743b086825305fbb06a63ea390c34607525639",
#     "x-requested-with": "XMLHttpRequest",
#     "x-susanin-react": "true",
#     "cookie": "suid=759b8eb4d296b851cad5d7e1b28f979c.464f4264d9190d342bf025cecae1ee1b; _csrf_token=4bcefaab37743b086825305fbb06a63ea390c34607525639; autoru_sid=a%3Ag63319fe42kc8asbe89b87qlolgkkrug.7d4cc723f464764a50a9a57d033a56bc%7C1664196580715.604800.QhEXzRdpjT2hZlI1zltnTg.RjbW4tSu2jmwkREMx86_iMWRNh9JQbO48qNaNNts4po; autoruuid=g63319fe42kc8asbe89b87qlolgkkrug.7d4cc723f464764a50a9a57d033a56bc; from=google-search; counter_ga_all7=1; yuidlt=1; yandexuid=5430543901611862534; my=YwA%3D; gdpr=0; _ym_isad=2; _ym_uid=16641965721000891258; _ym_visorc=b; spravka=dD0xNjY0MTk2NjE1O2k9OTQuMjUuMTc1LjUzO0Q9MDE3MDZCQ0YyQjdCMTEyNzlBNTZDNjI4NTE1NkUwQUFERkJCNEIyQzU0MzM4Q0YxOTFGNzgyMjY5OENEM0E2NTdCMDM5RTM5O3U9MTY2NDE5NjYxNTk4ODE0MTMzNDtoPTBjMjBmODA4OWIxMTliYzkxZWE4NDQ3NjA1ZTEzY2Ux; Session_id=noauth:1664196617; yandex_login=; ys=wprid.1659986136679882-13578828385488468951-sas3-0816-dd1-sas-l7-balancer-8080-BAL-2757#c_chck.2784033396; i=C8GyMosFUUsBOjYs7nYUMyOJ9y4ELL1s8vEzM/l96BEY8LHT4LaC5JU0rKdX54CQ6L0po3pRYu33pxUHN5b30e01zSA=; mda2_beacon=1664196617767; sso_status=sso.passport.yandex.ru:synchronized; cycada=VFg1K4efdUwHIaVgKtezeyi3/gL9kZfLyu8xzELZaHA=; _yasc=D/8rP8WIiuopjDZlTxYJdrAj+Oat11BXqA2JPlQCDi5grHaR; from_lifetime=1664197241884; _ym_d=1664197241; layout-config={\"win_width\":794,\"win_height\":650}",
#     "Referer": "https://auto.ru/moskva/",
#     "Referrer-Policy": "no-referrer-when-downgrade"
#   },
#   "body": None,
#   "method": "GET"
# });
#
# print(opel.status_code)
# print(opel.json().keys())
# cars = opel.json()['listing']['offers']
# [print(car['hash'])for car in cars]


# URL ="https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text=&clusters=true&enable_snippets=true&no_magic=true"
# URL = 'https://rarible.com/'
# print(URL)
# page = requests.get(URL)
# print(page.status_code)
# print(page.text)

#https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text#=&clusters=true&enable_snippets=true&no_magic=true
#
#https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text#=&clusters=true&enable_snippets=true&no_magic=true&page=1&hhtmFrom=vacancy_search_list

# serp-item__title
