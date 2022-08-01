import requests,time,pprint

TOKEN = '5449407787:AAHs7AbrX9ygAab41TfoTRJ0Hp8c0uY1SdU'
BOT_URL = f'https://api.telegram.org/bot{TOKEN}'

proxies = {
    'http': 'http://173.245.49.25:80',
    # 'https': 'http://173.245.49.25:80',
}
url = f'{BOT_URL}/getMe'
result = requests.get(url, proxies = proxies)
# print(result.status_code)
# Справка bot api
# https://tlgrm.ru/docs/bots/api

url = f'{BOT_URL}/getUpdates'
while True:
    time.sleep(3)
    result = requests.get(url, proxies=proxies)
    pprint.pp(result.json())
    messages = result.json()['result']
    for message in messages:
        chat_id = message['message']['chat']['id']
        url_send = f'{BOT_URL}/sendMessage'
        params = {
                  'chat_id': chat_id,
                  'text': 'Добрый день!'
                  }
        answer= requests.post(url_send, params = params, proxies = proxies)