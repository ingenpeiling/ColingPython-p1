# Возможно, этот код гораздо сложнее, чем мог бы быть, это попытка реализовать с нуля наивный байесовский классификатор.
# Здесь - немного усовершенствованная версия, с назначением статических весов (внутри функции char_probability).
# Предыдущая версия без весов работала стабильно, выдавала около 80% точности.
# А здесь почему-то при вызове an.predict('на', rev_mod, tag_list, tag_probs) одной строкой все работает хорошо, ответ PREP.
# Но при последующем запуске an.evaluate('pos_data_test.txt', rev_mod, tag_list, tag_probs) и выводе списка ошибок показывает,
# что "на" - NOUN (как было в версии без весов).
# Если после этого вернуться и запустить an.predict('на', rev_mod, tag_list, tag_probs) еще раз, то он тоже выдаст NOUN.
# Как будто какой-то сбой внутри evaluate не дает учитывать веса? Не могу понять, где ошибка.

from corus import load_corpora
import tqdm
from collections import defaultdict

path = 'annot.opcorpora.xml.byfile.zip'
records = load_corpora(path)

with open('pos_data.txt', 'w', encoding='utf8') as f:
    for rec in tqdm.tqdm(records):
        for par in rec.pars:
            for sent in par.sents:
                for token in sent.tokens:
                    f.write(f'{token.text} {token.forms[0].grams[0]}\n')

# делим датасет на test и train
num_lines = 0
with open('pos_data.txt', 'r', encoding="utf8") as f:
    for line in f:
        num_lines += 1
        
last_train = ((80 * num_lines) // 100) - 1
print(last_train)

with open('pos_data.txt', 'r', encoding="utf8") as f:
    for count, line in enumerate(f):
        if count <= last_train:
            with open('pos_data_train.txt', 'a', encoding="utf8") as train:
                train.writelines(line)
        else:
            with open('pos_data_test.txt', 'a', encoding="utf8") as test:
                test.writelines(line)

# начинается сам анализатор
class UnigramMorphAnalyzer:
    def __init__(self):
        pass
    
    def train(self, train_corp):
        """
        (file) -> defaultdict
        Получает на вход обучающую выборку (файл) и возвращает словарь того формата, который
        указан в задании. В дальнейшем этот словарь используется только для
        вывода частеречной статистики по указанному окончанию.
        """
        model = defaultdict(lambda: defaultdict(int))    
        last = ""                                                          
        with open(train_corp, 'r', encoding="utf-8") as train:
            for line in train:
                splitted = line.split()
                for i in range(-1, -5, -1):
                    if splitted[0].lower()[i:] != last:                     # last нужен, чтобы не засчитывать по несколько
                        model[splitted[0].lower()[i:]][splitted[1]] += 1    # раз слова короче 4 символов
                    last = splitted[0].lower()[i:]
        return model
    
    def reverse_train(self, train_corp):
        """
        (file) -> defaultdict
        Получает на вход обучающую выборку (файл) и возвращает словарь вида {'pos_tag': {'й': 22, 'ий':15}},
        где перечислены все части речи из выборки. В дальнейшем предсказании используется именно этот словарь.
        """
        model = defaultdict(lambda: defaultdict(int))  
        last = ""                                         
        with open(train_corp, 'r', encoding="utf-8") as train:   
            for line in train:                                              
                splitted = line.split()
                for i in range(-1, -5, -1):
                    if splitted[0].lower()[i:] != last:
                        model[splitted[1]][splitted[0].lower()[i:]] += 1
                    last = splitted[0].lower()[i:]
        return model
    
    def tag_list(self, train_corp): 
        """
        (file) -> list
        Получает на вход обучающую выборку (файл) и возвращает список всех частеречных тегов оттуда.
        Длина полученного списка равна числу строк в файле.
        """
        full_list = []
        with open(train_corp, 'r', encoding="utf-8") as train:
            for line in train:
                splitted = line.split()
                full_list.append(splitted[1])
        return full_list
  
    def tag_probability(self, tag_list, tag):
        """
        (list, str) -> float
        Получает на вход полный список тегов и тег, для которого необходимо вычислить вероятность. 
        Делит число вхождений данного тега в список на длину списка. 
        Возвращает полученное значение вероятности для данного тега.
        """
        len_tag_list = len(tag_list)
        assert tag in tag_list
        tag_prob = tag_list.count(tag) / len_tag_list
        return tag_prob
    
    def all_tag_probs(self, tag_list):
        """
        (list) -> dict
        Получает на вход полный список тегов и возвращает значение вероятности для каждого из них
        в формате {'NOUN': 0.37425614781661115}
        """
        result = {}
        tag_set = set(tag_list)
        for tag in tag_set:
            result[tag] = UnigramMorphAnalyzer.tag_probability(self, tag_list, tag)
        return result
              
    def char_probability(self, char, tag, rev_model, tag_list):
        """
        (str, str, defaultdict, list) -> float
        Получает на вход один или несколько символов, частеречный тег, словарь, полученный при обучении reverse_train
        и полный список тегов. Затем вычисляет вероятность встретить данное сочетание символов с данным тегом.
        В числителе - сколько раз встретилось данное окончание с данным тегом. 
        В знаменателе - общее число окончаний с данным тегом.
        Возвращает значение вероятности, полученное при делении.
        """
        num = rev_model[tag][char]
        denom = len(rev_model[tag])                               
        return (num / denom) * len(char)              # *len(char) - самый примитивный способ назначить веса ever
    
    def predict(self, word, rev_model, tag_list, all_tag_probs):
        """
        (str, defaultdict, list, dict{str: float}) -> str
        Получает на вход слово, модель, обученную при reverse_train, полный список тегов и список
        вероятностей всех тегов.
        Поочередно для каждого тега вычисляет вероятность встретить один, два, три и четыре последних
        символа с этим тегом и перемножает их. Полученное произведение умножает на вероятность самого
        тега, результат вносит в словарь tag_probs. Затем возвращает тег с максимальным значением из
        tag_probs.
        """
        tags_and_probs = {}                                       
        for tag in rev_model:
            last = ""
            prob = 1
            tag_prob = all_tag_probs[tag]
            for i in range(-1, -5, -1):
                char = word[i:]
                if char != last:
                    prob = prob * UnigramMorphAnalyzer.char_probability(self, char, tag, rev_model, tag_list)
                last = word[i:]                          # было внутри if, но вроде должно быть вне (кажется, работает и так, и так)
            tags_and_probs[tag] = prob * tag_prob
#         for w in sorted(tags_and_probs, key=tags_and_probs.get, reverse=True):         # это если нужно вывести вероятности всех тегов
#               print(w, tags_and_probs[w])               
        result = max(tags_and_probs, key=tags_and_probs.get)
        return result 
        
    def evaluate(self, test_corp, rev_model, tag_list, all_tag_probs):
        """
        (file, defaultdict, list, dict{str: float}) -> float
        Получает на вход тестовую выборку (файл), модель, обученную reverse_train, полный список тегов
        и словарь со значением вероятности для каждого тега. 
        Создает словарь correct формата {'сегодня': ADVB} с правильными ответами.
        Затем размечает тестовую выборку самостоятельно, сохраняя результаты в словарь system того же формата.
        Ключи в словарях correct и system сравниваются, в словарь diff записывается то, что не совпало.
        Затем вычисляется точность: число верных ответов системы делится на общее число ответов
        (оно же - число уникальных слов в тестовой выборке).
        """
        correct = {}
        system = {}
        
        with open(test_corp, 'r', encoding="utf-8") as f:
            for line in f:
                splitted = line.split()
                word = splitted[0]
                tag = splitted[1]
                correct[word] = tag
            
        with open(test_corp, 'r', encoding="utf-8") as f:
            for line in f:
                splitted = line.split()
                word = splitted[0]
                prediction = UnigramMorphAnalyzer.predict(self, word, rev_model, tag_list, all_tag_probs)
                system[word] = prediction
                
        diff = {k: v for k, v in system.items() if correct[k] != system[k]}
        corr_ans = len(system) - len(diff)
        presicion = (corr_ans / len(system)) * 100
        return presicion, diff

    # несколько функций недописаны, т.к. хотела сначала разобраться со всем, что выше.
    
    def save(self):
        pass
    
    def load(self):
        pass
    
# обучение
an = UnigramMorphAnalyzer()
rev_mod = an.reverse_train('pos_data_train.txt')
tag_list = an.tag_list('pos_data_train.txt')
tag_probs = an.all_tag_probs(tag_list)

