class my_class:
    def __init__(self,foo):
        self.foo =foo

class my_class_child(my_class):
    def __init__(self,foo,bar):
        self.foo =foo
        self.bar =bar

'''
  type(<имя класса>,
       <кортеж родительских классов>, # для наследования, может быть пустым
       <словарь, содержащий атрибуты и их значения>)
'''
# my_class =type('my_class',(),{'foo':100})
# my_class_child =type('my_class_child',(my_class,),{'bar':-100})

if __name__ =='__main__':
    # class_temp = my_class
    # print(class_temp)
    # obj1 =my_class(100)
    # print(obj1.foo)
    obj1 =my_class(10)
    print(obj1.foo)
    obj2 =my_class_child(10,-10)
    print(obj2.foo,obj2.bar)

    #__class__
    print(obj1.__class__)
    print(obj1.__class__.__class__)
    print(obj1.__class__.__class__.__class__)
