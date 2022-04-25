import apiai,json

token = '7ba78803999945e5f3b9c305a8676af9e2ea18a1'
token = 'nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC'
request = apiai.ApiAI(token).text_request()
request.lang = 'ru'
message = input('Введите сообщение:')
request.query =message
responseJson = json.loads(request.getresponse().read().decode('utf-8'))
print(responseJson)