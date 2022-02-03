f = open('text.txt','r', encoding='UTF-8')
text = f.read()
f.close()

#Задача 1
znak = ['-',',','«','»','.','?','!','—',';',':']

for i in znak:
     text = text.replace(i,'')
print(text)

#Задача 2
list_text = list(text.split())
print(list_text)

#Задача 3
map_text = list(map(str.lower,list_text))
print(map_text)

#Задача 4
from collections import Counter
ls = ['hello','say','pow','hello','say']
dict_text = dict.fromkeys(ls,2)
c = Counter(ls)
print(c.items())
# for i in ls:
#      print(ls.count(i))
# print(dict_text)
