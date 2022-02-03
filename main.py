f = open('text.txt','r', encoding='UTF-8')
t = f.read()
a = t
f.close()

#Задача 1
znak = ['-',',','«','»','.','?','!','—',';',':']

for i in znak:
     t = t.replace(i,'')
print(t)

