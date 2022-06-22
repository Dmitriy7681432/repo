# a = ['Hello World!\nHow are you','Hello']
# b = [i for i in a if i!='\\r\\n'or i!='\\n']
# print(b)
# for i in a:
#     if i.isspace():
#         print(i)
#
import unicodedata
c = 'Hello World!\r\nHow are you. Hello'
print(c)
r =[]
b =[]
# [r.append(ch) for ch in c if unicodedata.category(ch)[0]!='C']
for ch in c:
    if unicodedata.category(ch)[0] != 'C':
        r.append(ch)
r=(''.join(r))
r = list(r.split(','))
print(r)
mpa = dict.fromkeys(range(32))
b.append(c.translate(mpa))
print(r)
print(mpa)