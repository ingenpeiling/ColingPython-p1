def solution(a, b):
    initial_a = a.copy()
    for num_b in b:
        if num_b in initial_a:
            continue
        before = 0
        for num_a in a:
            if num_b > num_a:
                before +=1
            else:
                break  
        a.insert(before, num_b)
    return a
