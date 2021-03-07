import sys
sys.setrecursionlimit(1500)

def solution(a, b):
    if a == 0:
        return b
    else:
        return solution(a-1, b+1)
