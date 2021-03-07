def solution(a):
    
    hf = a.find('h')
    hl = a.rfind('h')
    if hf == hl:
        no_hs = a
    else:
        first = a[:a.find('h', hf + 1)]
        middle = a[a.find('h', hf + 1):hl]
        last = a[hl:]
        no_hs = "".join([first, middle.replace('h', 'H'), last])
        
    no_threes = ''.join([no_hs[i] for i in range(len(no_hs)) if i == 0 or i % 3 != 0])
    
    no_ones = no_threes.replace('1', 'one')
    
    return no_ones
