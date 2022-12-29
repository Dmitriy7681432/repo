# -*- coding: utf-8 -*-
import sqlite3 as lite
import  sys

connect = None
try:
    connect =lite.connect('test.db')

    cur =connect.cursor()
    cur.execute('SELECT SQLITE_VERSION()')

    data = cur.fetchone()[0]

    print(f'SQLite version: {data}')

except lite.Error as e:
    print(f"Error {e.args[0]}:")
    sys.exit(1)

# cur.execute('CREATE TABLE cars(id INT, name TEXT, price INT)')
# cur.execute("INSERT INTO cars VALUES(?,?,?)",(1,'Audi', 234212))
# cur.execute("INSERT INTO cars VALUES(2,'Mercedes',57127)")
# cur.execute("INSERT INTO cars VALUES(3,'Skoda',9000)")
# cur.execute("INSERT INTO cars VALUES(4,'Volvo',29000)")
# cur.execute("INSERT INTO cars VALUES(5,'Bentley',350000)")
# cur.execute("INSERT INTO cars VALUES(6,'Citroen',21000)")
# cur.execute("INSERT INTO cars VALUES(7,'Hummer',41400)")
# cur.execute("INSERT INTO cars VALUES(8,'Volkswagen',21600)")
#
# cars_list = [[9, 'Lada',5000], [10,'Renault', 90000]]
# for car in cars_list:
#     cur.execute("INSERT INTO cars VALUES(?,?,?)",(car[0],car[1],car[2]))

#Выгрузка всей инфы с бд
# sqlite_select_query = """SELECT * from cars"""
# cur.execute(sqlite_select_query)
#
# records = cur.fetchall()
# print(len(records))
# for row in records:
#     print(row)

#Выгрузка инфы по строчно, результат тип кортежа
# with connect:
#     cur =connect.cursor()
#     cur.execute("SELECT * FROM cars")
#
#     while True:
#         row = cur.fetchone()
#         if row ==None:
#             break
#         print(row[0],row[1], row[2])


#Выгрузка всё, результат тип JSON
# with connect:
#     connect.row_factory = lite.Row
#
#     cur = connect.cursor()
#     cur.execute('SELECT * FROM cars')
#
#     rows = cur.fetchall()
#
#     for row in rows:
#         print(f"{row['id']},{row['name']}, {row['price']}")

# Редактирование данных (UPDATE and WHERE)
# with connect:
#     cur = connect.cursor()
#     uPrice = 200
#     uId = 2
#     cur.execute("UPDATE cars SET price=? WHERE id>?",(uPrice,uId))
#     print(f"Number of rows updated: {cur.rowcount}")


# Редактирование данных (DELETE and WHERE)
# with connect:
#     cur = connect.cursor()
#     uId = 2
#     cur.execute(f"DELETE FROM cars WHERE id ={uId}")
#     print(f"Number of rows updated: {cur.rowcount}")

# Подсчет рядов с определенными условиями (Count)
# with connect:
#     cur = connect.cursor()
#     uId = 5
#     cars = 'cars'
#     rowsQuery = f"SELECT Count() FROM cars WHERE id > {uId}"
#     cur.execute(rowsQuery)
#     number0fRows = cur.fetchone()[0]
#     print(number0fRows)

#Сортировка (ORDER By)

# with connect:
#
#     cur = connect.cursor()
#     rows_group = f"SELECT * FROM cars ORDER BY cars.price DESC"
#     cur.execute(rows_group)
#
#     rows = cur.fetchall()
#     for row in rows:
#         print(row)


#Объединение таблиц (JOIN)
# cur.execute("CREATE TABLE cars_year(name TEXT, year INT)")
# cur.execute("INSERT INTO cars_year VALUES('Volvo', 2018)")
# cur.execute("INSERT INTO cars_year VALUES('Bentley', 2011)")
# cur.execute("INSERT INTO cars_year VALUES('Citroen', 1937)")
# cur.execute("INSERT INTO cars_year VALUES('LADA', 1945)")

# with connect:
#     cur =connect.cursor()
#
#     # rows_join = f"SELECT * FROM cars JOIN cars_year ON cars.name = cars_year.name"
#     # rows_join = f"SELECT * FROM cars INNER JOIN cars_year ON cars.name = cars_year.name"
#     rows_join = f"SELECT * FROM cars LEFT JOIN cars_year ON cars.name = cars_year.name"
#     # rows_join = f"SELECT * FROM cars RIGHT JOIN cars_year ON cars.name = cars_year.name"
#
#     cur.execute(rows_join)
#     rows = cur.fetchall()
#     for row in rows:
#         print(row)
#
'''
Работаем с изображениями
'''
# with connect:
#     cur = connect.cursor()
#     img = readImage('python.png')
#     img_binary = lite.Binary(img)
#     id = 1
#     #cur.execute("CREATE TABLE images(id INT, data BLOB)")
#     sqlite_insert_blob_query = """ INSERT INTO images (id, data) VALUES (?, ?)"""
#     cur.execute(sqlite_insert_blob_query, (id, img_binary))
#
# with connect:
#     cur = connect.cursor()
#     sqlite_select_query = """SELECT * from images"""
#     cur.execute(sqlite_select_query)
#     records = cur.fetchall()
#
#     print(len(records))
#
#     for row in records:
#         print(row)
connect.close()
