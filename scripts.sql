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
  AND table_name   = 'core_site';

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