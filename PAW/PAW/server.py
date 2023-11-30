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