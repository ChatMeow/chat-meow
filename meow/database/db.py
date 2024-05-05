from sqlite3 import Cursor
import time
import sqlite3
import logging


class DBHandler:
    conn = None
    cursor = None

    def __init__(self, db_file):
        self.conn = sqlite3.connect(
            db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.initialize_database()

    def close(self):
        self.conn.close()

    def execute(self, *args, **kwargs) -> Cursor:
        c = self.cursor.execute(*args, **kwargs)
        self.conn.commit()
        return c

    def initialize_database(self):
        self.execute("""
        create table if not exists prompt(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name varchar(255) not null,
            timestamp bigint not null,
            prompt text not null,
            length bigint not null
        )
        """)

        logging.debug('Database Initialized SUCCESS.')

    def add_one_prompt(self, name: str, prompt: str):
        self.execute('insert into prompt (name, timestamp, prompt, length) values (?,?,?,?)',
                     (name, int(time.time()), prompt, len(prompt)))

    def get_prompt(self, max_prompt_length: int) -> list[dict]:
        prompt_list = []
        index = 0
        current_prompt_length = 0
        while current_prompt_length < max_prompt_length:
            c = self.execute(
                'select name, prompt, length, id from prompt order by id desc limit 2 offset {}'.format(index))
            rows = c.fetchall()
            if not rows:
                break
            index += 2
            for row in rows:  # 保证插入顺序
                current_prompt_length += len(row[1])
                prompt_list.insert(
                    0, {"role": "{}".format(row[0]), "content": "{}".format(row[1])})

        return prompt_list


