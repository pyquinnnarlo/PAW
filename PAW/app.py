# app.py
from wsgiref.simple_server import make_server
from PAW.router import Router

if __name__ == '__main__':
    app = Router()
    
    # Import views module and register routes
    from PAW.views import *
    
    server = make_server('localhost', 8000, app.handle_request)
    print("Server is running on http://localhost:8000")
    server.serve_forever()
