def sorted_cards(a):
    print()
    for i in range(len(a)):
        if a[i] == '10' + u'\u2660':
            a[i] = 'A' + u'\u2660'
        if a[i] == '10' + u'\u2665':
            a[i] = 'A' + u'\u2665'
        if a[i] == '10' + u'\u2663':
            a[i] = 'A' + u'\u2663'
        if a[i] == '10' + u'\u2666':
            a[i] = 'A' + u'\u2666'
    a.sort()
    for i in range(len(a)):
        if a[i] == 'A' + u'\u2660':
            a[i] = '10' + u'\u2660'
        if a[i] == 'A' + u'\u2665':
            a[i] = '10' + u'\u2665'
        if a[i] == 'A' + u'\u2663':
            a[i] = '10' + u'\u2663'
        if a[i] == 'A' + u'\u2666':
            a[i] = '10' + u'\u2666'
    b =[]
    # for i in a:
    #     if
    print('Отсортировано', a)

b = ['8♣', '9♣', '10♥', 'Король♠', '7♠', 'Король♦']
c = ['10♥', '7♠', '8♣', '9♣', 'Король♠', 'Король♦']
sorted_cards(b)
print('10' + u'\u2665')
d = ''.join(c)
e = list(d)
print(d)
print(e)

if '8b'<'Валет':
    print(True)
else:
    print(False)

a = b.pop(0)
print(a)
print(b)
# a = input()
# print(a)
b = ['12a','2b','Корольf']
print('b=',b[1][:2])
if 'a' in ''.join(b):
    print('Yes',b[0])
print(b[1][-1:])
er = '14g'
print('er=',er[1][0])
if b[0]<b[1]:
    print('NO')

r = '21aВалет8106'
if r[:2] == '12':
    print('HELL')
print(r[:-1])
b.append('7f')
print(b)


import sys
func = sys._getframe().f_code.co_name

class Test:
    def func3(self):
        print(sys._getframe().f_code.co_name)

test = Test()
print(test.func3())
import traceback

stack = traceback.extract_stack()
# st = stack[-2][1]

def say_my_name():
    stack = traceback.extract_stack()
    print('Print from {}'.format(stack[-2][1]))
print(sys._getframe())
print(sys._getframe().f_lineno)
print(sys._getframe().f_lineno)

class Test1:

    def func_1(self):
        say_my_name()

    def func_2(self):
        say_my_name()

    def func_3(self):
        say_my_name()

    def func_4(self):
        say_my_name()


test = Test1()
test.func_1()
test.func_2()
test.func_3()
test.func_4()



ls1 = ['12','32','43']

ls2 = ['1','34']
for i in ls1:ls2.append(i)
print(','.join(ls1))
print(ls2)
# for i in enumerate(df):
#     print(i,enumerate(12))