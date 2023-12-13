from PAW.database.Sqlite_3 import Model
from pymongo import MongoClient
import datetime


# Usage
# client = MongoClient("mongodb://localhost:27017/test-database")
# db = Model(client)

# # Creating a 'users' collection
# db.create_collection('users')



# post = {
#     "author": "Quinn",
#     "text": "Things I Love to eat!",
#     "tags": ["Apple", "Orange", "Mango"],
#     "date": datetime.datetime.now(tz=datetime.timezone.utc),
# }

# db.insert_data('users', post)





#Create an instance of Model and modify it as needed
db = Model()
db.create_table('posts', 
                id='INTEGER PRIMARY KEY AUTOINCREMENT', 
                title='TEXT', 
                description='TEXT')


db.get_dyn('posts')