from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import threading
import mimetypes

from PAW.router import Router

STATIC_DIR = Path("static")

class MyFrameworkHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/static/'):
            self.serve_static()
        else:
            handler = Router.get_handler(self.path)
            if handler:
                try:
                    response, status_code = handler(self)
                    self.send_response(status_code)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(response.encode('utf-8'))
                except Exception as e:
                    self.handle_error(e)
            else:
                self.send_error(404, 'Not Found')

    def do_POST(self):
        handler = Router.post_handler(self.path)
        if handler:
            try:
                response, status_code = handler(self)
                self.send_response(status_code)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(response.encode('utf-8'))
            except Exception as e:
                self.handle_error(e)
        else:
            self.send_error(404, 'Not Found')

    def serve_static(self):
        try:
            file_path = STATIC_DIR / self.path[8:].replace('\\', '/')
            with open(file_path, 'rb') as file:
                content = file.read()
                self.send_response(200)
                content_type, encoding = mimetypes.guess_type(str(file_path))
                if content_type:
                    self.send_header('Content-type', content_type)
                if encoding:
                    self.send_header('Content-Encoding', encoding)
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, 'File Not Found')
        except Exception as e:
            self.handle_error(e)

    def handle_error(self, e):
        # Log or handle unexpected errors
        self.send_error(500, 'Internal Server Error')
        print(f"Error: {e}")

class MyFileSystemEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Restart server on code modification
        if event.is_directory or not event.src_path.endswith(".py"):
            return

        print("Code modified. Restarting server...")
        subprocess.run(["python", "main.py"])

class MyFrameworkServer:
    @staticmethod
    def run(port=8000):
        server_address = ('', port)
        with HTTPServer(server_address, MyFrameworkHandler) as httpd:
            print(f'Starting MyFramework server on port {port}')

            # Set up file system event handler for code modification
            event_handler = MyFileSystemEventHandler()
            observer = Observer()
            observer.schedule(event_handler, path=".", recursive=True)
            observer.start()

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass

            observer.stop()
            observer.join()
