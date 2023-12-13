# router.py
import re

class Router:
    routes_get = {}
    routes_post = {}

    @classmethod
    def route(cls, path, methods=None):
        def wrapper(func):
            if methods is None or 'GET' in methods:
                cls.routes_get[path] = func
            if methods is None or 'POST' in methods:
                cls.routes_post[path] = func
            return func
        return wrapper

    @classmethod
    def get_handler(cls, path):
        for route, handler in cls.routes_get.items():
            print(f"Checking route: {route} for path: {path}")
            if cls.match_path(route, path):
                return handler
        return cls.default_handler

    @classmethod
    def post_handler(cls, path):
        for route, handler in cls.routes_post.items():
            if cls.match_path(route, path):
                return handler
        return cls.default_handler

    @staticmethod
    def default_handler(*args, **kwargs):
        response = "404 Not Found"
        status_code = 404
        return response, status_code

    @staticmethod
    def match_path(route, path):
        # Convert route with parameters to a regex pattern
        pattern = re.sub(r'{[^}]+}', r'([^/]+)', route)
        pattern = f'^{pattern}$'

        # Check if the path matches the pattern
        match = re.match(pattern, path)
        return bool(match)




