import datetime
import random

from docx.shared import Cm
from docxtpl import DocxTemplate,InlineImage
import csv,json
with open('../lesson_7/7.2_job_doc/home_doc/car.txt') as f:
    car_rand = []
    reader = csv.reader(f)
    for row in f:
        car_rand.append(row.split())
print(row.split())
print(car_rand)
print(car_rand[0][1])

def get_context(brand,model,fuel_cons,price):
    return {
        'Brand':brand,
        'Model':model,
        'Fuel_cons':fuel_cons,
        'Price':price,
    }
def from_car(brand,model,fuel_cons,price,template):
    template =DocxTemplate(template)
    context = get_context(brand,model,fuel_cons,price)

    template.render(context)
    template.save('../lesson_7/7.2_job_doc/home_doc/Car_info1.docx')

def generate_car(brand,model,fuel_cons,price):
    template = '../lesson_7/7.2_job_doc/home_doc/Car_info.docx'
    document = from_car(brand,model,fuel_cons,price,template)

generate_car(car_rand[0][0],car_rand[0][1],car_rand[0][2],car_rand[0][3])

# #Создаём json файл
# with open('car.txt', 'w') as f:
#     json.dump(str(car_rand[0]), f)

# from docxtpl import DocxTemplate
# import csv
# import json
# import random
#
# with open('car.txt') as file:
#     car_rand = []
#     reader = csv.reader(file)
#     for row in file:
#         car_rand.append(row)
# report_car = car_rand[random.randint(0, len(car_rand)-1)]
# car_info = report_car.split()
# # print(car_info)
#
# #Генерируем автоматический отчёт о выбранном автомобиле
# def get_data (Brand, Model, Fuel_cons, Price):
#     return {
#         'Brand': Brand,
#         'Model': Model,
#         'Fuel_cons': Fuel_cons,
#         'Price': Price
#     }
#
# def from_template(Brand, Model, Fuel_cons, Price, template):
#     template = DocxTemplate(template)
#     data = get_data(Brand, Model, Fuel_cons, Price)
#     template.render(data)
#     template.save('Car_info1.docx')
#
# def report(Brand, Model, Fuel_cons, Price):
#     template = 'Car_info.docx'
#     document = from_template(Brand, Model, Fuel_cons, Price, template)
#
# report(car_info[0], car_info[1], car_info[2], car_info[3])
#
#
#
#
#
