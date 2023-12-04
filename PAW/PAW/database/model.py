import sqlite3
import re
import bcrypt

class BaseDatabase:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self, table_name, **kwargs):
        fields = ', '.join([f'{key} {value}' for key, value in kwargs.items()])
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {fields}
        )
        '''
        with self.conn:
            self.conn.execute(query)

    def insert_data(self, table_name, **kwargs):
        # Hash sensitive fields before inserting
        hashed_fields = ['password']  # Add other sensitive field names as needed
        for field in hashed_fields:
            if field in kwargs:
                kwargs[field] = self.hash_password(kwargs[field])
                
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

    def hash_password(self, password):
        # Use bcrypt for password hashing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')  # Ensure storing the hashed password as text

    def verify_password(self, table_name, user_id, provided_password):
        query = f'SELECT password FROM {table_name} WHERE id = ?'
        with self.conn:
            cursor = self.conn.execute(query, (user_id,))
            hashed_password = cursor.fetchone()

            if hashed_password:
                return bcrypt.checkpw(provided_password.encode('utf-8'), hashed_password[0].encode('utf-8'))

        return False


class Model(BaseDatabase):
    def __init__(self, db_name='db.sqlite3'):
        super().__init__(sqlite3.connect(db_name))
        self.create_table('schema_versions', id='INTEGER PRIMARY KEY AUTOINCREMENT', column_type='TEXT , schema_version INTEGER')

    def is_valid_email(self, email):
        # Use a simple regular expression for basic email format validation
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(re.match(email_pattern, email))
    
    def is_email_unique(self, email):
        query = 'SELECT COUNT(*) FROM users WHERE email = ?'
        with self.conn:
            cursor = self.conn.execute(query, (email,))
            count = cursor.fetchone()[0]
            return count == 0

    def register_user(self, username, email, password):
        if not self.is_valid_email(email):
            return {"success": False, "message": "Invalid email format"}

        if len(password) < 8:
            return {"success": False, "message": "Password should be at least 8 characters"}

        hashed_password = self.hash_password(password)
        self.insert_data('users', username=username, email=email, password=hashed_password)
        return {"success": True, "message": "User registered successfully"}

    def login_user(self, username, password):
        query = "SELECT * FROM users WHERE username = ?"
        with self.conn:
            cursor = self.conn.execute(query, (username,))
            user_data = cursor.fetchone()

        if user_data:
            stored_password = user_data[2]  # Assuming password is stored in the third column
            if self.verify_password('users', user_data[0], password):
                return {"success": True, "message": "Login successful"}
            else:
                return {"success": False, "message": "Incorrect password"}
        else:
            return {"success": False, "message": "User not found"}
