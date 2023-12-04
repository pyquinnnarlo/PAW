from PAW.server import MyFrameworkServer
from PAW.router import Router
from urllib.parse import parse_qs
from PAW.utils import Utils
from PAW.database.model import Model


import jinja2
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


db = Model()
class Template:
    def render_template(self, template_name, **kwargs):
            template = template_env.get_template(template_name)
            return template.render(**kwargs)


# Instantiate the Template class
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
        form_data = parse_qs(post_data)
        admin_name = form_data.get('admin_name', [''])[0]
        department = form_data.get('department', [''])[0]

        # Insert data into the database
        table_name = 'teachers'  # Change this to the desired table name
        db.insert_data(table_name, admin_name=admin_name, department=department)

        # Render the HTML template using Jinja2 with dynamic content
        html_content = template.render_template('home.html', dynamic_content=f"Hello, World! {admin_name}, {department}")
        
        return html_content, 200
    

@Router.route('/about', methods=['GET'])
def about(request):
    # Fetch data from the database
    table_name = 'teachers'  # Change this to the desired table name
    data = db.fetch_data(table_name)

    # Render the HTML template using Jinja2 with dynamic content
    html_content = template.render_template('about.html', dynamic_content=f"Data from the database: {data}")

    return html_content, 200




if __name__ == '__main__':
    MyFrameworkServer.run()



# # Parse form data
# form_data = parse_qs(post_data)
# input_value = form_data.get('input_name', [''])[0]