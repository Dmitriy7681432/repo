# Переопределение type

class meta_type(type):
     def __new__(cls, class_name, parents, attributes):
         print('meta.__new__')
         return super().__new__(cls, class_name, parents, attributes)

     def __call__(self, *args, **kwargs):
         print('meta.__call__')
         return super().__call__(*args, **kwargs)


class_type = meta_type('class_type', (), {'attr1': 10})

print(type(class_type))

obj = class_type()

print(obj.attr1)


# Свой метакласс

def upper_attr( class_name, parents, attributes):
    """
      Return a class object, with the list of its attribute turned
      into uppercase.
    """

    # pick up any attribute that doesn't start with '__' and uppercase it
    uppercase_attr = {}
    for name, val in attributes.items():
        print(name, val)
        if not name.startswith('__'):
            uppercase_attr[name.upper()] = val
        else:
            uppercase_attr[name] = val
    print(uppercase_attr)
    return type( class_name, parents, uppercase_attr)

#__metaclass__ = upper_attr # this will affect all classes in the module

class class_my(metaclass = upper_attr):
    foo = 'bip'

print(hasattr(class_my, 'foo'))

print(hasattr(class_my, 'FOO'))

#print(dir(class_my))