import os
import shutil

def create_app(app_name):
    app_path = os.path.join(os.getcwd(), app_name)

    # Create the main app folder
    os.makedirs(app_path)

    # Create subfolders (static, templates, PAW)
    app_name_lower = app_name.lower()
    folders = [app_name_lower, 'static', 'templates', 'PAW']
    for folder in folders:
        os.makedirs(os.path.join(app_path, folder))

    # Create files with default content
    default_content = {
        '.gitignore': "# .gitignore",
# -----------------------------------------------------------------------------------------------------|



# -----------------------------------------------------------------------------------------------------|
        f'{app_name_lower}/__init__.py' : 
"""
# __init__.py

""",    
        
# -----------------------------------------------------------------------------------------------------|




# -----------------------------------------------------------------------------------------------------|
        f'{app_name_lower}/views.py' : 
"""
# views.py
from PAW.router import Router
from PAW.utils import Template


template = Template()
""",
        
        
# -----------------------------------------------------------------------------------------------------|


# -----------------------------------------------------------------------------------------------------|
        f'{app_name_lower}/model.py' : 
"""
# model.py
from PAW.database.model import Model
from model import Model

# Create an instance of Model and modify it as needed
db = Model(db_name='db.sqlite3')
db.create_table('users', id='INTEGER PRIMARY KEY AUTOINCREMENT', username='TEXT', email='TEXT UNIQUE', password='TEXT')
""",
        
        
# -----------------------------------------------------------------------------------------------------|




# -----------------------------------------------------------------------------------------------------|
        'main.py': 
"""
# main.py

from PAW.server import MyFrameworkServer
from {}.views import *

# Define a decorator for generating route wrapper functions
def generate_route_wrapper(route_func):
    def wrapper(request):
        return route_func(request)
    return wrapper

# Iterate through functions in views.py and generate corresponding wrappers
for func_name in dir():
    if func_name.startswith("_"):
        continue

    func = globals().get(func_name)
    if callable(func) and hasattr(func, "route_path"):
        wrapper_func = generate_route_wrapper(func)
        setattr(globals(), func_name + "_wrapper", wrapper_func)

if __name__ == '__main__':
    MyFrameworkServer.run()
""".format(app_name_lower),
# -----------------------------------------------------------------------------------------------------|


        
# -----------------------------------------------------------------------------------------------------|
        'PAW/__init__.py' : "# __init__.py",
# -----------------------------------------------------------------------------------------------------|
        'PAW/database/__init__.py': "# __init__.py",
# -----------------------------------------------------------------------------------------------------|
        

# -----------------------------------------------------------------------------------------------------|
        'PAW/database/model.py': 
"""
# model.py
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
        self.create_table('schema_versions', id='INTEGER PRIMARY KEY AUTOINCREMENT', column_type='TEXT PRIMARY KEY, schema_version INTEGER')

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

""",
# -----------------------------------------------------------------------------------------------------|


# -----------------------------------------------------------------------------------------------------|
        'PAW/database/migration.py': 
"""
# migration.py
from database import db

class Migration:
    def __init__(self):
        pass

    def migrate_table(self, table_name, from_version, to_version, migration_query):
        for version in range(from_version + 1, to_version + 1):
            migration_method = getattr(self, f'migrate_{table_name}_to_version_{version}', None)
            if migration_method:
                migration_method(table_name)
                db.set_schema_version(table_name, version)
            else:
                with db.conn:
                    db.conn.execute(migration_query)

# This instance will be used for migrations
migration = Migration()

""",
        'PAW/database/database.py': 
"""
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
""",
# -----------------------------------------------------------------------------------------------------|


# -----------------------------------------------------------------------------------------------------|

        'PAW/router.py' : """
# router.py
# router.py
class Router:
    routes_get = {}
    routes_post = {}

    @classmethod
    def route(cls, path, methods=None):
        def wrapper(func):
            if methods is None or 'GET' in methods:
                cls.routes_get[path] = func
            if methods is None or 'POST' in methods:
                cls.routes_post[path] = func
            return func
        return wrapper

    @classmethod
    def get_handler(cls, path):
        return cls.routes_get.get(path, cls.default_handler)

    @classmethod
    def post_handler(cls, path):
        return cls.routes_post.get(path, cls.default_handler)

    @staticmethod
    def default_handler(*args, **kwargs):
        response = "404 Not Found"
        status_code = 404
        return response, status_code
""",

# -----------------------------------------------------------------------------------------------------|



# -----------------------------------------------------------------------------------------------------|
        'PAW/server.py': """
# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from PAW.router import Router


STATIC_DIR = Path("static")
class MyFrameworkHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/static/'):
            # Serve static files (CSS and JS)
            self.serve_static()
        else:
            handler = Router.get_handler(self.path)
            response, status_code = handler(self)
            self.send_response(status_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
        
    def do_POST(self):
        handler = Router.post_handler(self.path)
        response, status_code = handler(self)
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
        
        
    def serve_static(self):
        try:
            file_path = STATIC_DIR / self.path[8:].replace('\\', '/')  # Replace backslashes with forward slashes
            with open(file_path, 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', self.get_content_type(file_path))
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, 'File Not Found')


    def get_content_type(self, file_path):
        # Determine Content-type based on file extension
        extension = file_path.suffix[1:]
        if extension == 'css':
            return 'text/css'
        elif extension == 'js':
            return 'application/javascript'
        else:
            return 'text/plain'
        
        
class MyFrameworkServer:
    @staticmethod
    def run(port=8000):
        server_address = ('', port)
        with HTTPServer(server_address, MyFrameworkHandler) as httpd:
            print(f'Starting MyFramework server on port {port}')
            httpd.serve_forever()
""",
# -----------------------------------------------------------------------------------------------------|



# -----------------------------------------------------------------------------------------------------|
        'PAW/utils.py': 
"""
# utils.py
class Utils:
    @staticmethod
    def read_html_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
import jinja2
from urllib.parse import parse_qs

class Template:
    def __init__(self, template_folder='templates'):
        self.template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_folder))

    def render_template(self, template_name, **kwargs):
        template = self.template_env.get_template(template_name)
        return template.render(**kwargs)
    
    def parser(self, data):
        return parse_qs(data)
""",
# -----------------------------------------------------------------------------------------------------|



# -----------------------------------------------------------------------------------------------------|
    'templates/index.html': 
"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" type="text/css" href="../static/test.css" />
    <title>PAW Test Page</title>
  </head>
  <body>
    <div>
      <h1>Build and Deploy</h1>
    </div>
    <!-- Link to Github -->
    <div class="g">
      <a href="#">Open Source</a>
    </div>

    <!-- Empty Navbar-->
    <nav class="nav-bar"></nav>

    <!-- Welcome text section -->
    <section id="" class="welcome-display">
      <h1>Welcome to the Home Page</h1>
      <form action="/" method="POST">
        <label for="admin_name">Admin Name:</label>
        <input type="text" id="admin_name" name="admin_name" required />
        <br />
        <label for="department">Department:</label>
        <input type="text" id="department" name="department" required />
        <br />
        <br />
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required />
        <br />
        <input type="submit" value="Submit" />
      </form>
      <p>{{ dynamic_content }}</p>
    </section>
  </body>
</html>


""",


# -----------------------------------------------------------------------------------------------------|



# -----------------------------------------------------------------------------------------------------|
    'static/base.scss': 
"""

// DO NOT CHANGE ANTHING HERE, TILL YOU KNOW WHAT YOU ARE DOING.
/**
    Developed by: PAW
*/




body {
    margin: 0;
    padding: 0;

    --paw-transparent: transparent;
    --paw-black: rgb(11, 11, 11); // Need Fixing

    /** White **/
    --paw-white: rgb(255 255 255);
    --paw-slate-50: rgb(248 250 252);
    --paw-slate-100: rgb(241 245 249);
    --paw-slate-200: rgb(226 232 240);
    --paw-slate-300: rgb(203 213 225);
    --paw-slate-400: rgb(148 163 184);
    --paw-slate-500: rgb(100 116 139);
    --paw-slate-600: rgb(71 85 105);
    --paw-slate-700: rgb(51 65 85);
    --paw-slate-800: rgb(30 41 59);
    --paw-slate-900: rgb(15 23 42);
    --paw-slate-950: rgb(2 6 23);
    /** Gray **/
    --paw-gray-50: rgb(249 250 251);
    --paw-gray-100: rgb(243 244 246);
    --paw-gray-200: rgb(229 231 235);
    --paw-gray-300: rgb(209 213 219);
    --paw-gray-400: rgb(156 163 175);
    --paw-gray-500: rgb(107 114 128);
    --paw-gray-600: rgb(75 85 99);
    --paw-gray-700: rgb(55 65 81);
    --paw-gray-800: rgb(31 41 55);
    --paw-gray-900: rgb(17 24 39);
    --paw-gray-950: rgb(3 7 18);
    /** Zinc **/
   --paw-zinc-50: rgb(250 250 250);
    --paw-zinc-100: rgb(244 244 245);
    --paw-zinc-200: rgb(228 228 231);
    --paw-zinc-300: rgb(212 212 216);
    --paw-zinc-400: rgb(161 161 170);
    --paw-zinc-500: rgb(113 113 122);
    --paw-zinc-600: rgb(82 82 91);
    --paw-zinc-700: rgb(63 63 70);
    --paw-zinc-800: rgb(39 39 42);
    --paw-zinc-900: rgb(24 24 27);
    --paw-zinc-950: rgb(9 9 11);
    /** Neutral **/
    --paw-neutral-50: rgb(250 250 250);
    --paw-neutral-100: rgb(245 245 245);
    --paw-neutral-200: rgb(229 229 229);
    --paw-neutral-300: rgb(212 212 212);
    --paw-neutral-400: rgb(163 163 163);
    --paw-neutral-500: rgb(115 115 115);
    --paw-neutral-600: rgb(82 82 82);
    --paw-neutral-700: rgb(64 64 64);
    --paw-neutral-800: rgb(38 38 38);
    --paw-neutral-900: rgb(23 23 23);
    --paw-neutral-950: rgb(10 10 10);
    /** Stone **/
    --paw-stone-50: rgb(250 250 249);
    --paw-stone-100: rgb(245 245 244);
    --paw-stone-200: rgb(231 229 228);
    --paw-stone-300: rgb(214 211 209);
    --paw-stone-400: rgb(168 162 158);
    --paw-stone-500: rgb(120 113 108);
    --paw-stone-600: rgb(87 83 78);
    --paw-stone-700: rgb(68 64 60);
    --paw-stone-800: rgb(41 37 36);
    --paw-stone-900: rgb(28 25 23);
    --paw-stone-950: rgb(12 10 9);

}

    
"""


# -----------------------------------------------------------------------------------------------------|
        
    }

    for file, content in default_content.items():
        file_path = os.path.join(app_path, file)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write(content)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python create_app.py <app_name>")
        sys.exit(1)

    app_name = sys.argv[1]
    create_app(app_name)
    print(f"App '{app_name}' created successfully.")
