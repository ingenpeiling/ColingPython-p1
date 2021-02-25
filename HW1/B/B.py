def solution(n):
    if n != 0:
        result = "   _~_   " * n + "\n" + "  (o o)  " * n + "\n" + " /  V  \ " * n + "\n" + "/(  _  )\\" * n + "\n" + "  ^^ ^^  " * n
    else:
        result = ""
    return result



