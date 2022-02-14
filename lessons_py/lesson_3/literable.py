# f = open('C:/Users/Дмитрий/PycharmProjects/project01/lessons_py/lesson_3/text.txt', 'r', encoding='UTF-8')
f = open('../lesson_3/text.txt', 'r', encoding='UTF-8')
text = f.read()
f.close()

#Задача 1
# 1) методами строк очистить текст от знаков препинания;
print('Задача 1')
znak = [',','«','»','.','?','!','—',';',':']
for i in znak:
     text = text.replace(i,'')
print(text)

#Задача 2
# 2) сформировать list со словами (split);
print('Задача 2')
list_text = list(text.split())
print(list_text)

#Задача 3
# 3) привести все слова к нижнему регистру (map);
print('Задача 3')
map_text = list(map(str.lower,list_text))
print(map_text)

#Задача 3
# 3) получить из list пункта 3 dict, ключами которого являются слова, а значениями их количество появлений в тексте;
# ls = ['hello','say','pow','hello','say']
# dict_text = dict.fromkeys(ls,2)
print('Задача 3')
dict_text = dict((x,map_text.count(x)) for x in map_text)
print(dict_text)

#Задача 4
# 4) вывести 5 наиболее часто встречающихся слов (sort), вывести количество разных слов в тексте (set).
print('Задача 4')
list_dict_text = list(dict_text.items())
print(list_dict_text)
list_dict_text.sort(key=lambda i: i[1],reverse=True)
print(list_dict_text)
for i in list_dict_text[:5]:
     print(i[0])
set_list_text = set(list_dict_text)
print(len(set_list_text))
#Либо так
# r = []
# for j in set_list_text:
#      r.append(j[0])
# t = set(r)
# print(t)
# print('__________________________________________________')
# a = (('hello',1),('lol',1),('hello',2))
# b = set(a)
# c=[]
# for i in b:
#      c.append(i[0])
# e =set(c)
# print(len(e))

#Задача 5
# 5) выполнить light с условием: в пункте 2 дополнительно к приведению к нижнему регистру выполнить лемматизацию.
print('Задача 5')
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
p=morph.parse('стали')
# for i in dict_text:
#      for j in morph.parse(i):
          # print(j)
print(map(p))