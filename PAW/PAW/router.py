import re
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader

class Router:
    def __init__(self, template_path='templates', static_path='static'):
        self.routes = []
        self.template_env = Environment(loader=FileSystemLoader(template_path))
        self.static_path = static_path

    def route(self, pattern, methods=['GET']):
        def wrapper(func):
            self.routes.append((re.compile(pattern), func, methods))
            return func
        return wrapper

    def handle_request(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')
        method = environ.get('REQUEST_METHOD', 'GET')

        for pattern, handler, allowed_methods in self.routes:
            match = pattern.match(path)
            if match and method in allowed_methods:
                if method == 'POST':
                    content_length = int(environ.get('CONTENT_LENGTH', 0))
                    post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
                    form_data = parse_qs(post_data)

                    response_body = handler(self.template_env, form_data, *match.groups())
                elif method == 'GET' and path.startswith('/static/'):
                    # Serve static files
                    response_body = self.serve_static_file(path)
                else:
                    response_body = handler(self.template_env, *match.groups())
                break
        else:
            response_body = self.default_handler()

        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        start_response(status, headers)
        return [response_body.encode('utf-8')]

    def default_handler(self):
        return "404 Not Found"

        
    def serve_static_file(self, path):
        try:
            with open(f"{self.static_path}{path}", 'rb') as file:
                content = file.read().decode('utf-8')
                return content, 'text/css'
        except FileNotFoundError:
            return self.default_handler(), 'text/html'
