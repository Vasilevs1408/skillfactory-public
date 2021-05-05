def sort_sequence(sequence):
    for i in range(len(sequence)):
        for j in range(len(sequence) - i - 1):
            if sequence[j] > sequence[j + 1]:
                sequence[j], sequence[j + 1] = sequence[j + 1], sequence[j]
    print(sequence)
    return sequence

def binary_search(sorted_list, numb, left, right):
    middle = (right + left) // 2
    if numb > sorted_list[-1]:
        index_1 = len(sorted_list) - 1
        print("нет числа больше числа с индексом", index_1)
    elif numb <= sorted_list[0]:
        print("Нет числа меньше заданного")
    elif sorted_list[middle] == numb:
            a = sorted_list[:middle]
            for i in a:
                if i == numb:
                    a.remove(i)
            index_1 = (len(a) - 1)
            b = sorted_list[middle:]
            for j in b:
                if j < numb and len(b) > 1:
                    b.remove(j)
            ind = b[0]
            index_2 = sorted_list.index(ind)
            print(index_1, index_2)
            return index_1, index_2
    elif numb < sorted_list[middle]:
        return binary_search(sorted_list, numb, left, middle - 1)
    else:
        return binary_search(sorted_list, numb, middle + 1, right)

while True:
    sequence = list(map(int, input("Введите последовательность целых чисел через пробел: ").split()))
    numb = int(input("Введите одно целое число: "))
    sorted_list = sort_sequence(sequence)
    left = sorted_list[0] - 1
    right = sorted_list[-1] - 1
    binary_numb = binary_search(sorted_list, numb, left, right)
    break
