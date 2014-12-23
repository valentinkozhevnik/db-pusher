# DB pusher

#### Change setting in your local machine or server



```python
DATABASE = {
    'database': 'crm_custom',
    #'host': '127.0.0.1',
       'user': 'vako',
    #'password': '',
}
```

`CORE_TABLE = 'messages_customer_writer'` - core table in start create tree

`FIRST_STEP_COUNT = 1` 

`CORE_TABLE_COUNT = 100`

## Start script

`python load_data.py`