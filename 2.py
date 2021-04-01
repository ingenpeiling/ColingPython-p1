from nltk.tokenize import word_tokenize

class FileReader:
    def __init__(self, path, line_count=None, word_count=None):
        self.path = path
        self.line_count = line_count
        self.word_count = word_count
        
    def __str__(self):
        return f'The path to your file is {self.path}'
    
    def __add__(self, path_two, filename):     # filename - адрес (включающий имя) нового файла со склеенным текстом
        with open(self.path, 'r') as file_one: # path_two - путь к второму текстовому файлу
            text_one = file_one.read()
        with open(path_two, 'r') as file_two:
            text_two = file_two.read()
        with open(filename, 'w') as new_file:
            new_text = text_one + "\n" + text_two
            new_file.write(new_text)
        return self
    
    def read(self):
        try:
            with open(self.path, 'r') as file:
                text = file.read()
            return text
        except FileNotFoundError:
            return ''
    
    def write(self, text):                # если в файле уже что-то было, то старый текст исчезнет
        with open(self.path, 'w') as file:
            file.write(text)
        return self
    
    def count(self):
        with open(self.path, 'r') as file:
            line_count = 0
            for line in file:
                line_count += 1
        with open(self.path, 'r') as file:         
            text = file.read()
            word_count = len(word_tokenize(text))        
        self.word_count = word_count
        self.line_count = line_count
        return word_count, line_count
