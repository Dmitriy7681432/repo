import re

# string = 'It was beatufil today,It was beatufil today,It was beatufil today,It was beatufil today.'
# string = 'Отзыв о Citroen C5 2115 2009 — Auto.Exist'
string = 'Отзыв о Audi A3 2012 — Auto.Exist'
# pattern =r"was"
# string = 'ruby'
#finall поиск слова_____________________________
# print(len(re.findall(pattern, string)))

# [    ] поис букв________________________________0_______
# pattern = r'[a]'
# pattern = r'[a-zA-z0-9]'
# pattern = r'[,]'
# pattern = r'[0-9]{4}' #Поиск цифр заданной длины
# pattern= r'(?:19[0-9][0-9]|20[0-3][0-9])'
#[ . ]____________________1___
# pattern = r'(19[0-9][0-9]|20[0-3][0-9])' #Поиск цифр заданной длины
# pattern = r'\d+[]'
pattern= r'\w+'
print(' '.join((re.findall(pattern, string))[2:-3]))

#[ . ]_______________________
# pattern = r'[w]..'
# print(re.findall(pattern, string))


#Поиск спец символов

#\ w- все кроме спец знаков
#\W- все спец знаки (тире, точки, запятые и т.д)
#\d - любая цифра
#\D- не цифра

# pattern = r'\w'
# print(re.findall(pattern, string))

#Поиск определенного количества заданных символов
#\d{n} - ровно n раз
#\d{n,} - более  n раз
#\d{n,m} - не менее n цифр, но не более m

# pattern = r'\W\w{2,4}\W' #поиск слов заданной длины
# print(re.findall(pattern, string))

#search_________________________________________________
#
# pattern = r'\W\w{2,4}\W' #поиск слов заданной длины
# print(re.search(pattern, string))

#sub_________________________________________

# pattern = r'\W\w{2,4}\W' #поиск слов заданной длины
# print(re.sub(pattern,r' ', string))
