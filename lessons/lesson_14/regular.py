import re

string = 'It was beatufil today,It was beatufil today,It was beatufil today,It was beatufil today.'

# pattern =r"was"

#finall поиск слова_____________________________
# print(len(re.findall(pattern, string)))

# [    ] поис букв_______________________________________
# pattern = r'[a]'
# pattern = r'[a-zA-z0-9]'
# pattern = r'[,]'
# print(re.findall(pattern, string))

#[ . ]_______________________
# pattern = r'[w]..'
# print(re.findall(pattern, string))


#Поиск спец символов

#\w- все кроме спец знаков
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

pattern = r'\W\w{2,4}\W' #поиск слов заданной длины
print(re.sub(pattern,r' ', string))