def solution(a):
    result = []
    for i in range(len(a[0])):
        result.append([a[0][i]])
    for i in range(1, len(a)):
        y = 0
        for item in a[i]:
            result[y].append(item)
            y += 1
    return result
