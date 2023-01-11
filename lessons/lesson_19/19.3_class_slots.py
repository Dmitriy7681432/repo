class Someclass:
    def __init__(self):
        self.my_attr =1

class SomeclassSlots:
    __slots__ = ('my_attr','only_my_attr')
    def __init__(self):
        self.my_attr =1

if __name__ =='__main__':
    # obj = Someclass()
    # obj.no_my_attr = -1
    # print(obj.my_attr, obj.no_my_attr)
    # print(dir(obj))
    # print(obj.__dict__['my_attr'], obj.__dict__['no_my_attr'])

    obj =SomeclassSlots()
    obj.only_my_attr = lambda x: x**2
    # print(obj.only_my_attr(3))
    print(dir(obj))

