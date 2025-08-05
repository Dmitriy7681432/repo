# -*- coding: utf-8 -*-
import asyncio

class Testing3():

    async def hello(self):
        print('Запуск функции hello')
        await asyncio.sleep(0.0001)  # Отдаем управление обратно в Event loop пока ждём
        print('Переключение контекста в функцию hello')

    async def hello2(self):
        print('Запуск функции hello2')
        await asyncio.sleep(0.0001)  # Отдаем управление обратно в Event loop пока ждём
        print('Переключение контекста в функцию hello2')

    async def starter(self):
        await asyncio.gather(self.hello(), self.hello2())

testing = Testing3()
asyncio.run(testing.starter())
