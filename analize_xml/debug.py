from goto_py import goto

a = [1, 2, 3, 4, 5, 6, 7, 8, 9]

for i in a:
    i = i + 1
    print(i)
print('i1=', i)
for i in a:
    goto(5, once_only=True)
    print('i1=', i)
