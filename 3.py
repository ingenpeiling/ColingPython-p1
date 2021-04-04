# Не исправляла старое, написала заново. Теперь все проще, берем слово, находим его самое длинное окончание в словаре
# и выдаем самую частотную часть речи для этого окончания.
# Точность 85.7% при оценке на тестовых данных open corpora

from corus import load_corpora
import tqdm
from collections import defaultdict
import pickle

def main():    
    
    # загружаем корпус, здесь же считаем, сколько всего строк (num_lines)
    path = 'annot.opcorpora.xml.byfile.zip'
    records = load_corpora(path)
    num_lines = 0

    with open('pos_data.txt', 'w', encoding='utf8') as f:
        for rec in tqdm.tqdm(records):
            for par in rec.pars:
                for sent in par.sents:
                    for token in sent.tokens:
                        num_lines += 1
                        f.write(f'{token.text} {token.forms[0].grams[0]}\n')
                        
    # делим датасет на test и train
    last_train = ((80 * num_lines) // 100) - 1 

    with open('pos_data.txt', 'r', encoding="utf8") as f:
        for count, line in enumerate(f):
            if count <= last_train:
                with open('pos_data_train.txt', 'a', encoding="utf8") as train:
                    train.write(line)
            else:
                with open('pos_data_test.txt', 'a', encoding="utf8") as test:
                    test.write(line)
    return

# создаем словарь test_tagged с правильной разметкой test и сет test_raw с уникальными словами из test без разметки
# изначально это делалось одновременно с делением на test/train, но возникли проблемы с доступом к переменным
def prepare_test(test_file):
    test_tagged = {}
    test_raw = set()
    with open(test_file, 'r', encoding = "utf8") as test:
        for line in test:
            splitted = line.split()
            word = splitted[0]
            tag = splitted[1]
            test_tagged[word] = tag
            test_raw.add(word)
    return test_tagged, test_raw
    
# нужно, т.к. с lambda не работает pickle
def instead_of_lambda():
    return defaultdict(int)

class UnigramMorphAnalyzer:
    def __init__(self, model=None):
        model = defaultdict(instead_of_lambda)
        pass
    
    def __getitem__(self, item):
        return self.model[item]
    
    def train(self, word, tag):
        """
        (str, str) -> defaultdict
        Получает на вход слово и тег и сохраняет информацию о статистике по окончаниям в модель.
        Сохраняет модель как атрибут.
        """
        # model объявляется как пустой словарь только в том случае, если там еще ничего нет
        try:
            model = self.model
        except AttributeError:
            model = defaultdict(instead_of_lambda)
        # проверка на длину нужна, т.к. иначе короткие слова засчитываются по несколько раз
        # например, "вий" - "NOUN" было в корпусе 1 раз, но засчиталось бы как 2, т.к. всегда 4 прохода
        num = -5
        if len(word) < 4:
            num = (len(word)*(-1)) - 1
        for i in range(-1, num, -1):
            model[word[i:]][tag] += 1
        self.model = model
        return
    
    def predict(self, word):
        """
        (str) -> str
        Получает на вход слово и предсказывает часть речи
        """
        num = -4
        while word[num:] not in self.model:
            num = num + 1
            # нужно для случаев, когда окончания нет в словаре
            if num > -1:
                 return 'UNKN'              
        affix = self.model[word[num:]]
        final_list = sorted(affix, key=affix.get, reverse=True)
        result = final_list[0]
        return result
    
    def evaluate(self, test_file):
        """
        (dict, set) -> float
        Получает на вход размеченную тестовую выборку, и набор уникальных слов оттуда, 
        размечает их самостоятельно, затем сравнивает свой результат (predicted) 
        с правильными ответами (test_tagged) и возвращает точность в процентах.
        """
        tagged_and_raw = prepare_test(test_file)
        test_tagged = tagged_and_raw[0]
        test_raw = tagged_and_raw[1]
        predicted = {}
        for word in test_raw:
            prediction = UnigramMorphAnalyzer.predict(self, word)
            predicted[word] = prediction
        errors = {k: v for k, v in predicted.items() if test_tagged[k] != predicted[k]}
        total_num_words = len(test_raw)
        num_errors = len(errors)
        num_corr = total_num_words - num_errors
        precision = (num_corr / total_num_words) * 100
        return precision
    
    def save(self):
        pickle.dump(self.model, open("pos_model.p", "wb"))
        return
    
    def load(self, model_file):
        self.model = pickle.load(open(model_file, "rb"))
        return        
