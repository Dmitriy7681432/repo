# a = ['Hello World!\nHow are you','Hello']
# b = [i for i in a if i!='\\r\\n'or i!='\\n']
# print(b)
# for i in a:
#     if i.isspace():
#         print(i)
#
import unicodedata
c = 'Hello World!\r\nHow are you. Hello'
# print(c)
r =[]
b =[]
# [r.append(ch) for ch in c if unicodedata.category(ch)[0]!='C']
for ch in c:
    if unicodedata.category(ch)[0] != 'C':
        r.append(ch)
r=(''.join(r))
r = list(r.split(','))
# print(r)
mpa = dict.fromkeys(range(32))
b.append(c.translate(mpa))
# print(r)
# print(mpa)


c = 'Hello World!\nHow are you. Hello'
print(c)
e = []
d = []
for i in c:
    if i!='\r' or i!='\n':
        e.append(i)
print(e)
print(d.append(''.join(e)))
print(d)

z = []
r = [i for i in c if i!='\n']
z.append(''.join(r))
print(z)

print(c.strip('\\n'))


from unicodedata import category
import unicodedata
print(category('\r'))
def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

a =remove_control_characters(c)
print(a)
fa = [ch for ch in c if unicodedata.category(ch)[0]!="C"]
print(''.join(fa))
# e = [1]
# if e == [1]:
#     print('AAAA')
ls = [0]
# if ls ==[0]:
#     print('AAAAAAA')
if ls[4]==False:
    print(len(ls))