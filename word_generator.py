import random

__author__ = 'sergey'

word_file = "dicts/words.txt"
words = open(word_file).read().splitlines()


def word_generate(word_count=1):
    random.shuffle(words)
    return ' '.join(words[:word_count])


if __name__ == '__main__':
    q = word_generate(100)
    print(q)