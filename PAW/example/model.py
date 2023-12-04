from PAW.database.model import Model


# Create an instance of Model and modify it as needed
db = Model(db_name='db.sqlite3')
db.create_table('users', id='INTEGER PRIMARY KEY AUTOINCREMENT', username='TEXT', email='TEXT UNIQUE', password='TEXT')



# self.create_table('users', id='INTEGER PRIMARY KEY AUTOINCREMENT', username='TEXT', email='TEXT UNIQUE', password='TEXT')
# self.create_table('students', admin_name='TEXT', department='TEXT', password='TEXT')
