import random
#Задача 1
# 1. Напишите функцию (F): на вход список имен и целое число N;
# на выходе список длины N случайных имен из первого списка
# (могут повторяться, можно взять значения: количество имен 20, N = 100,
# рекомендуется использовать функцию random);
print('Задача 1')
def func (items_name,n):
    c = []
    for i in range((n)):
        b=random.choice(items_name)
        c.append(b)
    return c

func_output = func(['Igor','Sergeq','Vitaliy','Roma','Pasha','Sveta','Egor','Aleksey','Sasha','Volodya'],100)
print(func_output)
print(len(func_output))
print('-'*100)

#Задача 2
# 2. Напишите функцию вывода самого частого имени из списка на выходе функции F;
print('Задача 2')
def func_list(list_func):
    count_func = dict((x, list_func.count(x)) for x in list_func)
    print(count_func)
    list_count_func = list(count_func.items())
    list_count_func.sort(key=lambda i: i[1], reverse=True)
    print(list_count_func)
    for i in list_count_func[:1]:
        return i[0]

func1 = func_list(func_output)
print(func1)
print('-'*50)
#Задача 3
# 3. Напишите функцию вывода самой редкой буквы, с которого начинаются имена в списке на выходе функции F.
print('Задача 3')

def func_simvol(a):
    sl = []
    # for i in a:
    for i in func_output:
        # for j in i:
        sl.append(i[0])
    # print(sl)
    ls1 = dict((x, sl.count(x)) for x in sl)
    ls2 = list(ls1.items())
    ls2.sort(key=lambda i:i[1])
    print(ls2)
    for i in ls2[:1]:
        # print(i[0])
        return i[0]
ds = func_simvol(func_output)
print(ds)

#Задача 4
# 4.  В файле с логами найти дату самого позднего лога (по метке времени): https://drive.google.com/open?id=1pKGu-u2Vvtx4xK8i2ZhOzE5rBXyO4qd8

f = open('log','r',encoding='utf-8')
a = f.read()
print(a)

b = a.split('\n')
print(b)
c = sorted(b,reverse=True)
print(c[0])
d=[]
for i in c[0]:
    if i.isalpha():
        break
    d.append(i)
print(''.join(d)[:-2])
f.close()

e = [1,2,3,4,5,6,7,8,9,0]
v = list(e)
print(v)


# a = '2011'
# b = sorted(a,reverse=True)
# c =''.join(b)
# print(c)






# with open('log', mode='rt', encoding='utf-8') as f:
#     text = f.read()
# print(text, '\n')
#
# text = text.split('\n')
# last_log = max(text, key=lambda x: x[:23])
# print('Cамый поздний лог:', last_log)
# print('И его метка времени:', last_log[:23])