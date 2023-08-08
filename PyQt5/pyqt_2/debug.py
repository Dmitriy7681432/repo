# -*- coding: utf-8 -*-
#
# class AAA(object):
#     def __init__(self):
#         self.num = "Hello"
#
#     def func_a(self):
#         print("Это метода класса А")
#
#
# class BBB(AAA):
#     # def __init__(self):
#         # super().__init__()
#         # self.num = self.num + "Hello1"
#
#     def func_b(self):
#         print("Это метода класса B")
#
#     def func_a_class(self):
#         self.a = AAA()
#         self.a.func_a()
#
#
# # class CCC(BBB):
# #
# #    def func_c(self):
# #       self.c =BBB.func_a_class(self).func_a()
# #       return self.c
#
# if __name__ == "__main__":
#     a = BBB()
#     text= a.num
#     print(text,"---")
#     # print(a.func_a(),"---")
from PyQt5.QtWidgets import QComboBox

class Bar(QComboBox):

    def connect_activated(self):
        # The PyQt5 documentation will define what the default overload is.
        # In this case it is the overload with the single integer argument.
        self.activated.connect(self.handle_int)

        # For non-default overloads we have to specify which we want to
        # connect.  In this case the one with the single string argument.
        # (Note that we could also explicitly specify the default if we
        # wanted to.)
        self.activated[str].connect(self.handle_string)

    def handle_int(self, index):
        print( "activated signal passed integer", index)

    def handle_string(self, text):
        print( "activated signal passed QString", text)

bar =Bar()
bar.connect_activated()