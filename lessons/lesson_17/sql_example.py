# -*- coding: utf-8 -*-
import random
import sqlite3 as lite

NUM_EMP =6
NUM_DEP =5
NAME_EMP = 'Natalia Ksenia Viola Ivan Kostya Kosmos Katya Darya Valya Nikita Serezha Vitya Sarah Petya Victor Seva Lyonya Maxim Vova Raya'.split()

connect = None
try:
    connect =lite.connect('test.db')
    cur = connect.cursor()
except lite.Error as e:
    print(f"Error {e.args[0]}:")
    sys.exit(1)

# cur.execute("CREATE TABLE staff(id INT,id_dep INT, id_head INT, name TEXT, sal INT)")

for i in range(1, NUM_EMP+1):
    id_dep = random.randint(1,NUM_DEP)
    cur.execute("INSERT INTO staff VALUES(?,?,?,?,?)", (i,id_dep,id_dep, NAME_EMP[random.randint(0,len(NAME_EMP)-1)], \
                                                       random.randint(10000, 50000)))
for i in range(1,6):
    cur.execute("UPDATE staff SET id_dep=?, id_head=? WHERE id=?", (i,i,i))

sqlite_select_query = "SELECT *from staff"
cur.execute(sqlite_select_query)
records = cur.fetchall()
for row in records:
    print(row)
#Вывести отдел с наибольшим числом сотрудников
query = "SELECT id_dep, COUNT(id_dep) as Result from staff GROUP BY id_dep ORDER BY Result DESC limit 1"
cur.execute(query)
records = cur.fetchone()
print(records)
print(f'В отделе {records[0]} наибольшее число сотрудников: {records[1]}')

connect.close()
