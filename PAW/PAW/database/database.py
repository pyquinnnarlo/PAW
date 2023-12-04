# database.py
import sqlite3

class Database:
    def __init__(self, db_name='db.sqlite3'):
        self.conn = sqlite3.connect(db_name)

    def execute_query(self, query, params=None):
        with self.conn:
            if params:
                self.conn.execute(query, params)
            else:
                self.conn.execute(query)

# This instance will be used throughout the application
db = Database()



#         self.create_table('schema_versions', column_type='TEXT PRIMARY KEY, schema_version INTEGER')
#         self.create_table('students', dev_name='TEXT', age='INTEGER')
#         self.create_table('teachers', admin_name='TEXT', department='TEXT')

#         query = f'SELECT * FROM {table_name}'
#         with self.conn:
#             cursor = self.conn.execute(query)
#             return cursor.fetchall()

   

# if __name__ == "__main__":
#     db_students = Model()
#     db_students.character_field('students', 'first_name', column_type='TEXT')

#     db_teachers = Model()
#     db_teachers.character_field('teachers', 'teacher_name', column_type='TEXT')

#     # Perform migration for students table
#     current_version_students = db_students.get_schema_version('students')
#     db_students.migrate_table('students', current_version_students, 2, migration_query='ALTER TABLE students ADD COLUMN age INTEGER DEFAULT 0')
#     db_students.set_schema_version('students', current_version_students + 1)

#     # Perform migration for teachers table
#     current_version_teachers = db_teachers.get_schema_version('teachers')
#     db_teachers.migrate_table('teachers', current_version_teachers, 2, migration_query='ALTER TABLE teachers ADD COLUMN department TEXT DEFAULT ""')
#     db_teachers.set_schema_version('teachers', current_version_teachers + 1)

#     # Insert data into the "students" and "teachers" tables
#     db_students.insert_data('students', first_name='John', last_name='Doe', age=25)
#     db_teachers.insert_data('teachers', teacher_name='Professor Smith', department='Computer Science')

#     # Fetch and print data from the "students" and "teachers" tables
#     data_students = db_students.fetch_data('students')
#     data_teachers = db_teachers.fetch_data('teachers')

#     print("Data from students table:", data_students)
#     print("Data from teachers table:", data_teachers)



# Assuming 'students' is the table name and '1' is the id to delete
# db.delete_data_by_id('students', 1)


# Assuming 'students' is the table name, 'dev_name' is the condition column, and 'Quinn' is the condition value
# db.delete_data('students', 'dev_name', 'Quinn')


# Assuming 'students' is the table name
# db.delete_all_data('students')