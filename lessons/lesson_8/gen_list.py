# Тернарный оператор

age = 17

def check_adult(age):
    check = 0
    if age >= 18:
        check = 1
    else:
        check = 0
    return check

check_adult_l = lambda x: 1 if age >=18 else 0

check = 1 if age >=18 else 0

print(check_adult(age), check, check_adult_l (age))

# Генераторы последовательностей


# Список
list_sq = []

N = 10

for i in range(1, N+1):
    if (i**2)%2 == 0:
        list_sq.append((i**2))
print(list_sq)

list_sq_g = [i**2 for i in range(1, N+1) if (i**2)%2 == 0]

print(list_sq_g)

# Словарь

dict_g = {i:i**2 for i in range(1, N+1) }
print(dict_g)

# Множество

set_g = {i**2 for i in range(1, N+1) }
set_g_d = {(i**2)%10 for i in range(1, N+1) }

print(set_g, set_g_d)


# Задача
list_names = ['Dima', 'kate', 'Oleg', 'natali']

# Сформировать список из первых букв так, чтобы они были заглавные

list_char = [ x[0] if x[0].isupper() else x[0].title() for x in list_names]

print(list_char)