# database.py
import sqlite3

class Database:
    def __init__(self, db_name='paw.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_value TEXT
        )
        '''
        with self.conn:
            self.conn.execute(query)

    def insert_data(self, input_value):
        query = 'INSERT INTO user_data (input_value) VALUES (?)'
        with self.conn:
            self.conn.execute(query, (input_value,))

    def fetch_data(self):
        query = 'SELECT * FROM user_data'
        with self.conn:
            cursor = self.conn.execute(query)
            return cursor.fetchall()
