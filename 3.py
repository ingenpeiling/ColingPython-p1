import itertools
import pymorphy2
import random
import more_itertools

# решила реализовать в виде класса, чтобы записывать список возможных комбинаций в атрибуты, а функцией generate
# просто извлекать одну из них

# сначала использовала itertools.product, но возникла проблема: в списках adjf и nouns около 400 000 слов, если делать
# полное декартово произведение, вышло бы около 160 миллиардов словосочетаний; 
# я ограничила число словосочетаний 50 000, но itertools.product идет по порядку и все эти 50 000 сочетаний у него получались
# с одним и тем же прилагательным - первым в списке;
# more_itertools.random_product позволяет этого избежать, т.к. берет значения из массивов не по порядку, а рандомно.

def main():
    rand = RandomGenerator
    rand.pos('rus_shuffled.txt')
    rand.make_combs()
    rand.generate()

class RandomGenerator:
    def __init__(self, adjf=None, nouns=None, combs=None):
        self.adjf = adjf or []
        self.nouns = nouns or []
        self.combs = combs or []

    def pos(self, filename):
        morph = pymorphy2.MorphAnalyzer()

        adjf = self.adjf
        nouns = self.nouns

        with open(filename, 'r', encoding="utf8") as f:
            for line in f:
                word = line.strip()
                if 'NOUN' in morph.parse(word)[0].tag:
                    nouns.append(word)
                elif 'ADJF' in morph.parse(word)[0].tag:
                    adjf.append(word)
                    
        self.adjf = adjf
        self.nouns = nouns        
        return 
      
    def make_combs(self):
        possible_comb = []
        for i in range(50000):
            it = more_itertools.random_product(self.adjf, self.nouns)
            possible_comb.append(it)
        
        final_combs = []
        for comb in possible_comb:
            adj = comb[0]
            word = comb[1]
            noun_parse = morph.parse(word)[0]
            gender = noun_parse.tag.gender
            try:
                # все приводится к ед.ч., т.к. с тегами мн.ч. у прилагательных непросто, они могут выглядеть по-разному
                # если при склонении возникают ошибки, то такие слова просто пропускаются
                final_noun = noun_parse.inflect({'sing', 'nomn'}).word
            except AttributeError:
                continue

            adj_parse = morph.parse(adj)[0]
            try:
                final_adj = adj_parse.inflect({gender, 'sing', 'nomn'}).word
            except:
                continue

            final_combs.append(f"{final_adj} {final_noun}")
            
        self.combs = final_combs            
        return
    
                
    def generate(self):
        if self.combs:
            return random.choice(self.combs)
        else:
            # если RandomGenerator.make_combs не было запущено раньше и среди атрибутов нет списка словосочетаний,
            # то RandomGenerator.make_combs запустится внутри RandomGenerator.generate
            RandomGenerator.make_combs(self)
            return random.choice(self.combs)
