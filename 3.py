def integers():
    num = 1
    while True:
        yield num
        num += 1
        
def squares():
    pm = integers()
    while True:
        yield next(pm) ** 2

def take(num, generator):
    result = []
    for i in range(num):
        result.append(next(generator))
    return result

