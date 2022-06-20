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
    if i!='\n':
        e.append(i)
print(e)
print(d.append(''.join(e)))
print(d)