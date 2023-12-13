import sqlite3
import re
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import jwt
import time
from PAW.utils import Template
from .session_manager import SessionManager


template = Template()

# Initialize the SessionManager
session_manager = SessionManager()

SECRET_KEY = os.getenv('SECRET_KEY')


class BaseDatabase:
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
        
    def get_dyn(self, table_name, **kwargs):
        # Modify the method to accept any keyword arguments
        if kwargs:
            # If there are additional filters, add WHERE clause to the query
            conditions = [f"{key} = ?" for key in kwargs.keys()]
            conditions_str = " AND ".join(conditions)
            query = f'SELECT id FROM {table_name} WHERE {conditions_str}'
        else:
            # If no additional filters, retrieve all user IDs
            query = f'SELECT id FROM {table_name}'

        with self.conn:
            cursor = self.conn.execute(query, tuple(kwargs.values()))
            user_ids = [row[0] for row in cursor.fetchall()]
            return user_ids
        
    # Write a if statement to check!

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
            # Configure your email server
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
                return("Email sent successfully!")
            except Exception as e:
                return(f"Error: {e}")
        

    def register_user(self, request, username, email, password):
        if not self.is_valid_email(email):
            return {"success": False, "message": "Invalid email format"}

        if len(password) < 8:
            return {"success": False, "message": "Password should be at least 8 characters"}
        
        if not self.is_email_unique(email):
            return {"success": False, "message": "Email already exists. Choose a different email."}
        
        hashed_password = self.hash_password(password)
        self.insert_data('users', username=username, email=email, password=hashed_password)
        
        # Send a registration confirmation email
        subject = "Welcome to Your App"
        message = f"Dear {username},\n\nThank you for registering with Your App!"
        html_content = template.render_template('email_confrimation.html', username=username)
        self.send_email(email, subject, message, html_content)
        
        
        # Set user data in the session
        user_id = self.fetch_data('users', condition_column='username', condition_value=username)[0]['id']
        request.session_data['user_id'] = user_id
        request.session_data['username'] = username
        
        return {"success": True, "message": "User registered successfully. Check your email for confirmation."}

    def login_user(self, request, username, password):
        query = "SELECT * FROM users WHERE username = ?"
        with self.conn:
            cursor = self.conn.execute(query, (username,))
            user_data = cursor.fetchone()

        if user_data:
            stored_password = user_data[2]  # Assuming password is stored in the third column
            if self.verify_password('users', user_data[0], password):
                # Set user data in the session
                request.session_data['user_id'] = str(user_data[0])
                request.session_data['username'] = user_data[1]  # Assuming username is in the second column
                return {"success": True, "message": "Login successful"}
            else:
                return {"success": False, "message": "Incorrect password"}
        else:
            return {"success": False, "message": "User not found"}

    
    def logout_user(self, request):
        # Check if the user is authenticated
        if 'user_id' in request.session_data:
            # Remove the user's session
            session_manager.remove_session(request.session_id)
            return {"success": True, "message": "Logout successful"}
        else:
            return {"success": False, "message": "User not authenticated"}
    

    
    

