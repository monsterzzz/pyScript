a = [2, 4, 5, 1, 3]


# def quickSort(unSortList: list):
#     if len(unSortList) == 0:
#         return unSortList
#
#     left = 0
#     right = len(unSortList) - 1
#
#     base = unSortList[left]
#     while left < right:
#
#         while left < right and unSortList[right] >= base:
#             right -= 1
#         unSortList[left] = unSortList[right]
#
#         while left < right and unSortList[left] <= base:
#             left += 1
#         unSortList[right] = unSortList[left]
#
#     unSortList[left] = base
#     unSortList[left+1:] = quickSort(unSortList[left+1:])
#
#     return unSortList
#
# print(quickSort(a))

def b(a):
    a[:1].append(99)


print(a)
b(a)
print(a)

