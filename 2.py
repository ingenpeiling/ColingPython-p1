import collections as coll

def sort_str(inp):    
    alphabet = coll.defaultdict(int)
    for char in "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz":
        alphabet[char]
        
    count = coll.Counter(inp)
    for key in count:
        alphabet[key] += count[key]
    
    result = ""
    for key in alphabet:
        result = result + key * alphabet[key]
            
    return result   
