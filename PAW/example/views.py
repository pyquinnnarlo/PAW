from PAW.router import Router
from PAW.utils import Template
from .model import db
from PAW.middleware.auth import authenticate_user

template = Template()


@Router.route('/post_detail/<post_id>/', methods=['GET', 'POST'])
def post_detail(request, post_id):
    print(f"Handling request for post_id: {post_id}")
    if request.command == 'GET':
        data = db.get_dyn('posts')
        print(data)
        html_content = template.render_template('post_detail.html', data)
        return html_content, 200
    else:
        data = db.get_dyn('posts')
        
        html_content = template.render_template('post_detail.html', data)
        return html_content, 200




# @Router.route('/', methods=['GET'])
def app(request):
    if request.command == 'GET':
        # Render all data from database
        collection = 'posts'
        data = db.fetch_data(collection)
        
        # Render the HTML template using Jinja2 with dynamic content
        html_content = template.render_template('app.html', content=data)
        status_code = 200
        context = [html_content, status_code]

        return context
    

@Router.route('/dashboard', methods=['GET', 'POST'])
# @authenticate_user
def dashboard(request):
 
    if request.command == 'GET':
        html_content = template.render_template('dashboard.html')
        return html_content, 200
        
    # Validate POST Method:
    elif request.command == 'POST':
        # Parse form data
        form_data = template.parse_form_data(request)
        # Define the list of field names you want to extract
        field_names = ['title', 'description']
        # Use the second function to get the parsed fields
        parsed_fields = template.parse_form_data_fields(form_data, field_names)

        title = parsed_fields['title']
        description = parsed_fields['description']
        
        # Insert data into the database
        collection = 'posts'  # Change this to the desired table name
        db.insert_data(collection, title=title, description=description)
        

        # Render the HTML template using Jinja2 with dynamic content
        html_content = template.render_template('dashboard.html', dynamic_content=f"Hello, World! {title}, {description}")    
        status_code = 200
        contex = [html_content, status_code]

        return contex 

    
 
 
  
    
    
    
    
    
    
    
    


# @Router.route('/register', methods=['GET', 'POST'])
# def register(request):
#     if request.command == 'GET':
#         # Check if the user is already authenticated
#         if 'user_id' in request.session_data:
#             # Redirect to the dashboard if authenticated
#             redirect_url = '/dashboard'  # Change this to your desired URL
#             headers = {'Location': redirect_url}
#             return '', 302, headers
#         # Render the HTML template for registration form
#         html_content = template.render_template('register_result.html')
#         return html_content, 200
    
#     elif request.command == 'POST':
#         # Parse form data
#         form_data = template.parse_form_data(request)
#         # Define the list of field names you want to extract
#         field_names = ['username', 'email', 'password']
#         # Use the second function to get the parsed fields
#         parsed_fields = template.parse_form_data_fields(form_data, field_names)

#         username = parsed_fields['username']
#         email = parsed_fields['email']
#         password = parsed_fields['password']
        
#         # Register user
#         response = db.register_user(request, username, email, password)
#         if response["success"]:
#             # Set a cookie to store the user's session ID
#             response.set_cookie('session_id', request.session_id)

#         # Render the HTML template for registration result
#         html_content = template.render_template('register_result.html', success=response["success"], message=response["message"])
#         return html_content, 200
    
    
# @Router.route('/login', methods=['GET', 'POST'])
# def login(request):
#     if request.command == 'GET':
#         # Check if the user is already authenticated
#         if 'user_id' in request.session_data:
#             # Redirect to the dashboard if authenticated
#             redirect_url = '/dashboard'  # Change this to your desired URL
#             headers = {'Location': redirect_url}
#             return '', 302, headers
        
#         # Render the HTML template for login form
#         html_content = template.render_template('login_result.html')
#         return html_content, 200
#     elif request.command == 'POST':
#         content_length = int(request.headers['Content-Length'])
#         post_data = request.rfile.read(content_length).decode('utf-8')

#         # Parse form data
#         form_data = template.parser(post_data)
#         username = form_data.get('username', [''])[0]
#         password = form_data.get('password', [''])[0]

#         # Login user
#         response = db.login_user(username, password)

#         if response["success"]:
#             # Set a cookie to store the user's session ID
#             response.set_cookie('session_id', request.session_id)
            
#             # Redirect to the dashboard after successful login
#             redirect_url = '/dashboard'  # Change this to your desired URL
#             headers = {'Location': redirect_url}
#             return '', 302, headers
#         else:
#             # Render the HTML template for login result
#             html_content = template.render_template('login_result.html', success=response["success"], message=response["message"])
#             return html_content, 200


# @Router.route('/logout', methods=['GET'])
# def logout(request):
    # Check if the user is authenticated
    if 'user_id' in request.session_data:
        # Log out the user
        response = db.logout_user(request)
        if response["success"]:
            # Clear the session ID cookie
            response.set_cookie('session_id', '', expires=0)
        return '', 302, {'Location': '/login'}  # Redirect to the login page after logout
    else:
        # If the user is not authenticated, redirect to the login page
        return '', 302, {'Location': '/login'}



# @Router.route('/users/{user_id}', methods=['GET'])
# def get_user(request, user_id):
#     # Handle GET request for a specific user
#     return f"Getting user with ID: {user_id}", 200

# @Router.route('/posts/{post_id}', methods=['GET'])
# def get_post(request, post_id):
#     # Handle GET request for a specific post
#     return f"Getting post with ID: {post_id}", 200