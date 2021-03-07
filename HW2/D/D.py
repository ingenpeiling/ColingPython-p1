def solution(n, k):
    warriors = [i for i in range(1, n+1)]          
    start = 0
    for i in range(1, len(warriors)):
        ind_killed = start + k - 1
        if ind_killed > len(warriors) - 1:
            ind_killed = (ind_killed - len(warriors)) % len(warriors)
        warriors.pop(ind_killed)
        start = ind_killed
    result = warriors[0]
    return result
