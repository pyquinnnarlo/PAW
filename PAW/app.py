# app.py
from wsgiref.simple_server import make_server
from PAW.router import Router
import os

if __name__ == '__main__':
    app = Router()
    
    # Import views module and register routes
    from example.views import *
    
    # Additional route for serving static files
    @app.route(r'^/static/.*$', methods=['GET'])
    def static_files(environ, template_env, form_data=None):
        path = environ.get('PATH_INFO', '/').lstrip('/')
        file_path = os.path.join(os.path.dirname(__file__), 'static', path[len('static/'):])

        try:
            with open(file_path, 'rb') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            return b'404 Not Found'
        
        
    

    
    server = make_server('localhost', 8000, app.handle_request)
    print("Server is running on http://localhost:8000")
    server.serve_forever()
