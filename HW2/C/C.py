import numpy

# решение после подсказки, с numpy.rot90
def solution(arr):
    result = [el for el in arr[0]]    # сразу записываем верхнюю строчку как есть
    req_len = len(arr) * len(arr[0])  # необходимую длину финального списка вычисляем сразу, т.к. потом arr будет изменяться
    
    while len(result) != req_len:
        cut = numpy.rot90(arr[1:])
        for el in cut[0]: result.append(el)
        arr = cut
    
    return result


# мое изначальное решение
def solution_old(arr):
    total_len = len(arr[0]) * len(arr)
    result = []
    i = 0
    
    while len(result) < total_len:
        if i == 0:
            result.extend(item for item in arr[0])
            result.extend([item[-1] for item in arr[1:]])
            result.extend([item for item in arr[-1][:-1][::-1]])
            result.extend([item[0] for item in arr[1:-1][::-1]])
        else:
            result.extend(item for item in arr[i][i:-i])
            result.extend([item[-(i+1)] for item in arr[i+1:-i]])
            result.extend([item for item in arr[-(i+1)][i:-(i+1)][::-1]])
            result.extend([item[i] for item in arr[i+1:-(i+1)][::-1]])  
        i += 1
            
    return result


