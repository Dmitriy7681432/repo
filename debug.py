a = [[1,2,3,'a'],[4,5,6,'b'],[7,8,9,'c'],[10,11,12,'d']]
b = [1,2,3]
print(' '.join(map(str,b)))
c = [['1', 'Programm','Java'],['2','Programm','Python']]
d = []
for i in c:
   d.append('      '.join(i))
print(d)
for i in d:
    print(i)