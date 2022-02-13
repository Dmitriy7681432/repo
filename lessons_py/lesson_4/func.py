import random
#Задача 1
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
print('Задача 2')
# count_func = dict((x,func_output.count(x)) for x in func_output)
# print(count_func)
# list_count_func = list(count_func.items())
# list_count_func.sort(key=lambda i:i[1],reverse=True)
# print(list_count_func)
# for i in list_count_func[:1]:
#     print(i[0])
# print('func-----------------------------------')
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


#
# import random
#
# print()
# print("Задача 1. \nВыбор 100 случайных имен из списка")
# # 20 имен
# list_names = 'Natalia Ksenia Viola Ivan Kostya Kosmos Katya Darya Valya Nikita Serezha Vitya Sarah Petya Victor Seva Lyonya Maxim Vova Raya'.split()
#
#
# def name_n(list_names, n):
#     '''
#     :param list_names: список имен
#     :param n: длина списка на выходе
#     :return: список из 20 случайных имен
#     '''
#     list_names_random = []
#     len_list = len(list_names)
#     newName = ''
#
#     for i in range(1, n + 1):
#         # randomChoice - это случайное число в пределах длины начального списка,
#         # случайным образом выбираем индекс
#         randomChoice = random.randint(0, len_list-1)
#         # newName - это случайное слово по индексу
#         newName = list_names[randomChoice]
#         # Добавляем случайное слово newName в список
#         list_names_random.append(newName)
#
#     return list_names_random
#
# list_names_random = name_n(list_names, 100) # n == 100
# print('Список: \n%s\nКоличество слов: %s\nИзначально слов: %s' % (list_names_random, len(list_names_random), len(list_names)))
# print()
