import os
import sys
import itertools
import random

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fgrab_path = os.path.join(root_path, 'utils')
sys.path.append(fgrab_path)

from grab_folder import fgrab
from collections import defaultdict

# Code for acquiring the training data used for rhyme model.

path = os.path.join(root_path, 'dataset/english/rhymedata-master/english_gold')

folder = fgrab(path).get_all_in_dir('.pgold')

class RhymePairFinder:
    def __init__(self, path: str):
        self.text = open(path, mode='r',encoding='ISO 8859-1').readlines()

    def get_stanza(self):
        temp = list()
        for line in self.text:
            if not line.strip():
                continue
            if line != '\n':
                temp.append(line.strip())
        return list(itertools.zip_longest(*[iter(temp)]*3))
    
    def get_rhyme(self):
        temp = list()
        result = list()
        for stanza in self.get_stanza():
            d = defaultdict(list)
            for t in list(zip(stanza[0].split(' ')[1:], stanza[1].split(' '))):
                d[t[1]].append(t[0])
            s_result = [list(itertools.combinations(x, 2)) for x in d.values()]
            temp.extend(s_result)
        temp = [pair for pair in temp if len(pair) != 0]
        for pair in temp:
            for t in pair:
                result.append(t)
        return result

    def get_example(self, pairs: set, negaposi: int, length: int):
        result = list()
        if negaposi == 1:
            for pair in pairs:
                result.append(pair[0] + '.' + pair[1] + '.1')
        return result
pairs = list()

for f in folder:
    rpf = RhymePairFinder(f)
    pairs.extend(rpf.get_rhyme())

pairs = list(set(pairs))

def get_example(pairs: list, negaposi: int):
    result = list()

    if negaposi == 0:
        for pair in pairs:
            result.append(pair[0] + '.' + '\t'+ random.choice(pairs)[1] + '.' + '\t' + '0' + '\n')
    if negaposi == 1:
        for pair in pairs:
            result.append(pair[0] + '.' + '\t' + pair[1] + '.' + '\t' + '1' + '\n')
    
    return result

nega = get_example(pairs, 0)
posi = get_example(pairs, 1)

print(len(nega))
print(len(posi))