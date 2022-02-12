#4.1

# # def add(a,b):
# #      """
# #      :param x:
# #      :param y:
# #      :return:
# #
# #      """
# #      return a+b
# #
# # help(add)
#
#
# def f1(n):
#      print('n = ',n)
#      def f2(m):
#           print('m =',m)
#           return n+m
#      return f2
# new_f = f1(100)
# print(new_f(250))
#
#
# def add(b,a=2,z=10):
#      """
#      :param x:
#      :param y:
#      :return:
#
#      """
#      return a+b+z
#
# print(add(1,2,4))
#
#
# def func(*args):
#      print(type(args),args)
#      return args
#
# func({'a':2,'b':3})
#
#
# def func2(**kwargs):
#      print(type(kwargs),kwargs)
#      return kwargs
#
# func2(a=1,b=2,f=3)
# print('-'*20)
#
# def func3(x=2,y=2,*args,**kwargs):
#      print(type(x),x)
#      print(type(y),y)
#      print(type(args),args)
#      print(type(kwargs),kwargs)
#      return kwargs
#
# func3(3,4, (3,2,3), t=3, t1=4)
#
#4.2

auto =['VOlvo','BMW','Nissan']
map_auto = map(len(auto),auto)
print(map_auto)

sq = map(lambda x:x*x,[0,1,2,3,4])
print(sq)

from functools import reduce
sum = reduce(lambda x,y:x*y,[1,2,3,4,5])
print(sum)


def miles(miles_t):
    return miles_t*1.6

list_miles = [1.0,1.6,2.3]
a = set(map(miles,list_miles))
print(type(a),a)

list_1 =[1,2,3]
list_2 =[4,5,6]
list_3 = list(map(lambda x,y: x*y,list_1,list_2))
print(list_3)

from functools import reduce
list_temp = [43,22,46,101,202,34,95]
max_list = reduce(lambda a,b:a if a>b else b,list_temp)
print(max_list)

list_50 =list(filter(lambda x:x>50,list_temp))
print(list_50)


def fact(n):
    if n<=1:
        return 1
    else:
        return n*fact(n-1)

print(fact(4))


