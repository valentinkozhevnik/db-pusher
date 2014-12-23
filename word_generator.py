import random

__author__ = 'sergey'

word_file = "dicts/words.txt"
words = open(word_file).read().splitlines()


def word_generate(word_count=1):
    random.shuffle(words)
    return ' '.join(words[:word_count])

import re
class Checked(object):
    def __init__(self, field, strs):
        self.field = field
        self.strs = strs
        self.res = re.findall(r'\((.*)\)', sty)

def gen(value, max_value=10000):
    def find(info):
        return re.findall(r'\((.*)\)', info)
    def find_num(info):
        return re.findall(r'[\d\-]+', info)
    _and = False
    if "AND" in value:
        _and = True
    if _and:
        res1 = find(value)
        minx, maxx = res1[0].split(' AND ')
        # print(minx, maxx)
        # print(find_num(find(maxx)[0]), find_num(find(minx)[0]))
        return random.randint(int(find_num(find(minx)[0])[0]), int(find_num(find(maxx)[0])[0]))
    else:
        if '>' in value:
            val_in = find_num(find(value)[0])
            return random.randint(int(val_in[0]), max_value)
        elif '<' in value:
            val_in = find_num(find(value)[0])
            return random.randint(-max_value, int(val_in[0]))



if __name__ == '__main__':
    field = 'timezone_num'
    timezone_num = 1
    sty = '(((-12) < timezone_num) AND (timezone_num < 12))'
    sty2 = '(work_count >= 0)'
    print(gen(sty))
    print(gen(sty2))
    print(re.findall(r'\((.*)\)', sty))
    print(re.findall(r'\d(?<=\)\ \<)', sty))
    print(re.findall(r'(?<=\< )\d+', sty))
    if eval('(((-12) < timezone_num) AND (timezone_num < 12))'.replace('AND', 'and')):
        print('YEA')
