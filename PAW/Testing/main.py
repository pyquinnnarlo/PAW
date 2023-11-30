from http.server import BaseHTTPRequestHandler, HTTPServer
from PAW.router import Router

class Utils:
    @staticmethod
    def read_html_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

class MyFrameworkHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        handler = Router.get_handler(self.path)
        response, status_code = handler(self)
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

@Router.route('/')
def home(request):
    html_content = Utils.read_html_file('templates/home.html')
    return html_content, 200  # Assuming 200 OK status

@Router.route('/about')
def about(request):
    html_content = Utils.read_html_file('templates/about.html')
    return html_content, 200  # Assuming 200 OK status

@Router.route('/contact')
def contact(request):
    html_content = Utils.read_html_file('templates/contact.html')
    return html_content, 200  # Assuming 200 OK status


class MyFrameworkServer:
    @staticmethod
    def run(port=8000):
        server_address = ('', port)
        with HTTPServer(server_address, MyFrameworkHandler) as httpd:
            print(f'Starting MyFramework server on port {port}')
            httpd.serve_forever()

if __name__ == '__main__':
    MyFrameworkServer.run()
