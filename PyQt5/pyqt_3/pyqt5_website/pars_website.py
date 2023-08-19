#  -*- coding:   utf-8  -*-
from pywebcopy import save_webpage, save_website
import validators


def webpage(url, folder, name):
    save_webpage(
        url=url,
        project_folder=folder,
        project_name=name,
        bypass_robots=True,
        debug=True,
        open_in_browser=True,
        delay=None,
        threaded=False,
    )


def website(url, folder, name):
    save_website(
        url=url,
        project_folder=folder,
        project_name=name,
        bypass_robots=True,
        debug=True,
        open_in_browser=True,
        delay=None,
        threaded=False,
    )


def warning(text):
    print("\033[1m\033[31m{}\033[0m".format(text))


# print("""Выберите цифру:
# 1 - Сохранить страницу
# 2 - Сохранить сайт""")
# b = False
#
# while b == False:
#     try:
#         a = int(input())
#         if a == 1 or a == 2:
#             b = True
#         else:
#             warning("Выберите корректный номер!")
#     except:
#         warning("Только цифры!")
#
# c = False
# while c == False:
#     url = input("Введите ссылку: ")
#     if validators.url(url):
#         c = True
#     else:
#         warning("Некорректная ссылка!")
#
# folder = input("Куда сохранять: ")
# name = input("Название проекта: ")
# if a == 1:
#     webpage(url, folder, name)
# else:
#     website(url, folder, name)

# https://it.kgsu.ru/Python_Qt/pyqt5_001.html
# D://repo/PyQt5/pyqt_3/pyqt5_website

#Страницы
# for i in range(1,314):
#     if i<10:
#         url = f"https://it.kgsu.ru/Python_Qt/pyqt5_00{i}.html"
#     elif i <100:
#         url = f"https://it.kgsu.ru/Python_Qt/pyqt5_0{i}.html"
#     elif i <314:
#         url = f"https://it.kgsu.ru/Python_Qt/pyqt5_{i}.html"
#     folder = "D://repo/PyQt5/pyqt_3/pyqt5_website"
#     name = "pages"
#     webpage(url,folder,name)

#Содержание
# for i in range(0,18):
#     if i<1:
#         url = f"https://it.kgsu.ru/Python_Qt/oglav.html"
#     else:
#         url = f"https://it.kgsu.ru/Python_Qt/oglav{i}.html"
#     folder = "D://repo/PyQt5/pyqt_3/pyqt5_website"
#     name = "contents"
#     webpage(url,folder,name)
#Весь сайт

while True:
    url = "http://it.kgsu.ru/Python_Qt/oglav.html"
    folder = "D://repo/PyQt5/pyqt_3/pyqt5_website"
    name = "all_site"
    website(url,folder,name)
