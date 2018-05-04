#! encoding=utf-8
# @Time    : 2018/5/4 14:16
# @Author  : lhy
# 二分查找

#二分查找非递归版
def binary_search(data, val):
    low = 0
    high = len(data)
    while low <= high:
        mid = (high + low) // 2
        if val == data[mid]:
            return mid
        elif val < data[mid]:
            high = mid - 1
        else:
            low = mid + 1
    else:
        return None

#二分查找递归版
def binary_search_rec(data, val, low, high):
    if low <= high:
        mid = (low + high) // 2
        if val == data[mid]:
            return mid
        elif val < data[mid]:
            return binary_search_rec(data, val, low, mid-1)
        else:
            return binary_search_rec(data, val, mid+1, high)
    else:
        return None



if __name__ == '__main__':
    val = 4
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    print binary_search(data, val)
    print binary_search_rec(data, val, 0, len(data))