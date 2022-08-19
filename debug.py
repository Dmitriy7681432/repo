
# Для сети 2
a = (0x80000|0x1|0x2|0x10000|0x20000|0x40000|0x4000|0x8000) &0x1E00
print(a)
print(hex(a))

# Для сети 1
b = (0x80000|0x200|0x400|0x10000|0x20000|0x40000|0x4000|0x8000) &0x1E00
print(b)
f =0b1000000000000
print(f)
# 1111 1100 0000 0000 0011
#         1 1110 0000 0000
a =['STATION_HOURS','MOTOHOURS_ADDR','N_U_AB','EA_U_AB','B_I_A','FC1_I_A']
b=['B_I_A', 'FC2_I_A','EA_U_AB','N_U_AB','STATION_HOURS']
c =a+b

print(c.sort())
print(c)
count=0
d=[]

for i in a:
    if i not in b:
        d.append(i)
for i in b:
    if i not in a:
        d.append(i)
print(d)

