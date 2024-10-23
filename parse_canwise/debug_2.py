# -*- coding: utf-8 -*-
graph_list = ['График 1', 50, [1, 1, 1, 1], 'График 2', 51, [2, 2, 2],'График 2', 54, [4, 4, 4], 'График 2', 52, [3, 3, 3], \
              'График 2', 55, [5, 5, 5, 5], 'График 2', 56, [6, 6, 6],'График 4', 57, [7, 7, 7], 'График 5', 58, [8, 8, 8]
              ]
gr_list = []

def func(arg):
    count = 0
    count1 = -1
    count2 = -1
    count3 = 0
    count4 = -1
    flag = 0
    graph_lst = []
    graph_lst1 = []
    for i in arg:
        count3+=1
        count4+=1
        if count3 ==1:
            # print(count4)
            graph_lst.append([arg[count4],arg[count4+1],arg[count4+2]])
        elif count3 ==3:
            count3 =0
    # print(graph_lst)
    return graph_lst
    # while count < len(arg)/3:
    #     count += 1
    # for i in graph_lst[count1]:
    #     count1+=1
    #     for j in graph_lst[count2]:
    #         count2 += 1
    #         if i==j and count1!=count2:
    #             print(count1)
    #             graph_lst1.append(arg[count1])
    #             graph_lst1.append(arg[count1+1])
    #             graph_lst1.append(arg[count1+2])
    #             graph_lst1.append(arg[count2])
    #             graph_lst1.append(arg[count2+1])
    #             graph_lst1.append(arg[count2+2])
    #             graph_lst.pop(count2)
    #             graph_lst.pop(count2)
    #             graph_lst.pop(count2)
    #             # if flag ==0:
    #             #     cnt =count1
    #             #     graph_lst.append(arg[cnt])
    #             #     graph_lst.append(arg[cnt + 1])
    #             #     graph_lst.append(arg[cnt + 2])
    #             #     flag =1
    #
    #     count2 =-1
    # print(graph_lst1)

func(graph_list)
cnt = 0
cnt1 = 0
gr_list = func(graph_list)
print(gr_list)
for i in gr_list[cnt+cnt1]:
    cnt1+=1
    print(i)
    # print(cnt1)
    # if cnt1==3:
    #     cnt+=1
    #     cnt1 =0