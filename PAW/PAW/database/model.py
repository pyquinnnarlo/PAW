# model.py
import sqlite3

class Model:
    def __init__(self, db_name='db.sqlite3'):
        self.conn = sqlite3.connect(db_name)
        self.create_table('schema_versions', column_type='TEXT PRIMARY KEY, schema_version INTEGER')


    def create_table(self, table_name, **kwargs):
        # Allow additional keyword arguments for more flexibility
        # Format the fields string using the provided kwargs
        fields = ', '.join([f'{key} {value}' for key, value in kwargs.items()])
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {fields}
        )
        '''
        with self.conn:
            self.conn.execute(query)

    def insert_data(self, table_name, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in range(len(kwargs))])
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'

        with self.conn:
            self.conn.execute(query, tuple(kwargs.values()))
            
    def delete_all_data(self, table_name):
        query = f'DELETE FROM {table_name}'
        with self.conn:
            self.conn.execute(query)
            
    def delete_data(self, table_name, condition_column, condition_value):
        query = f'DELETE FROM {table_name} WHERE {condition_column} = ?'
        with self.conn:
            self.conn.execute(query, (condition_value,))
            
    def delete_data_by_id(self, table_name, id_value):
        query = f'DELETE FROM {table_name} WHERE id = ?'
        with self.conn:
            self.conn.execute(query, (id_value,))

    def fetch_data(self, table_name):
        query = f'SELECT * FROM {table_name}'
        with self.conn:
            cursor = self.conn.execute(query)
            return cursor.fetchall()
        
        
    def character_field(self, table_name, text, default="", nullable=False):
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            "{text}" TEXT DEFAULT '{default}'
        )
        '''
        with self.conn:
            self.conn.execute(query)

    def get_schema_version(self, table_name):
        query = f'SELECT schema_version FROM schema_versions WHERE table_name = ?'
        with self.conn:
            cursor = self.conn.execute(query, (table_name,))
            result = cursor.fetchone()
            return result[0] if result else 0

    def set_schema_version(self, table_name, version):
        query = 'INSERT OR REPLACE INTO schema_versions (table_name, schema_version) VALUES (?, ?)'
        with self.conn:
            self.conn.execute(query, (table_name, version))
