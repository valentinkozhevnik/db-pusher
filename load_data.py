from itertools import groupby
import random
import psycopg2
from settings import CORE_TABLE
from generate_info import GeneratorColumns
from pprint import pprint
__author__ = 'vako'

conn = psycopg2.connect(database='crm_custom', user='vako')
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
        self.table_name = table_name
        self.level = level
        self.column = {}
        self.column_ord = {}
        cursor.execute("""
        select col.column_name, col.data_type, col.udt_name, col.character_maximum_length,
          col.ordinal_position
        from information_schema.columns as col where table_name = '%s' order by ordinal_position
        """ % table_name)
        for a1, a2, a3, a4, a5 in cursor.fetchall():
            self.column[a1] = {
                'type': a2,
                'utd': a3,
                'len': a4 or 0,
                'ord': a5
            }
            self.column_ord[a1] = {
                'type': a2,
                'utd': a3,
                'len': a4 or 0,
                'ord': a5
            }
        self.column_ord2 = sorted(self.column, key=lambda x:self.column[x]['ord'])

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
            print(a1, a2, a3, a4, a5)
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
            print(a1, a2, a3, a4, a5)
            self.foreign_keys.add(a3)
            data = self.column.get(a3, None)
            print(data)
            if isinstance(data, Load_data):
                print('GgGGGGGG'*100)
                self.column[a3].level += 1
            else:
                self.column[a3] = Load_data(a4, level+1, gener=gener)
        _dict[table_name] = self
        self.get_primary_list()
        print(_dict)

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
        # print(self.column_ord2)
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

    print("23423"*100)
    print(_dict)
    sort_table = sorted(_dict, key=lambda x: _dict[x].level, reverse=True)
    print(sort_table)
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
        )).replace('None, ', '').replace('"', '')
        cursor.execute(res)
        try:
            conn.commit()
        except psycopg2.IntegrityError as e:
            print('reload ', e)
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

if __name__ == '__main__s':
    print(enum_database())
    gener = GeneratorColumns(type_enum=enum_database())
    test_data = {'len': 0, 'type': 'double precision', 'utd': 'float8'}
    test_data2 = {'len': 0, 'type': 'double precision', 'utd': 'number'}
    test_data3 = {'len': 0, 'type': 'double precision', 'utd': 'varchar'}
    test_data4 = {'len': 0, 'type': 'double precision', 'utd': 'user_type'}
    test_data5 = {'len': 0, 'type': 'double precision', 'utd': 'choice5'}
    print(gener.get_value(test_data))
    print(gener.get_value(test_data2))
    print(gener.get_value(test_data3))
    print(gener.get_value(test_data4))
    print(gener.get_value(test_data5))


"""
SELECT table_name FROM information_schema.tables
           WHERE table_schema = 'public';


select col.column_name, col.data_type, col.udt_name, col.character_maximum_length, *
from information_schema.columns as col where table_name = 'essays_order';


SELECT
    tc.constraint_name, tc.table_name, kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
--   *
FROM
    information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
WHERE
--   constraint_type = 'FOREIGN KEY' AND
      tc.table_name='essays_order';


SELECT *
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name   = 'essays_order';

select count(*) from essays_order;

SELECT * from essays_order
  LEFT JOIN customers_customer on customers_customer.id = essays_order.customer_id
  WHERE essays_order.total < 1000000;


CREATE TYPE choice5 AS ENUM ('0', '1', '2', '3', '4', '5');

CREATE TYPE user_type AS ENUM('pr', 'wr', 'cu');
CREATE TYPE logger AS (
  user_t user_type,
  user_id INTEGER,
  object_t INTEGER,
  object_id INTEGER,
  date_create TIMESTAMP WITH TIME ZONE
);
CREATE TABLE statistic (
  inc logger PRIMARY KEY ,
  description TEXT,
  search TSVECTOR
);
create index search_index_tsv on statistic USING gin(search);
INSERT INTO statistic (inc, description, search) VALUES
  (
      ROW('pr', 1, 1, 1, current_timestamp),
      'hello info hello',
      to_tsvector('english', COALESCE('hello info hello', ''))
  );


CREATE FUNCTION check_password(uname TEXT, pass TEXT)
RETURNS BOOLEAN AS $$
DECLARE passed BOOLEAN;
BEGIN
        SELECT  (pwd = $2) INTO passed
        FROM    pwds
        WHERE   username = $1;

        RETURN passed;
END;
$$  LANGUAGE;

INSERT INTO statistic VALUES (ROW('pr', 1, 1, 1), 'skdjfhsgdkfjhgsdkfjhgsdkfjhgsdkfjhsgdf');

select * from statistic where (inc).object_id = 10 and (inc).object_t = 50 and (inc).user_t = 'cu';

CREATE TABLE moobar(

    myval INT
);

select * from statistic where description @@ plainto_tsquery('english', 'moldi vanish ' );

 SELECT
   pg_type.typname AS enumtype,
     pg_enum.enumlabel AS enumlabel
--   *
 FROM pg_type
 JOIN pg_enum
     ON pg_enum.enumtypid = pg_type.oid;

SELECT * from pg_type where typname = 'varchar';

"""
