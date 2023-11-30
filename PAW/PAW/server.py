from http.server import BaseHTTPRequestHandler, HTTPServer
from PAW.router import Router
class MyFrameworkHandler(BaseHTTPRequestHandler):
    def do_GET(self):
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
        
        
class MyFrameworkServer:
    @staticmethod
    def run(port=8000):
        server_address = ('', port)
        with HTTPServer(server_address, MyFrameworkHandler) as httpd:
            print(f'Starting MyFramework server on port {port}')
            httpd.serve_forever()