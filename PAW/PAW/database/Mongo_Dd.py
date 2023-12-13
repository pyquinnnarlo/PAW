import pymongo
from pymongo import MongoClient
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re
from dotenv import load_dotenv
import time
import jwt
from PAW.utils import Template
from .session_manager import SessionManager
from pymongo.errors import CollectionInvalid


template = Template()
# Initialize the SessionManager
session_manager = SessionManager()

SECRET_KEY = os.getenv('SECRET_KEY')

class BaseDatabase:
    def __init__(self, client, db_name):
        self.db = client[db_name]

    def create_collection(self, collection_name):
        try:
            # Try to create the collection
            self.db.create_collection(collection_name)
            return(f"Collection '{collection_name}' created successfully.")
        except CollectionInvalid as e:
            # Handle the case where the collection already exists
            return(f"Collection '{collection_name}' already exists.")

    def insert_data(self, collection_name, data):
        collection = self.db[collection_name]
        results = collection.insert_one(data)
        if results:
            return(results)
        else:
            return("Zero insertion made.")
# ------------------------------------------------------------------------------------------------




# ------------------------------------------------------------------------------------------------
    
    def delete_all_data(self, collection_name):
        collection = self.db[collection_name]
        results = collection.delete_many({})
        if results:
            return(results)
        else:
            return("Collection empty!")
# ------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------
    
    def delete_data(self, collection_name, data):
        collection = self.db[collection_name]
        results = collection.delete_one(data)
        if results:
            return(results)
        else:
            return("Item not found!")
# ------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------

    def fetch_data(self, collection_name):
        collection = self.db[collection_name]
        results =  collection.find()
        
        # Collect all results in a list
        if not results:
            return ("No collection found in database.")
            
        all_data = [result for result in results]
        if len(all_data) == 0:
            return ("No collection found in database.")

        # Return the list of all data
        return all_data
# ------------------------------------------------------------------------------------------------




# ------------------------------------------------------------------------------------------------
        
    def find_one(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.find_one(query)

        if result:
            return(result)
        else:
            return("No matching document found.")
# ------------------------------------------------------------------------------------------------



        
# ------------------------------------------------------------------------------------------------
    def insert_many(self, collection_name, documents):
        collection = self.db[collection_name]
        result = collection.insert_many(documents)

        if result:
            return(f"{result} {len(result.inserted_ids)}.")
        else:
            return("Insert operation failed.")

        """
        # Example usage
        # Assuming you have an instance of your class named `db_instance`
        # and you want to insert multiple documents into the collection "your_collection_name"
        # Define a list of documents to insert
        documents_to_insert = [
            {"field1": "value1", "field2": "value2"},
            {"field1": "value3", "field2": "value4"},
            # Add more documents as needed
        ]

        db_instance.insert_many("your_collection_name", documents_to_insert)
        """
# ------------------------------------------------------------------------------------------------


    

# ------------------------------------------------------------------------------------------------


    def update_one(self, collection_name, filter_query, update_data):
        collection = self.db[collection_name]
        result = collection.update_one(filter_query, {"$set": update_data})

        # Process the result
        if result.modified_count > 0:
            return(result)
        else:
            return("No documents matched the filter or the update operation failed.")

        """
        # Example usage
        # Assuming you have an instance of your class named `db_instance`
        # and you want to update a document in the collection "your_collection_name"
        # Define the filter query to identify the document to update
        filter_query = {"field1": "value1"}

        # Define the data to update
        update_data = {"$set": {"field2": "updated_value"}}

        db_instance.update_one("your_collection_name", filter_query, update_data)
        """
        
        
    def replace_one(self, collection_name, filter_query, replacement):
        collection = self.db[collection_name]
        result = collection.replace_one(filter_query, replacement)

        # Process the result
        if result.matched_count > 0:
            return(result)
        else:
            return("No documents matched the filter or the replace operation failed.")

        """
        # Example usage
        # Assuming you have an instance of your class named `db_instance`
        # and you want to replace a document in the collection "your_collection_name"
        # Define the filter query to identify the document to replace
        filter_query = {"field1": "value1"}

        # Define the replacement document
        replacement = {"field1": "new_value1", "field2": "new_value2"}

        db_instance.replace_one("your_collection_name", filter_query, replacement)
        """


    def drop_collection(self, collection_name):
        collection = self.db[collection_name]
        result = collection.drop()

        # Process the result
        if result:
            return(f"{result} {collection_name}")
        else:
            return(f"Failed to drop collection '{collection_name}'.")

        """
        # Example usage
        # Assuming you have an instance of your class named `db_instance`
        # and you want to drop the collection "your_collection_name"

        db_instance.drop_collection("your_collection_name")
        """

    
    
        


class Model(BaseDatabase):
    def __init__(self, client, db_name='test-database'):
        # Load environment variables from .env file
        load_dotenv()
        super().__init__(client, db_name)
        
    def is_valid_email(self, email):
        # Use a simple regular expression for basic email format validation
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(re.match(email_pattern, email))
    
    def is_email_unique(self, email):
        collection_name = 'users'
        # Use case-insensitive query to check for email uniqueness
        existing_user = self.db[collection_name].find_one({"email": {"$regex": f'^{email}$', "$options": "i"}})
        return existing_user is None

    def hash_password(self, password):
        # Use bcrypt for password hashing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')  # Ensure storing the hashed password as text

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
        # Additional logic for MongoDB registration
        if not self.is_valid_email(email):
            return {"success": False, "message": "Invalid email format"}
        
        if len(password) < 8:
            return {"success": False, "message": "Password should be at least 8 characters"}
        
        # Check if the email is already registered
        if self.is_email_unique(email):
            data = {
                "username": username,
                "email": email,
                "password": self.hash_password(password),
            }
            collection_name = 'users'
            self.insert_data(collection_name, data)

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
        else:
            return {"success": False, "message": "Email already exists. Choose a different email."}



    def login_user(self, request, username, password):
        # Check if the user exists
        user_query = {"username": username}
        user_data = self.find_one("users", user_query)

        if user_data:
            # Verify the password
            stored_password = user_data.get("password", "")
            if self.verify_password("users", str(user_data.get("_id")), password):
                # Set user data in the session
                request.session_data['user_id'] = str(user_data['_id'])
                request.session_data['username'] = user_data['username']  # Assuming 'username' is the correct key
                return {"success": True, "message": "Login successful"}
            else:
                return {"success": False, "message": "Incorrect password"}
        else:
            return {"success": False, "message": "User not found"}

        """
        # Example usage
        # Assuming you have an instance of your class named `db_instance`
        # and you want to log in a user with the provided username and password

        login_result = db_instance.login_user("example_username", "example_password")
        print(login_result)
        """


    def logout_user(self, request):
        # Check if the user is authenticated
        if 'user_id' in request.session_data:
            # Remove the user's session
            session_manager.remove_session(request.session_id)
            return {"success": True, "message": "Logout successful"}
        else:
            return {"success": False, "message": "User not authenticated"}
    
    
    # # Example usage
    # username = "example_user"
    # password = "example_password"

    # # Example login
    # login_result = db_instance.login_user(username, password)
    # if login_result["success"]:
    #     auth_token = login_result["token"]
    #     print(f"User logged in. Auth Token: {auth_token}")

    # # Example logout (client-side):
    # # - Clear or expire the token in your client application

    # # Example logout (server-side, optional):
    # # - You can call the logout_user method to perform server-side logout
    # # db_instance.logout_user(auth_token)
    
    
    
    # Example usage
    # user_id = 123
    # token_data = {"user_id": user_id, "exp": int(time.time()) + 3600}  # Expire in 1 hour
    # token = db_instance.generate_token(token_data)
    # print(f"Generated Token: {token}")

    # # Example verification
    # verified_data = db_instance.verify_token(token)
    # if "error" in verified_data:
    #     print(f"Token Verification Failed: {verified_data['error']}")
    # else:
    #     print(f"Verified Data: {verified_data}")
