# Простой декоратор
def show_information(f):
    def wrapper(*args, **kwargs):
        print('Код до функции!')
        f(*args, **kwargs)
        print('Код после функции!')
    return wrapper

def simple_function():
    print('Я простая функция')

@show_information
def another_simple_function():
    print('Я тоже простая функция')

simple_function()

simple_function_decorated = show_information(simple_function)

simple_function_decorated()

another_simple_function()

# Декораторы с параметрами


def show_type(f):

    def wrapper(*args, **kwargs):
        print('Код до функции!', type(args[0]))
        print(f(*args, **kwargs))
        print('Код после функции!', type(args[1]))
    return wrapper


@show_information
@show_type
def my_add(a,b):
    return a+b

my_add(10,20)


# Пример использования декоратора

import time
import requests

def show_time(f):

    def wrapper(*args, **kwargs):
        print(time.time())
        print('URL: ', args[0])
        text = f(*args, **kwargs)
        print(time.time())
        return text
    return wrapper

@show_time
def requests_example(url):
    webpage = requests.get(url)
    return webpage.text

url = 'https://google.com'

text = requests_example(url)

print(text)