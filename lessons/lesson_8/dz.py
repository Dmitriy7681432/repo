import time

def show(f):
    def func(*args,**kwargs):
        start_time = time.time()
        print(start_time)
        f(*args,**kwargs)
        stop_time = time.time()
        print(stop_time)
        print(f'Время выполнения функции:{stop_time-start_time}')
    return func

@show
def func1():
    a = ['Volvo','BMW','Audio','Lada','Lexus']
    b =[]
    c =[]
    for i in a:
        b.append(i)
    for i in b:
        c.append(i)
    print(b)
    for i in range(60):
        c.append(i)
    print(c)
    for i in c:
        if not isinstance(i,str):
            i=i+2
            b.append(i)
    print(b)

func1()