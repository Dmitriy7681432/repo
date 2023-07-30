# -*- coding: utf-8 -*-

class AAA(object):
    def __init__(self):
        self.num = "Hello"

    def func_a(self):
        print("Это метода класса А")


class BBB():
    def __init__(self):
        super().__init__()

    def func_b(self):
        print("Это метода класса B")

    def func_a_class(self):
        self.a = AAA()
        self.a.func_a()


# class CCC(BBB):
#
#    def func_c(self):
#       self.c =BBB.func_a_class(self).func_a()
#       return self.c

if __name__ == "__main__":
    a = BBB()
    print(a.func_a())
