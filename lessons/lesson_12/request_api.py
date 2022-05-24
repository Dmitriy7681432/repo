import requests,pprint

url = 'https://neuraluniversity.getcourse.ru/teach/control/lesson/view/id/113738391'
response = requests.get(url)
print(type(response),dir(response))
print(response.status_code)
print(response.text)