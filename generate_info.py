import string
import re
import random
import datetime
from word_generator import word_generate

__author__ = 'smuravko'


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
        return random.randint(int(find_num(find(minx)[0])[0])+1, int(find_num(find(maxx)[0])[0]) -1)
    else:
        if '>' in value:
            val_in = find_num(find(value)[0])
            return random.randint(int(val_in[0]) + 1, max_value)
        elif '<' in value:
            val_in = find_num(find(value)[0])
            return random.randint(-max_value, int(val_in[0]) - 1)

class GeneratorColumns(object):
    def __init__(self, type_enum=None):
        self.type_enum = type_enum

    def get_value(self, data, text_length=100):
        if not isinstance(data, dict):
            return 'error: in type'
        if 'const' in data.keys():

            return gen(data['const'])

        if data['utd'][:5] == 'float':
            max_bites = int(data['utd'][5:])
            num = (1 << max_bites*4)/2 -1
            return float("{0:.2f}".format(random.random() * num))

        elif data['utd'][:3] == 'int':
            size = int(data['utd'][3:])
            num = (1 << size*8)/2 -1
            return random.randint(0, num)

        elif data['utd'] == 'varchar':
            if data['len'] != 0:
                size = data['len']
            else:
                size = text_length
            if random.randint(0,1):
                return word_generate(random.randint(1, 10))[:size]
            chars = string.ascii_uppercase + \
                    string.ascii_lowercase + string.digits + ' '
            return ''.join(random.choice(chars) for _ in range(size))

        elif data['utd'] == 'text':
            return word_generate(random.randint(20, 100))

        elif data['utd'] == 'timestamptz':
            return '\'%s\'' % str(datetime.datetime.today() -
                                  datetime.timedelta(
                                      days=-random.randint(1, 100)))

        elif data['utd'] == 'bool':
            return '1'

        elif data['utd'] in self.type_enum.keys():
            size = len(self.type_enum[data['utd']])
            return self.type_enum[data['utd']][random.randint(0, size-1)]
        #
        elif data['utd'] == 'numeric':
            first = 10 ** (data['num_p'] - data['num_r'])
            last = 10 ** data['num_r']
            result = '%d.%d' % (
                random.randint(0, first - 1), random.randint(0, last - 1))
            return float(result)
        elif data['utd'] == 'inet':
            return '%d.%d.%d.%d' % (
                random.randint(1, 255),
                random.randint(1, 255),
                random.randint(1, 255),
                random.randint(1, 255)
            )
        else:
            raise Exception('TYPE NOT FOUNT %s' % data)


