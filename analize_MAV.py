def func_a():
    f = open('D:\\log1.txt', 'r')
    d = []
    e = []
    a = 0
    for i in f:
        a += 1
        if 'p3' in i:
            b = int(i[5:])
            # print('b=', b)
            d.append(b)
            z = str(a)
            d.append(z)
        if 'p9' in i and d:
            c = int(i[5:])
            # print('c=', c)
            e.append(c)
            x = str(a)
            e.append(x)
    f.close()
    # print(d)
    # print(e)

    for k, j in zip(d, e):
        # print(k)
        # print(j)
        if isinstance(k, int) and isinstance(j, int) and k > j:
            delta_kj = (360 - k) + j
            if delta_kj > 64:
                flag = 1
                print('p3=', k)
                print('p9=', j)
            else:
                flag = 0
            # print('Ok')
            # print('delta_kj',delta_kj)
        if isinstance(k, str) and flag == 1:
            print('str=', k)
            print('str=', j)
            flag1 = 1
        else:
            flag1 = 0
        if isinstance(k, int) and isinstance(j, int) and k < j:
            delta_kj = j - k
            if delta_kj > 64:
                flag = 1
                print('p3=', k)
                print('p9=', j)
            else:
                flag = 0
            # print('No')
            # print('delta_kj',delta_kj)
        # if isinstance(j,str):print('j=',j)
        if flag == 1 and flag1 == 1:
            print('Error')
            print('**************************')
    return 0


def func_b():
        f = open('D:\\log1.txt', 'r')
        d = []
        e = []
        a = 0
        for i in f:
            a += 1
            if 'p4' in i:
                b = int(i[5:])
                # print('b=', b)
                d.append(b)
                z = str(a)
                d.append(z)
            if 'p10' in i and d:
                c = int(i[5:])
                # print('c=', c)
                e.append(c)
                x = str(a)
                e.append(x)
        f.close()
        # print(d)
        # print(e)

        for k, j in zip(d, e):
            # print(k)
            # print(j)
            if isinstance(k, int) and isinstance(j, int) and k > j:
                delta_kj = (360 - k) + j
                if delta_kj > 64:
                    flag = 1
                    print('p4=', k)
                    print('p10=', j)
                else:
                    flag = 0
                # print('Ok')
                # print('delta_kj',delta_kj)
            if isinstance(k, str) and flag == 1:
                print('str=', k)
                print('str=', j)
                flag1 = 1
            else:
                flag1 = 0
            if isinstance(k, int) and isinstance(j, int) and k < j:
                delta_kj = j - k
                if delta_kj > 64:
                    flag = 1
                    print('p4=', k)
                    print('p10=', j)
                else:
                    flag = 0
                # print('No')
                # print('delta_kj',delta_kj)
            # if isinstance(j,str):print('j=',j)
            if flag == 1 and flag1 == 1:
                print('Error')
                print('**************************')
        return 0


def func_c():
    f = open('D:\\log1.txt', 'r')
    d = []
    e = []
    a = 0
    for i in f:
        a += 1
        if 'p5' in i:
            b = int(i[5:])
            # print('b=', b)
            d.append(b)
            z = str(a)
            d.append(z)
        if 'p11' in i and d:
            c = int(i[5:])
            # print('c=', c)
            e.append(c)
            x = str(a)
            e.append(x)
    f.close()
    # print(d)
    # print(e)

    for k, j in zip(d, e):
        # print(k)
        # print(j)
        if isinstance(k, int) and isinstance(j, int) and k > j:
            delta_kj = (360 - k) + j
            if delta_kj > 64:
                flag = 1
                print('p5=', k)
                print('p11=', j)
            else:
                flag = 0
            # print('Ok')
            # print('delta_kj',delta_kj)
        if isinstance(k, str) and flag == 1:
            print('str=', k)
            print('str=', j)
            flag1 = 1
        else:
            flag1 = 0
        if isinstance(k, int) and isinstance(j, int) and k < j:
            delta_kj = j - k
            if delta_kj > 64:
                flag = 1
                print('p5=', k)
                print('p11=', j)
            else:
                flag = 0
            # print('No')
            # print('delta_kj',delta_kj)
        # if isinstance(j,str):print('j=',j)
        if flag == 1 and flag1 == 1:
            print('Error')
            print('**************************')
    return 0


