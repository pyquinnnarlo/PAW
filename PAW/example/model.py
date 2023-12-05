from PAW.database.Mongo_Dd import Model
from pymongo import MongoClient
import datetime


# Usage
client = MongoClient("mongodb://localhost:27017/test-database")
db = Model(client)

# Creating a 'users' collection
#db.create_collection('users')


def Post():
    post = {
        "author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }

    db.insert_data('users', post)







# Create an instance of Model and modify it as needed
# db = Model()
# db.create_table('users', id='INTEGER PRIMARY KEY AUTOINCREMENT', username='TEXT', email='TEXT UNIQUE', password='TEXT')


# student = Model()
# student.create_table('students', id='INTEGER PRIMARY KEY AUTOINCREMENT', admin_name='TEXT', department='TEXT')
