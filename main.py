import psycopg2
from settings import CORE_TABLE
from word_generator import word_generate
__author__ = 'vako'
import random
conn = psycopg2.connect(database='crm2', user='vako')
cursor = conn.cursor()
ENUM = ['pr', 'wr', 'cu']
if __name__ == '__main__':
    for sd in range(1000):
        print(sd)
        res = "INSERT INTO statistic (inc, description, search) VALUES"
        items = []
        for i in range(100):
            s = """
          (
              ROW('{enum}', {v1}, {v2}, {v3}, current_timestamp),
              '{text}',
              to_tsvector('english', COALESCE('{text}', ''))
          )
            """.format(**{
                'enum': ENUM[random.randint(0, 2)],
                'v1': random.randint(1, 200),
                'v2': random.randint(1, 200),
                'v3': random.randint(1, 200),
                'text': word_generate(random.randint(1, 20))})
            items.append(s)

        cursor.execute(res + ', '.join(items))
        conn.commit()
        # print(s)
        print('start work')
