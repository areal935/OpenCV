def list_to_range(list1):
    list2 = []
    start = list1[0]
    for num in list1:
        end = num
        if num - 1 not in list1:
            start = num
        if num + 1 not in list1:
            list2.append((start, end))
    return list2

my_list = [1, 2, 3, 4, 5, 8,9, 11, 13]
print(list_to_range(my_list))