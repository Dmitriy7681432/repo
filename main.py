# a = ['Hello World!\nHow are you','Hello']
# b = [i for i in a if i!='\\r\\n'or i!='\\n']
# print(b)
# for i in a:
#     if i.isspace():
#         print(i)
#

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