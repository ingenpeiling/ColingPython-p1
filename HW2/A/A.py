# версия после подсказки (короче и меньше вложенных if)
def solution(arr):
    max_elements = 1
    curr_rep = 1
    prev_element = arr[0]
    for element in arr[1:]:
        if element == prev_element:
            curr_rep += 1
            max_elements = max(max_elements, curr_rep)
        else:
            curr_rep = 1
        prev_element = element        
    return max_elements

# версия, изначально написанная мной
def solution_old(arr):
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


