import sqlite3
import re
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from werkzeug.datastructures import MultiDict
from .router import Router
from .sessions import Session

template = Router()

# Initialize the SessionManager
session_manager = Session()

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


class Auth:
    def __init__(self, connection):
        if connection is None:
            raise ValueError("Database connection cannot be None")
        self.conn = connection

    def create_table(self, table_name, **kwargs):
        fields = ', '.join([f'{key} {value}' for key, value in kwargs.items()])
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {fields}
        )
        '''
        with self.conn:
            self.conn.execute(query)
            
            
    def migrate(self, column, data_type):
        cursor = self.conn.execute("PRAGMA table_info(posts)")
        columns = {col[1]: col[2] for col in cursor.fetchall()}

        if column not in columns:
            self.conn.execute(f"ALTER TABLE posts ADD COLUMN {column} {data_type}")
            self.conn.commit()

    def apply_migrations(self, migrations):
        for column, data_type in migrations.items():
            self.migrate(column, data_type)
            
            
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
            
    def fetch_data(self, table_name, **kwargs):
        # Modify the method to accept any keyword arguments
        query = f'SELECT * FROM {table_name}'
        if kwargs:
            # If there are additional filters, add WHERE clause to the query
            conditions = [f"{key} = ?" for key in kwargs.keys()]
            conditions_str = " AND ".join(conditions)
            query += f' WHERE {conditions_str}'

        with self.conn:
            cursor = self.conn.execute(query, tuple(kwargs.values()))
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            result = [dict(zip(columns, row)) for row in rows]
            return result
            
    def get_user_by_id(self, user_id):
        query = 'SELECT * FROM users WHERE id = ?'
        with self.conn:
            cursor = self.conn.execute(query, (user_id,))
            user_data = cursor.fetchone()
            return {"id": user_data[0], "username": user_data[1], "email": user_data[2]} if user_data else None
        
    def set_session_data(self, response, user_id):
        # Customize this method based on your project's requirements
        # For example, you can use cookies to store session information
        session_id = session_manager.create_session(user_id)
        response.headers.add('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly; Secure')

    def hash_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    def verify_password(self, user_id, provided_password):
        query = 'SELECT password FROM users WHERE id = ?'
        with self.conn:
            cursor = self.conn.execute(query, (user_id,))
            hashed_password = cursor.fetchone()

            if hashed_password:
                return bcrypt.checkpw(provided_password.encode('utf-8'), hashed_password[0].encode('utf-8'))

        return False

    def insert_user(self, username, email, password):
        hashed_password = self.hash_password(password)
        with self.conn:
            self.conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                              (username, email, hashed_password))

    

    

    




    def fetch_user_id_by_email(self, email):
        query = 'SELECT id FROM users WHERE email = ?'
        with self.conn:
            cursor = self.conn.execute(query, (email,))
            result = cursor.fetchone()
            return result[0] if result else None


class Model(Auth):
    def __init__(self, db_name='db.sqlite3'):
        # Load environment variables from .env file
        load_dotenv()
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
        
        
    def send_email(self, to_email, subject, message, html_content):
        # Configuration for your email server
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')

        # Create an email message
        email_message = MIMEMultipart()
        email_message.attach(MIMEText(message))
        email_message.attach(MIMEText(html_content, 'html'))
        email_message['Subject'] = subject
        email_message['From'] = smtp_username
        email_message['To'] = to_email

        # Connect to the SMTP server and send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, [to_email], email_message.as_string())
            return "Email sent successfully!"
        except Exception as e:
            return f"Error: {e}"
        
        
    def register_user(self, request, username, email, password):
        if not self.is_valid_email(email):
            return {"success": False, "message": "Invalid email format"}

        if len(password) < 8:
            return {"success": False, "message": "Password should be at least 8 characters"}

        if not self.is_email_unique(email):
            return {"success": False, "message": "Email already exists. Choose a different email."}

        self.insert_user(username, email, password)

        # Send a registration confirmation email
        subject = "Welcome to Your App"
        message = f"Dear {username},\n\nThank you for registering with Your App!"
        html_content = template.render_template('email_confirmation.html', username=username)
        self.send_email(email, subject, message, html_content)

        # Set user data in the session
        user_id = self.fetch_user_id_by_email(email)
        session_id = self.session.create_session(user_id)
        request.session_data['user_id'] = user_id
        request.session_data['username'] = username
        request.session_data['session_id'] = session_id

        return {"success": True, "message": "User registered successfully. Check your email for confirmation."}

    def login_user(self, request, username, password):
        query = "SELECT * FROM users WHERE username = ?"
        with self.conn:
            cursor = self.conn.execute(query, (username,))
            user_data = cursor.fetchone()

        if user_data:
            stored_password = user_data[3]  # Assuming password is stored in the fourth column
            if self.verify_password(user_data[0], password):
                # Set user data in the session
                user_id = user_data[0]
                session_id = self.session.create_session(user_id)
                request.session_data['user_id'] = str(user_id)
                request.session_data['username'] = user_data[1]  # Assuming username is in the second column
                request.session_data['session_id'] = session_id

                return {"success": True, "message": "Login successful"}
            else:
                return {"success": False, "message": "Incorrect password"}
        else:
            return {"success": False, "message": "User not found"}

    def logout_user(self, request):
        # Check if the user is authenticated
        if 'user_id' in request.session_data:
            # Remove the user's session
            user_id = request.session_data['user_id']
            session_id = request.session_data['session_id']
            self.session.delete_session(session_id)
            del request.session_data['user_id']
            del request.session_data['username']
            del request.session_data['session_id']
            return {"success": True, "message": "Logout successful"}
        else:
            return {"success": False, "message": "User not authenticated"}
