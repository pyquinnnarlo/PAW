from PAW.database.model import Model


# Create an instance of Model and modify it as needed
db = Model()
db.create_table('users', id='INTEGER PRIMARY KEY AUTOINCREMENT', username='TEXT', email='TEXT UNIQUE', password='TEXT')


student = Model()
student.create_table('students', id='INTEGER PRIMARY KEY AUTOINCREMENT', admin_name='TEXT', department='TEXT')
