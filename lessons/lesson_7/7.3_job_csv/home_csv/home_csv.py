import csv
with open('C:/Users/Дмитрий/PycharmProjects/project01/lessons/lesson_7/7.2_job_doc/home_doc/car.txt') as f:
    car=[]
    for i in f:
        a=i.strip()
        b = a.split(',')
        car.append(b)
    print(car)

with open('example2.csv','w') as f_c:
    writer = csv.writer(f_c,delimiter='|')
    writer.writerows(car)


# #Другой чел делал
# #Создаём csv файл
# car_list=[]
# with open('C:/Users/Дмитрий/PycharmProjects/project01/lessons/lesson_7/7.2_job_doc/home_doc/car.txt') as file:
#     for row in file:
#         inner_list = [x.strip() for x in row.split(',')]
#         car_list.append(inner_list)
# print(car_list)
# with open('example2.csv', 'w') as file:
#         writer = csv.writer(file, delimiter = '*')
#         writer.writerows(car_list)