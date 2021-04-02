from nltk.tokenize import word_tokenize

class FileReader:
    def __init__(self, path, line_count=None, word_count=None):
        self.path = path
        self.line_count = line_count
        self.word_count = word_count
        
    def __str__(self):
        return f'The path to your file is {self.path}'
    
    def __add__(self, other):
        fnames = [self.path, other]
        with open('new_file.txt', 'w') as new_file:
            for fname in fnames:
                with open(fname, 'r') as old_file:
                    for line in old_file:
                        new_file.write(line)
        return new_file

    def read(self):
        try:
            with open(self.path, 'r') as file:
                text = file.read()
            return text
        except FileNotFoundError:
            return ''
    
    def write(self, text):                          # если в файле уже что-то было, то старый текст исчезнет
        with open(self.path, 'w') as file:
            file.write(text)
        return self
    
    def count(self):
        with open(self.path, 'r') as file:
            line_count = 0
            word_count = 0
            for line in file:
                len_line = len(word_tokenize(line))
                line_count += 1
                word_count = word_count + len_line   
        self.word_count = word_count
        self.line_count = line_count
        return word_count, line_count
