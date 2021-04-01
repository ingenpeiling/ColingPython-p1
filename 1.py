class OneIndexedList:
    
    def __init__(self, items = None):
        self.items = items or []
    
    def __getitem__(self, key):
        assert key != 0
        return self.items[key - 1]
    
    def __str__(self):
        return '{self.items}'.format(self=self)
    
    def __setitem__(self, index, value):
        assert index != 0
        self.items[index - 1] = value
