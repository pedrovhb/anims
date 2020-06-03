shuffled_arr = [4, 5, 0, 2, 6, 7, 9]

while True:
    swapped = False

    for i in range(len(shuffled_arr) - 1):
        if shuffled_arr[i] > shuffled_arr[i + 1]:
            swapped = True
            shuffled_arr[i], shuffled_arr[i + 1] = shuffled_arr[i + 1], shuffled_arr[i]

    if not swapped:
        break
