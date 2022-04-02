class Dexter:
    def __init__(self):
        self.__lol = ['1,2,3']
        self.pop = ['3,4,5']
    def get_lol(self):
        return self.__lol
    def get_pop(self):
        return self.pop
a = Dexter()
print(a.get_lol())
print(a.pop)
print(a.__lol)