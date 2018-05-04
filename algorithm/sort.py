#! encoding=utf-8
# @Time    : 2018/5/4 14:31
# @Author  : lhy

#冒泡排序
def bubble_sort_1(data):
    count = 1
    for i in range(len(data)):
        for j in range(1, len(data)-i):
            count += 1
            if data[j-1] > data[j]:
                # print '({},{})=>({},{})'.format(data[j-1], data[j], data[j], data[j-1])
                data[j-1], data[j] = data[j], data[j-1]
    print count
    return data

def bubble_sort_2(li):
    count = 1
    for j in range(len(li)-1):
        for i in range(1, len(li)):
            count += 1
            if li[i] > li[i-1]:
                li[i], li[i-1] = li[i-1], li[i]
    print count
    return li

def bubble_sort_opt(data):
    count = 1
    for i in range(len(data)):
        no_change_flag = True
        for j in range(1, len(data)-i):
            count += 1
            if data[j-1] > data[j]:
                no_change_flag = False
                # print '({},{})=>({},{})'.format(data[j - 1], data[j], data[j], data[j - 1])
                data[j-1], data[j] = data[j], data[j-1]
        if no_change_flag:
            print count
            return data
    print count
    return data

if __name__ == '__main__':
    data = [12, 4, 5, 6, 7, 2, 3, 9, 8, 11]
    # data = range(15)
    print data
    print bubble_sort_1(data)
    # print bubble_sort_2(data)
    print bubble_sort_opt(data)