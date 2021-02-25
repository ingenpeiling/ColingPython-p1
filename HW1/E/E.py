def solution(x1, y1, x2, y2):
    result = False
    if x2 in [x1, x1 + 1, x1 - 1] and y2 in [y1, y1 + 1, y1 - 1]:
        result = True
    return result
