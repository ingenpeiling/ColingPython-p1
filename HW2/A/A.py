def solution(arr):
    count = 0
    repeated = []
    options = [1]
    for i in range(len(arr) - 1):
        if arr[i] == arr[i+1]:
            if arr[i] != arr[i - 1]:
                count = 2
                repeated.append(arr[i])
            else:
                count += 1
                if i == len(arr) - 2:
                    options.append(count)
        elif arr[i] != arr[i+1] and count not in options:
            options.append(count)
    result = max(options)
    return result

# мне кажется, это неизящное решение,
# но хотя бы работает. как написать
# с меньшим числом вложенных if -
# пока не знаю.

