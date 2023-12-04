from PAW.router import Router
from PAW.utils import Template
from .model import db


template = Template()

@Router.route('/', methods=['GET', 'POST'])
def home(request):
    if request.command == 'GET':
        
        # Render the HTML template using Jinja2
        html_content = template.render_template('home.html')
        return html_content, 200
    elif request.command == 'POST':
        content_length = int(request.headers['Content-Length'])
        post_data = request.rfile.read(content_length).decode('utf-8')

        # Parse form data
        form_data = template.parser(post_data)
        admin_name = form_data.get('admin_name', [''])[0]
        department = form_data.get('department', [''])[0]
        password = form_data.get('password', [''])[0]

        # Insert data into the database
        table_name = 'students'  # Change this to the desired table name
        db.insert_data(table_name, admin_name=admin_name, department=department, password=password)
        # Render the HTML template using Jinja2 with dynamic content
        html_content = template.render_template('home.html', dynamic_content=f"Hello, World! {admin_name}, {department}")
        
        return html_content, 200
    
@Router.route('/about', methods=['GET'])
def about(request):
    # Fetch data from the database
    table_name = 'students'  # Change this to the desired table name
    data = db.fetch_data(table_name)

    # Render the HTML template using Jinja2 with dynamic content
    html_content = template.render_template('about.html', dynamic_content=f"Data from the database: {data}")

    return html_content, 200


@Router.route('/register', methods=['GET', 'POST'])
def register(request):
    if request.command == 'GET':
        # Render the HTML template for registration form
        html_content = template.render_template('register_result.html')
        return html_content, 200
    elif request.command == 'POST':
        content_length = int(request.headers['Content-Length'])
        post_data = request.rfile.read(content_length).decode('utf-8')

        # Parse form data
        form_data = template.parser(post_data)
        username = form_data.get('username', [''])[0]
        email = form_data.get('email', [''])[0]
        password = form_data.get('password', [''])[0]

        # Register user
        response = db.register_user(username, email, password)

        # Render the HTML template for registration result
        html_content = template.render_template('register_result.html', success=response["success"], message=response["message"])
        return html_content, 200
    
    
@Router.route('/login', methods=['GET', 'POST'])
def login(request):
    if request.command == 'GET':
        # Render the HTML template for login form
        html_content = template.render_template('login_result.html')
        return html_content, 200
    elif request.command == 'POST':
        content_length = int(request.headers['Content-Length'])
        post_data = request.rfile.read(content_length).decode('utf-8')

        # Parse form data
        form_data = template.parser(post_data)
        username = form_data.get('username', [''])[0]
        password = form_data.get('password', [''])[0]

        # Login user
        response = db.login_user(username, password)

        if response["success"]:
            # Redirect to a different URL after successful login
            redirect_url = '/dashboard'  # Change this to your desired URL
            headers = {'Location': redirect_url}
            return '', 302, headers
        else:
            # Render the HTML template for login result
            html_content = template.render_template('login_result.html', success=response["success"], message=response["message"])
            return html_content, 200
        
@Router.route('/dashboard', methods=['GET'])
def dashboard(request):
    # Fetch data from the database
    table_name = 'students'  # Change this to the desired table name
    data = db.fetch_data(table_name)

    # Render the HTML template using Jinja2 with dynamic content
    html_content = template.render_template('about.html', dynamic_content=f"Data from the database: {data}")

    return html_content, 200