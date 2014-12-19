import string
import random
import datetime

__author__ = 'smuravko'


class GeneratorColumns(object):
    def __init__(self, type_enum=None):
        self.type_enum = type_enum

    def get_value(self, data, text_length=100):
        if not isinstance(data, dict):
            return 'error: in type'

        if data['utd'][:5] == 'float':
            max_bites = int(data['utd'][5:])
            num = (1 << max_bites*4)/2 -1
            return float("{0:.2f}".format(random.random() * num))

        elif data['utd'][:3] == 'int':
            size = int(data['utd'][3:])
            num = (1 << size*8)/2 -1
            return random.randint(0, num)

        elif data['utd'] == 'varchar' or data['utd'] == 'text':
            if data['len'] == 0:
                size = text_length
            elif data['len'] != 0:
                size = data['len']

            chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + ' '
            return ''.join(random.choice(chars) for _ in range(size))

        elif data['utd'] == 'timestamptz':
            return '\'%s\'' % str(datetime.datetime.today() - datetime.timedelta(days=-random.randint(1, 100)))

        elif data['utd'] == 'bool':
            return '1'

        elif data['utd'] in self.type_enum.keys():
            size = len(self.type_enum[data['utd']])
            return self.type_enum[data['utd']][random.randint(0, size-1)]

        elif data['utd'] == 'numeric':
            # return "numeric(1,0)"
            num = (1 << 2*1)/2 -1
            return float("{0:.2f}".format(random.random() * num))
        elif data['utd'] == 'inet':
            return '127.0.0.1'
        else:
            print('TYPE NOT FOUNT %s' % data)


