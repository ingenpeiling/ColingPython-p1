# все тесты на leetcode пройдены
# Runtime: 56 ms
# Memory Usage: 18.1 MB
# дефолтное значение self.min_num = 2147483648 взято из условия на leetcode, там сказано, что инпута больше 2 ** 31 не будет

class MinStack:

    def __init__(self):
        self.stack = []
        self.min_num = 2147483648
        self.prev_mins = []
        
    def push(self, num):        
        if self.min_num >= num:
            self.prev_mins.append(self.min_num)
            self.min_num = num
        
        self.stack.append(num)        
        return
        
    def pop(self):
        if self.stack[-1] == self.min_num:
            self.min_num = self.prev_mins.pop()
            
        self.stack.pop()
        return
    
    def top(self):
        return self.stack[-1]
        
    def getMin(self):
        return self.min_num
