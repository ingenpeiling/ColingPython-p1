class ReverseIter:
    def __init__(self, nums):
        self.nums = nums
        self.i = -1
        
    def __iter__(self):
        pass
    
    def __next__(self):
        stop = (-1) * (len(self.nums))
        if self.i >= stop:            
            i = self.i
            self.i = self.i - 1
            return self.nums[i]
        else:
            raise StopIteration()
