import json

dict_ex = {'brand': 'Volvo', 'Price': '1.5', 'Vol': 2.0}

# dump, dumps

dict_to_json = json.dumps(dict_ex)
print(type(dict_to_json), dict_to_json)

with open('dict_to_json.txt', 'w') as f:
    json.dump(dict_ex, f)

# load, loads
with open('dict_to_json.txt') as f:
    data = json.load(f)

print(type(data), data)

data_1 = json.loads(dict_to_json)
print(type(data_1), data_1)


# Реальный пример, ответ по API

import requests

response = requests.get("https://jsonplaceholder.typicode.com/todos")
data_2 = json.loads(response.text)
print(data_2)