a = [52, 11, 10, 6, -1, 2.2, 8, 8, 15]

"""
52 
15, 11, 10, 6, -1, 2.2, 8, 8, 15
15, 11, 10, 6, -1, 2.2, 8, 8, 52

"""


def quickSort(unSortList: list):
    if len(unSortList) == 0:
        return unSortList

    left = 0
    right = len(unSortList) - 1

    base = unSortList[left]
    while left < right:

        while left < right and unSortList[right] > base:
            right -= 1
        unSortList[left] = unSortList[right]

        left += 1
        while left < right and unSortList[left] < base:
            left += 1
        unSortList[right] = unSortList[left]

    unSortList[left] = base
    unSortList[:left] = quickSort(unSortList[:left])
    unSortList[left + 1:] = quickSort(unSortList[left + 1:])

    return unSortList


print(quickSort(a))
