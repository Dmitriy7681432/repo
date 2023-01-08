from sqlalchemy import Column, Integer, String

# class Order():
#     def __init__(self, name, price, quantity):
#         self.name = name
#         self.price = price
#         self.quantity= quantity
#
#     def sum(self):
#         return self.price*self.quantity

'''
Better
'''


# class Order():
#     def __init__(self, name, price, quantity):
#         self.name = name
#         self._price = price
#         self._quantity = quantity
#
#     @property
#     def price(self):
#         return self._price
#
#     @price.setter
#     def price(self, value):
#         if value<0:
#             raise ValueError('Цена не должна быть отрицательной')
#
#     @property
#     def quantity(self):
#         return self._quantity
#
#     @quantity.setter
#     def quantity(self, value):
#         if value<0:
#             raise ValueError('Количество не должна быть отрицательной')
#
#     def sum(self):
#         return self._price * self._quantity

'''
The Best
'''
#Дескриптор
class NonNegative:
    def __init__(self, value =0):
        self._value =0

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance,value):
        if value<0:
            raise ValueError('Отрицательное число! Ошибка!')
        self._value =value

#Класс
class Order:
    price =NonNegative()
    quantity = NonNegative()

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity= quantity

    def sum(self):
        return self.price*self.quantity

if __name__ == '__main__':
    apple_order = Order('apple', 15, 2)
    print(apple_order.sum())
    # apple_order.quantity = -1
    # apple_order.price = -100
    print(apple_order.sum())
