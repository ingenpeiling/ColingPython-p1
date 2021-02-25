def solution(a, b):
    original_a = a.copy()
    for item in b:
        if item not in original_a:
            a.append(item)
    result = sorted(a)
    return result
