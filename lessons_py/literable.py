f = open('C:/Users/Дмитрий/PycharmProjects/project01/lessons_py/text.txt', 'r', encoding='UTF-8')
# f = open('C:/text.txt', 'r', encoding='UTF-8')
text = f.read()
f.close()

#Задача 1
znak = [',','«','»','.','?','!','—',';',':']

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
# c = dict((x,map_text.count(x)) for x in map_text)
c =iter(c)
for x in map_text:
     c=dict(map_text.count(x))
print(c)
# for i in ls:
#      print(ls.count(i))
# print(dict_text)
