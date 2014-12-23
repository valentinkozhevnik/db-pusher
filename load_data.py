from itertools import groupby
import random
import psycopg2
from settings import CORE_TABLE, DATABASE
from generate_info import GeneratorColumns
from pprint import pprint
__author__ = 'vako'

conn = psycopg2.connect(**DATABASE)
cursor = conn.cursor()

_dict = {}

def enum_database():
    sql = """
     SELECT
   pg_type.typname AS enumtype,
     pg_enum.enumlabel AS enumlabel
--   *
 FROM pg_type
 JOIN pg_enum
     ON pg_enum.enumtypid = pg_type.oid;
    """

    cursor.execute(sql)
    return dict(map(lambda x: (x[0], list(map(lambda z: z[1], x[1]))),
                    groupby(cursor.fetchall(), key=lambda x: x[0])))

class Load_data(object):
    def __init__(self, table_name, level=0, gener=None):
        print('Scan -- > ', table_name)
        self.table_name = table_name
        self.level = level
        self.column = {}
        self.column_ord = {}
        cursor.execute("""
        select col.column_name, col.data_type, col.udt_name,
          col.character_maximum_length,
          col.ordinal_position, col.numeric_precision, col.numeric_scale
        from information_schema.columns as col where table_name = '%s'
          order by ordinal_position
        """ % table_name)
        for a1, a2, a3, a4, a5, a6, a7 in cursor.fetchall():
            self.column[a1] = {
                'type': a2,
                'utd': a3,
                'len': a4 or 0,
                'ord': a5,
                'num_p': a6 or 0,
                'num_r': a7 or 0,
            }
            self.column_ord[a1] = {
                'type': a2,
                'utd': a3,
                'len': a4 or 0,
                'ord': a5,
                'num_p': a6 or 0,
                'num_r': a7 or 0,
            }
        self.column_ord2 = sorted(self.column,
                                  key=lambda x:self.column[x]['ord'])

        cursor.execute("""SELECT
            tc.constraint_name, tc.table_name, kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM
            information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
        WHERE
           constraint_type = 'PRIMARY KEY' AND
              tc.table_name='%s';""" % table_name)

        self.primary = set()
        for a1, a2, a3, a4, a5 in cursor.fetchall():
            self.primary.add(a3)
        cursor.execute("""SELECT
            tc.constraint_name, tc.table_name, kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM
            information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
        WHERE
           constraint_type = 'FOREIGN KEY' AND
              tc.table_name='%s';""" % table_name)

        self.foreign_keys = set()
        for a1, a2, a3, a4, a5 in cursor.fetchall():
            self.foreign_keys.add(a3)
            data = self.column.get(a3, None)
            if isinstance(data, Load_data):
                self.column[a3].level += 1
            else:
                self.column[a3] = Load_data(a4, level+1, gener=gener)
        _dict[table_name] = self
        self.get_primary_list()

    def get_primary_list(self):
        self.keys = []
        cursor.execute("""
        select %s from %s
        """ % (list(self.primary)[0], self.table_name))
        for i in cursor.fetchall():
            self.keys.append(i[0])
        random.shuffle(self.keys)
        self.keys = self.keys[:1000]

    def add_value(self):
        for value in self.column_ord2:
            if value in self.primary:
                yield None
            elif value in self.foreign_keys:
                yield self.column[value].get_value()
            else:
                yield gener.get_value(self.column[value])

    def get_value(self):
        if len(self.keys) == 0:
            return 0
        random.shuffle(self.keys)
        return self.keys[0]

    def __str__(self):
        return self.column

    def __repr__(self):
        return "<%s> L:%s" % (self.table_name, self.level)

if __name__ == '__main__':
    gener = GeneratorColumns(type_enum=enum_database())
    Load_data(CORE_TABLE, gener=gener)
    create_count = 1

    sort_table = sorted(_dict, key=lambda x: _dict[x].level, reverse=True)

    for i in sort_table:
        print('*'*100)
        print(i)
        if _dict[i].level == 0:
            break
        d = "INSERT INTO %s (%s) VALUES %s"
        lists = []
        for ias in range(create_count):
            lists.append(str(tuple(_dict[i].add_value())))
        res = (d % (
            i,
            ','.join(_dict[i].column_ord2[1:]),
            ', '.join(lists)
        )).replace('None, ', '').replace('"', '')\
            .replace('\'|', '').replace('|\'', '')
        try:
            cursor.execute(res)
            conn.commit()
        except Exception as e:
            print('reload ', e)
            conn.rollback()
        _dict[i].get_primary_list()

    for ds in range(10000):
        d = "INSERT INTO %s (%s) VALUES %s"
        lists = []
        for i in range(100):
            lists.append(str(tuple(_dict[CORE_TABLE].add_value())))
        res = (d % (
            CORE_TABLE,
            ','.join(_dict[CORE_TABLE].column_ord2[1:]),
            ', '.join(lists)
        )).replace('None, ', '').replace('"', '')
        print(ds)
        try:
            cursor.execute(res)
            conn.commit()
        except (psycopg2.IntegrityError, psycopg2.InternalError) as e:
            print('reload ', e)
            conn.rollback()
