class Vector:
    def __init__(self,*args):
        print('init')
        self.values= []
        for i in args:
            if isinstance(i, int):
                self.values.append(i)
        self.values.sort()
    def __str__(self):
        print("__str__")
        if len(self.values)>0:
            return f"Вектор{tuple(self.values)}"
        return "Пустой вектор"
    def __add__(self, other):
        print("__add__")
        lst = []
        if isinstance(other,int):
            print("other,int")
            for i in range(len(self.values)):
                lst.append(self.values[i]+other)
            return Vector(*[i for i in lst])
        if isinstance(other,Vector):
            if len(self.values)==len(other.values):
                print("other Vector")
                for i in range(len(self.values)):
                    lst.append(self.values[i]+other.values[i])
                return Vector(*[i for i in lst])
                # return f"Вектор{self.values}"
            else:
                return "Сложение векторов разной длины недопустимо"

v1 = Vector(1,2,3)
print(v1,'v1') # печатает "Вектор(1, 2, 3)"

v2 = Vector(3,4,5)
print(v2,'v2') # печатает "Вектор(3, 4, 5)"
v3 = v1 + v2
print(v3,'v3') # печатает "Вектор(4, 6, 8)"
v4 = v3 + 5
print(v4,'v4') # печатает "Вектор(9, 11, 13)"

















# v1 = Vector(1,2,3)
# # print(v1,'v1') # печатает "Вектор(1, 2, 3)"
#
# v2 = Vector(3,4,5)
# # print(v2,'v2') # печатает "Вектор(3, 4, 5)"
# v5 = v1+3
# print(v5,'v5')
#
# v3 = v1 + v2
# print(v3,'v3') # печатает "Вектор(4, 6, 8)"
#
# v4 = v3 + 5
# print(v4,'v4') # печатает "Вектор(9, 11, 13)"