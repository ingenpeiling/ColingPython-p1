def solution(arr):
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
