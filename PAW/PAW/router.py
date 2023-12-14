import re
import mimetypes
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path


STATIC_DIR = Path("static")
class Router:
    def __init__(self, template_path='templates', static_path='static'):
        self.routes = []
        self.template_env = Environment(loader=FileSystemLoader(template_path))
        self.static_path = static_path.replace('\\', '/')  # Replace backslashes with forward slashes

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
                    # Serve static files
                    response_body, content_type = self.serve_static_file(path)
                    status = '200 OK'
                    headers = [('Content-type', content_type)]
                    start_response(status, headers)
                    return [response_body]
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
            relative_path = os.path.join('..', path.lstrip('/'))
            full_path = os.path.abspath(os.path.join(self.static_path, relative_path))

            print(f"Attempting to read file: {full_path}")

            with open(full_path, 'rb') as file:
                content = file.read()

            content_type, _ = mimetypes.guess_type(path)

            if content_type is None:
                content_type = 'application/octet-stream'

            print(f"Successfully read file. Content Type: {content_type}")
            return content, content_type
        except FileNotFoundError:
            print("File not found. Returning default content.")
            return self.default_handler().encode('utf-8'), 'text/html'

        
        



